"""Public file-based CJF annotation pipeline."""
from .config import Config, load_config
from .models import InputValidationError, OutputWriteError, ShaclValidationError, StageResult
from .pipeline import build_individuals, run_pipeline, run_shacl, validate_inputs


def materialize(*args, **kwargs):
    """Load optional inference support only on explicit invocation."""
    from .reasoning import materialize as execute
    return execute(*args, **kwargs)


__all__ = ["Config", "load_config", "build_individuals", "run_shacl", "run_pipeline", "validate_inputs", "materialize",
           "InputValidationError", "OutputWriteError", "ShaclValidationError", "StageResult"]
