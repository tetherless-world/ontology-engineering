"""File-based stages: build -> saved asserted RDF -> SHACL -> saved current RDF."""
from __future__ import annotations
from importlib.resources import files
import json
from pathlib import Path
import platform
import rdflib
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, XSD
from .config import as_config, load_profile
from .construction import Builder, parse_graph
from .models import StageResult, InputValidationError, ShaclValidationError
from .serialization import check_destination, save_graph, write_json, atomic_bytes, digest


def input_paths(config):
    paths = [config.path] if config.path else []
    for section, names in {"inputs": ["annotations", "transcript", "base_individuals"],
                           "ontology": ["file", "profile", "import_map"], "annotations": ["column_map"],
                           "state_events": ["event_mapping"], "validation": ["shapes"]}.items():
        paths.extend(v for n in names if (v := config.data[section].get(n)) and isinstance(v, Path))
    return paths


def output_path(config, explicit, name):
    value = explicit or config.data["outputs"].get("output")
    if value:
        return Path(value).resolve()
    directory = config.data["outputs"].get("directory")
    if not directory:
        raise InputValidationError("Supply an output path or outputs.directory")
    return Path(directory) / name


def build_manifest_path(config, target):
    """Keep non-RDF build artifacts in a configurable directory."""
    directory = config.data["outputs"].get("artifacts_directory")
    return (Path(directory) if directory else target.parent) / (target.name + ".manifest.json")


def configure(config, **overrides):
    config = as_config(config)
    for key, value in overrides.items():
        if value is None:
            continue
        if key == "ontology":
            config.data["ontology"]["file"] = Path(value).resolve()
        elif key == "workbook":
            config.data["inputs"]["annotations"] = Path(value).resolve()
        elif key in {"transcript", "base_individuals"}:
            for name in ["transcript", "transcript_sheet", "base_individuals"]:
                config.data["inputs"].pop(name, None)
            config.data["inputs"][key] = Path(value).resolve()
    return config


def preflight(config, paths, *, inputs=(), overwrite=False):
    paths = {k: Path(v).resolve() for k,v in paths.items() if v is not None}
    if len(set(paths.values())) != len(paths):
        raise InputValidationError("Output/report/manifest paths must be distinct")
    protected = input_paths(config) + list(inputs)
    for path in paths.values():
        check_destination(path, inputs=protected, overwrite=overwrite)
    return paths


def report_paths(report):
    if not report:
        return {}
    path = Path(report).resolve()
    return {"report": path, "validation_text": path.with_name(path.name + ".shacl.txt"),
            "validation_rdf": path.with_name(path.name + ".shacl.ttl")}


def snapshot_inputs(paths):
    """Detect concurrent input edits across a multi-sheet/file read."""
    return {Path(p).resolve(): digest(p) for p in paths if p is not None}


def unchanged(snapshot):
    if any(not p.is_file() or digest(p) != before for p, before in snapshot.items()):
        raise InputValidationError("An input changed during execution; rerun against a consistent saved snapshot")


def _build(config):
    try:
        return Builder(config).build()
    except InputValidationError:
        raise
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise InputValidationError(f"Build input: {exc}") from exc


def validate_inputs(config=None, *, workbook=None, ontology=None, transcript=None, base_individuals=None, report=None, overwrite=False):
    config = configure(config, workbook=workbook, ontology=ontology, transcript=transcript, base_individuals=base_individuals)
    paths = preflight(config, {"report": report}, overwrite=overwrite)
    snapshot = snapshot_inputs(input_paths(config))
    _, manifest = _build(config)
    unchanged(snapshot)
    summary = {"stage": "validate-input", "valid": True, **manifest["counts"]}
    if paths:
        write_json(paths["report"], summary)
    return StageResult(None, paths, summary)


