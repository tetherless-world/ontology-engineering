"""Legacy executable paths delegate to the shared package, never old defaults."""
import sys
from .cli import main as cli_main


def main(stage):
    print("Legacy script entry point: use cjf-serialize " + stage +
          ". Partial imports are retired; build converts the complete configured workbook. "
          "Pass package options (--config/--workbook/--ontology/--output); use --help.", file=sys.stderr)
    return cli_main([stage, *sys.argv[1:]])
