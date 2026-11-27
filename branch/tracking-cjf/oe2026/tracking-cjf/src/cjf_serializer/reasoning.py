"""Optional external HermiT/OWLAPI worker integration; never imported by core stages."""
from __future__ import annotations
from pathlib import Path
import json
import subprocess
import tempfile
from .config import as_config, read_yaml
from .construction import parse_graph
from .models import InputValidationError, StageResult
from .pipeline import input_paths, preflight, run_shacl
from .serialization import save_graph, write_json, atomic_bytes, digest


def materialize(individuals, *, config=None, output_directory=None, overwrite=False, dry_run=False):
    """Explicit opt-in to a configured worker implementing the documented protocol.

    The worker owns Java/OWLAPI/HermiT and inferred-axiom generation. This adapter
    does not claim RDFLib or OWL-RL provides HermiT reasoning.
    """
    config = as_config(config)
    schema = config.data["ontology"].get("file")
    runtime = config.data["reasoner"].get("runtime")
    if not schema or not runtime:
        raise InputValidationError("Optional HermiT requires ontology.file and reasoner.runtime; core commands do not require these runtime settings")
    if config.data["reasoner"].get("engine", "hermit") != "hermit":
        raise InputValidationError("Only the explicit HermiT worker protocol is supported")
    settings = read_yaml(runtime)
    if set(settings) - {"command", "timeout_seconds", "heap_mb"}:
        raise InputValidationError("Unknown HermiT runtime setting")
    command = settings.get("command")
    if not isinstance(command, list) or not command or any(not isinstance(v, str) for v in command):
        raise InputValidationError("HermiT runtime.command must be a nonempty argument list, never a shell string")
    timeout = settings.get("timeout_seconds", 120)
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise InputValidationError("timeout_seconds must be positive")
    output_dir = Path(output_directory or config.data["outputs"].get("directory", Path(individuals).parent) / "inference").resolve()
    paths = preflight(config, {"inferred": output_dir / "inferred.ttl", "materialized": output_dir / "materialized.ttl",
        "reasoning_log": output_dir / "reasoning.log", "report": output_dir / "reasoning-report.json"}, inputs=[individuals, runtime], overwrite=overwrite)
    # Refresh/validate a temporary copy before passing it to the optional worker.
    # Sources and published core output are never changed by optional inference.
    with tempfile.TemporaryDirectory(prefix="cjf-hermit-", dir=output_dir.parent if output_dir.parent.exists() else None) as directory:
        temp = Path(directory)
        current = temp / "current.rdf"
        validation_config = as_config(config)
        validation_config.data["outputs"].pop("report", None)
        run_shacl(individuals, output=current, config=validation_config)
        imports = {}
        if config.data["ontology"].get("import_map"):
            mapping_path = config.data["ontology"]["import_map"]
            imports = {iri: str((mapping_path.parent / str(path)).resolve()) for iri,path in read_yaml(mapping_path).items()}
        for iri, path in imports.items():
            if not Path(path).is_file():
                raise InputValidationError(f"Missing local ontology import {iri}: {path}")
        request = {"protocol_version": 1, "engine": "HermiT", "individuals": str(current), "ontology": str(schema),
            "imports": imports, "inferred_output": str(temp / "inferred.ttl"), "result_output": str(temp / "result.json"),
            "assertion_kinds": ["named_class", "object_property", "data_property"], "heap_mb": settings.get("heap_mb", 2048)}
        request_path = temp / "request.json"
        write_json(request_path, request)
        if dry_run:
            return StageResult(None, {}, {"stage": "materialize", "dry_run": True, "worker_not_started": True})
        arguments = [v.replace("{request}", str(request_path)) for v in command]
        if not any("{request}" in v for v in command):
            arguments.append(str(request_path))
        try:
            completed = subprocess.run(arguments, cwd=Path(runtime).parent, capture_output=True, text=True, timeout=timeout, shell=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise InputValidationError(f"HermiT worker failed; core RDF preserved: {exc}") from exc
        if completed.returncode:
            raise InputValidationError(f"HermiT worker exit {completed.returncode}; core RDF preserved: {completed.stderr[-2000:]}")
        try:
            result = json.loads((temp / "result.json").read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise InputValidationError("HermiT worker did not produce its protocol result") from exc
        if result.get("engine") != "HermiT" or result.get("consistent") is not True or result.get("materialized") is not True:
            raise InputValidationError("Worker must confirm HermiT, consistency and explicit assertion materialization")
        inferred = parse_graph(temp / "inferred.ttl")
        asserted = parse_graph(current)
        # Export only genuinely new selected triples, preserving the core graph.
        new = inferred - asserted
        combined = asserted + new
        summary = {"stage": "materialize", "engine": "HermiT", "inference_status": "completed",
            "new_triples": len(new), "schema_sha256": digest(schema), "imports_sha256": {iri: digest(path) for iri,path in imports.items()}, "worker_result": result}
        save_graph(new, paths["inferred"]); save_graph(combined, paths["materialized"])
        atomic_bytes(paths["reasoning_log"], (completed.stdout + "\n" + completed.stderr).encode())
        write_json(paths["report"], summary)
        return StageResult(paths["materialized"], paths, summary)