def build_individuals(config=None, *, workbook=None, ontology=None, transcript=None, base_individuals=None, output=None, report=None, overwrite=False, dry_run=False):
    config = configure(config, workbook=workbook, ontology=ontology, transcript=transcript, base_individuals=base_individuals)
    target = output_path(config, output, "asserted-individuals.rdf")
    report = report or config.data["outputs"].get("report")
    manifest_path = build_manifest_path(config, target)
    paths = preflight(config, {"output": target, "manifest": manifest_path, "report": report}, overwrite=overwrite)
    snapshot = snapshot_inputs(input_paths(config))
    graph, manifest = _build(config)
    unchanged(snapshot)
    manifest.update({"stage": "build", "python_version": platform.python_version(), "rdflib_version": rdflib.__version__, "dry_run": dry_run})
    if config.path:
        manifest["config_sha256"] = digest(config.path)
    if not dry_run:
        save_graph(graph, target)
        write_json(manifest_path, manifest)
    if report:
        write_json(paths["report"], manifest)
    return StageResult(None if dry_run else target, {k:v for k,v in paths.items() if k != "output" and (not dry_run or k == "report")}, manifest)


def _refresh(graph, config, shapes=None, ontology=None):
    """Minimal SHACL flow; no independent Python history validation."""
    from pyshacl import validate, __version__ as version
    profile = load_profile(config)
    ns = profile["namespace"]
    terms = profile.get("terms", {})
    def term(name):
        value = terms.get(name, name)
        return URIRef(value if "://" in value or value.startswith("urn:") else ns + value)
    supplied = shapes or config.shapes
    if supplied:
        shape_graph = parse_graph(supplied)
    else:
        if ns != "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/" or terms:
            raise InputValidationError("A changed namespace or term map requires explicit compatible SHACL shapes (including embedded SPARQL); the packaged CJF shapes are not rewritten")
        shape_graph = Graph().parse(data=files("cjf_serializer").joinpath("resources/shacl/current-state-assignment-rules.ttl").read_text(), format="turtle")
        # Adapt only the packaged template. User shapes are never silently edited.
        default_ns = "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/"
        def mapped(node):
            return term(str(node)[len(default_ns):]) if isinstance(node, URIRef) and str(node).startswith(default_ns) else node
        adapted = Graph()
        for s,p,o in shape_graph:
            adapted.add((mapped(s), mapped(p), mapped(o)))
        shape_graph = adapted
        schema_path = ontology or config.data["ontology"].get("file")
        if schema_path:
            schema = parse_graph(schema_path, config.data["ontology"].get("format"))
            from rdflib.namespace import RDFS
            ranges = set(schema.objects(term("hasTurnNumber"), RDFS.range))
        else:
            ranges = {value.datatype for value in graph.objects(None, term("hasTurnNumber")) if isinstance(value, rdflib.Literal)}
        if len(ranges) == 1 and next(iter(ranges)) in {XSD.int, XSD.integer, XSD.positiveInteger}:
            datatype = next(iter(ranges))
            for subject, predicate in list(shape_graph.subject_predicates(XSD.integer)):
                shape_graph.set((subject, predicate, datatype))
        elif ranges:
            raise InputValidationError("Mixed/unsupported turn datatypes; supply compatible shapes explicitly")
    existing = set(graph.triples((None, term("hasCurrentStateAssignment"), None)))
    moves = set(graph.subjects(term("hasStateAssignment"), None))
    for move in moves:
        graph.remove((move, term("hasCurrentStateAssignment"), None))
    # The engine checks meta-shapes, applies rules, then validates the data.
    # One validate() call; no second run or Python-derived endpoint comparison.
    conforms, report_graph, report_text = validate(graph, shacl_graph=shape_graph, advanced=True,
        inference="none", inplace=True, iterate_rules=True, do_owl_imports=False, meta_shacl=True)
    if not conforms:
        raise ShaclValidationError(str(report_text), report_graph)
    current = set(graph.triples((None, term("hasCurrentStateAssignment"), None)))
    return graph, report_graph, str(report_text), {"stage": "shacl", "shacl_conforms": True,
        "pyshacl_version": version, "rdflib_version": rdflib.__version__, "moves_with_state": len(moves),
        "current_assignment_links": len(current), "new_current_links": len(current-existing),
        "stale_current_links_removed": len(existing-current), "inference_status": "skipped"}


