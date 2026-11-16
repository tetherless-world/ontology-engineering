#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import sys
import tempfile

try:
    from pyshacl import validate
    from rdflib import Graph, Namespace, RDF
except ImportError:
    raise SystemExit(
        "Missing dependencies. Run: python -m pip install -r "
        + str(Path(__file__).with_name("requirements-shacl.txt"))
    )

HERE = Path(__file__).resolve().parent
V = Namespace(
    "https://tw.rpi.edu/ontology-engineering/oe2026/"
    "ventilation-compliance/"
)


def assess(data, shapes):
    """Apply SHACL-AF rules in place; return the validation result and report."""
    if not any(data.subjects(RDF.type, V.PolicyAssessment)):
        raise ValueError(
            "No explicit v:PolicyAssessment instances found. Check the data namespace "
            "and types; this script does not run OWL/SWRL inference."
        )
    return validate(
        data_graph=data,
        shacl_graph=shapes,
        advanced=True,
        iterate_rules=True,
        inplace=True,
        inference="none",
        do_owl_imports=False,
        allow_warnings=True,
    )


def save_rdf(data, destination):
    """Finish serialization before atomically replacing the destination."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=destination.parent, suffix=".rdf", delete=False
        ) as stream:
            temporary = Path(stream.name)
            data.serialize(destination=stream, format="xml", encoding="utf-8")
        if destination.exists():
            temporary.chmod(destination.stat().st_mode & 0o777)
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", nargs="?", type=Path,
        help="RDF/XML input file (alternative to --input-path)",
    )
    parser.add_argument(
        "--input-path", type=Path,
        help="RDF/XML input file path; relative paths use the working directory",
    )
    parser.add_argument(
        "--shapes", type=Path, default=HERE / "unknown-policy-assessment.ttl",
        help="SHACL rules in Turtle",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--output-path", type=Path, help="destination RDF/XML file path")
    output.add_argument("-o", "--output", type=Path, help="destination RDF/XML file")
    output.add_argument("--in-place", action="store_true", help="overwrite the input file")
    args = parser.parse_args(argv)
    if args.input_path is not None and args.input is not None:
        parser.error("use either positional input or --input-path, not both")
    source = args.input_path or args.input or HERE / "ventilation-compliance-individuals.rdf"
    if args.in_place:
        destination = source
    else:
        destination = args.output_path or args.output or source.with_name(source.stem + "-assessed.rdf")
    try:
        if not source.is_file():
            raise ValueError(f"Input path must be an existing RDF/XML file: {source}")
        if destination.is_dir():
            raise ValueError(f"Output path must be a file, not a directory: {destination}")
        data = Graph().parse(source, format="xml")
        shapes = Graph().parse(args.shapes, format="turtle")
        before = set(data)
        conforms, _, report_text = assess(data, shapes)
        print(report_text)
        if not conforms:
            print("Validation failed; output was not written.", file=sys.stderr)
            return 1
        destination.parent.mkdir(parents=True, exist_ok=True)
        save_rdf(data, destination)
        added = set(data) - before
        print(f"Added {len(added)} triples. Saved RDF/XML to {destination}")
        for subject, predicate, obj in sorted(added):
            print(f"  {subject.n3()} {predicate.n3()} {obj.n3()} .")
        return 0
    except Exception as exc:
        print(f"Assessment failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
