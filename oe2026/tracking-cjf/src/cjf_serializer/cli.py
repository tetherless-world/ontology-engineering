"""Console and python -m entry points use the same public file API."""
import argparse
import json
import sys
from . import load_config, build_individuals, run_shacl, run_pipeline, validate_inputs, materialize
from .models import InputValidationError, ShaclValidationError, ConfigurationError


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cjf-serialize", description="Excel annotations -> RDF file -> SHACL -> current RDF file")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ["validate-input", "build", "shacl", "run", "materialize"]:
        sub = commands.add_parser(name)
        sub.add_argument("--config")
        sub.add_argument("--ontology")
        sub.add_argument("--overwrite", action="store_true")
        sub.add_argument("--dry-run", action="store_true")
        if name != "materialize":
            sub.add_argument("--report")
        if name in {"validate-input", "build", "run"}:
            sub.add_argument("--workbook")
            source = sub.add_mutually_exclusive_group()
            source.add_argument("--transcript")
            source.add_argument("--base-individuals")
        if name in {"build", "shacl", "run"}:
            sub.add_argument("--output")
        if name in {"shacl", "materialize"}:
            sub.add_argument("--individuals", required=True)
        if name == "shacl":
            sub.add_argument("--shapes")
        if name == "run":
            sub.add_argument("--intermediate-output")
            inference = sub.add_mutually_exclusive_group()
            inference.add_argument("--with-inference", dest="with_inference", action="store_true")
            inference.add_argument("--no-inference", dest="with_inference", action="store_false")
            sub.set_defaults(with_inference=None)
        if name == "materialize":
            sub.add_argument("--output-directory", required=True)
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        config = load_config(args.pop("config"), ontology_path=args.pop("ontology"))
        if command == "validate-input":
            args.pop("dry_run")
            result = validate_inputs(config, **args)
        else:
            function = {"build": build_individuals, "shacl": run_shacl, "run": run_pipeline, "materialize": materialize}[command]
            result = function(config=config, **args)
        print(json.dumps({"output": str(result.output_path) if result.output_path else None, "reports": result.report_paths, "summary": result.summary}, default=str, ensure_ascii=False))
        return 0
    except ConfigurationError as exc:
        print(f"Configuration: {exc}", file=sys.stderr); return 2
    except ShaclValidationError as exc:
        print(f"SHACL: {exc}", file=sys.stderr); return 1
    except InputValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr); return 1
    except (OSError, ImportError, ValueError, TypeError) as exc:
        print(f"Configuration/runtime/output error: {exc}", file=sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