def run_shacl(individuals, *, shapes=None, output=None, config=None, ontology=None, report=None, overwrite=False, dry_run=False):
    config = configure(config, ontology=ontology)
    target = output_path(config, output, "current-individuals.rdf")
    reports = report_paths(report or config.data["outputs"].get("report"))
    preflight(config, {"output": target, **reports}, inputs=[individuals, shapes] if shapes else [individuals], overwrite=overwrite)
    snapshot = snapshot_inputs([individuals, shapes, config.shapes, config.data["ontology"].get("file"), config.path])
    graph = parse_graph(individuals)
    try:
        graph, report_graph, text, summary = _refresh(graph, config, shapes, ontology)
    except ShaclValidationError as exc:
        if reports:
            write_json(reports["report"], {"stage": "shacl", "shacl_conforms": False, "error": str(exc)})
            atomic_bytes(reports["validation_text"], exc.report_text.encode())
            atomic_bytes(reports["validation_rdf"], exc.report_graph.serialize(format="turtle", encoding="utf-8"))
        raise
    summary.update({"individuals": str(Path(individuals).resolve()), "output": str(target), "dry_run": dry_run})
    unchanged(snapshot)
    if not dry_run:
        save_graph(graph, target)
    if reports:
        write_json(reports["report"], summary)
        atomic_bytes(reports["validation_text"], text.encode())
        atomic_bytes(reports["validation_rdf"], report_graph.serialize(format="turtle", encoding="utf-8"))
    return StageResult(None if dry_run else target, reports, summary)


def run_pipeline(config=None, *, workbook=None, ontology=None, transcript=None, base_individuals=None,
                 intermediate_output=None, output=None, report=None, overwrite=False, dry_run=False, with_inference=None):
    config = configure(config, workbook=workbook, ontology=ontology, transcript=transcript, base_individuals=base_individuals)
    target = output_path(config, output, "current-individuals.rdf")
    intermediate = Path(intermediate_output or config.data["outputs"].get("intermediate_output") or target.with_name("asserted-individuals.rdf")).resolve()
    report = report or config.data["outputs"].get("report")
    # Check ALL destinations before the first successful stage writes anything.
    preflight(config, {"output": target, "intermediate": intermediate,
        "manifest": build_manifest_path(config, intermediate), **report_paths(report)}, overwrite=overwrite)
    if dry_run:
        enabled = config.data["reasoner"].get("enabled", False) if with_inference is None else with_inference
        if enabled:
            raise InputValidationError("Combined --dry-run with inference is not supported; dry-run core with --no-inference or use standalone materialize --dry-run on saved RDF")
        graph, manifest = _build(config)
        _, _, _, summary = _refresh(graph, config)
        if report:
            write_json(report, {**summary, "dry_run": True, "build": manifest["counts"]})
        return StageResult(None, {"report": Path(report)} if report else {}, summary)
    build_config = as_config(config)
    build_config.data["outputs"].pop("report", None)
    built = build_individuals(build_config, output=intermediate, overwrite=overwrite)
    result = run_shacl(built.output_path, output=target, config=config, report=report, overwrite=overwrite)
    enabled = config.data["reasoner"].get("enabled", False) if with_inference is None else with_inference
    result.summary.update({"intermediate_output": str(built.output_path), "inference_enabled": enabled, "inference_status": "skipped"})
    if enabled:
        from .reasoning import materialize
        inferred = materialize(target, config=config, output_directory=target.parent / "inference", overwrite=overwrite)
        result.summary["inference_status"] = "completed"
        result.report_paths.update(inferred.report_paths)
    if report:
        write_json(report, result.summary)
    return result
