"""Validated configuration with explicit paths and portable package resources."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
import yaml
from .models import ConfigurationError as InputValidationError

SECTIONS = {
    "conversation": {"id", "key", "individuals_iri", "base"},
    "inputs": {"annotations", "transcript", "transcript_sheet", "base_individuals", "adapter", "continuation_lines", "date", "timezone"},
    "ontology": {"file", "profile", "format", "import_map"},
    "annotations": {"column_map", "states_sheet"},
    "state_events": {"event_mapping", "evidence_policy", "as_of_turn", "same_turn_relationships"},
    "validation": {"shapes"},
    "reasoner": {"enabled", "engine", "runtime"},
    "outputs": {"directory", "output", "intermediate_output", "report", "artifacts_directory"},
}
PATH_KEYS = {("inputs", "annotations"), ("inputs", "transcript"), ("inputs", "base_individuals"),
             ("ontology", "file"), ("ontology", "import_map"), ("annotations", "column_map"),
             ("state_events", "event_mapping"), ("validation", "shapes"),
             ("outputs", "artifacts_directory"), ("outputs", "directory"), ("outputs", "output"), ("outputs", "intermediate_output"), ("outputs", "report")}


def read_yaml(path):
    try:
        value = yaml.safe_load(Path(path).read_text(encoding="utf-8-sig")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise InputValidationError(f"Configuration {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InputValidationError(f"Expected a mapping in {path}")
    return value


@dataclass
class Config:
    data: dict = field(default_factory=dict)
    path: Path | None = None

    @property
    def shapes(self):
        return self.data.get("validation", {}).get("shapes")


def load_config(path=None, *, ontology_path=None):
    source = Path(path).resolve() if path else None
    data = read_yaml(source) if source else {}
    for key in data:
        if key not in SECTIONS and key != "config_version":
            raise InputValidationError(f"Unknown configuration section: {key}")
    if data.get("config_version", 1) != 1:
        raise InputValidationError("Unsupported config_version")
    for section, allowed in SECTIONS.items():
        values = data.setdefault(section, {})
        if not isinstance(values, dict) or set(values) - allowed:
            raise InputValidationError(f"Unknown or malformed {section} configuration: {set(values) - allowed if isinstance(values, dict) else values}")
    base = source.parent if source else Path.cwd()
    for section, key in PATH_KEYS:
        value = data[section].get(key)
        if value is not None:
            data[section][key] = (base / str(value)).resolve()
    profile = data["ontology"].get("profile")
    if profile and profile != "cjf":
        data["ontology"]["profile"] = (base / str(profile)).resolve()
    runtime = data["reasoner"].get("runtime")
    if runtime:
        # Merely resolving a path does not load/check the optional runtime.
        data["reasoner"]["runtime"] = (base / str(runtime)).resolve()
    if ontology_path is not None:
        data["ontology"]["file"] = Path(ontology_path).resolve()
    if not isinstance(data["reasoner"].get("enabled", False), bool):
        raise InputValidationError("reasoner.enabled must be true or false")
    if data["state_events"].get("evidence_policy", "full_utterance") != "full_utterance":
        raise InputValidationError("Only full_utterance relationship/state evidence is supported")
    if data["annotations"].get("states_sheet", "optional") not in {"optional", "required", "absent"}:
        raise InputValidationError("states_sheet must be optional, required, or absent")
    if data["state_events"].get("same_turn_relationships", "reject") not in {"reject", "group_by_target_turn"}:
        raise InputValidationError("same_turn_relationships must be reject or group_by_target_turn")
    cutoff = data["state_events"].get("as_of_turn")
    if cutoff is not None and (isinstance(cutoff, bool) or not isinstance(cutoff, int) or cutoff < 1):
        raise InputValidationError("as_of_turn must be null or a positive integer")
    if data["inputs"].get("continuation_lines", "reject") not in {"reject", "append"}:
        raise InputValidationError("continuation_lines must be reject or append")
    return Config(data, source)


def as_config(config=None):
    if isinstance(config, Config):
        return Config(deepcopy(config.data), config.path)
    return load_config(config)


def load_profile(config):
    default = yaml.safe_load(files("cjf_serializer").joinpath("resources/profiles/cjf.yaml").read_text())
    selected = config.data["ontology"].get("profile")
    if selected and selected != "cjf":
        override = read_yaml(selected)
        if set(override) - set(default):
            raise InputValidationError(f"Unknown profile keys: {set(override) - set(default)}")
        for key, value in override.items():
            if isinstance(default.get(key), dict) and isinstance(value, dict):
                default[key].update(value)
            else:
                default[key] = value
    for key in ["classes", "initial_states", "terms", "sheets", "relationships"]:
        if not isinstance(default[key], dict):
            raise InputValidationError(f"Profile {key} must be a mapping")
    event_file = config.data["state_events"].get("event_mapping")
    if event_file:
        mappings = read_yaml(event_file)
        for kind, targets in mappings.items():
            if kind not in default["relationships"] or not isinstance(targets, list):
                raise InputValidationError("Event mapping must map known relationships to target-class lists; no DL rules")
            default["relationships"][kind]["event_targets"] = targets
    for kind, mapping in default["relationships"].items():
        if not isinstance(mapping, dict) or set(mapping) - {"class", "makes", "target", "property", "event_targets", "same_type"}:
            raise InputValidationError(f"Unsupported relationship mapping {kind}; DL rules are not supported")
        if not isinstance(mapping.get("event_targets", []), list):
            raise InputValidationError(f"event_targets for {kind} must be a list of target class names")
    if not isinstance(default["state_classes"], list) or not isinstance(default["namespace"], str):
        raise InputValidationError("Profile state_classes/namespace are malformed")
    for key in ["classes", "initial_states", "terms", "sheets"]:
        if any(not isinstance(k, str) or not isinstance(v, str) for k,v in default[key].items()):
            raise InputValidationError(f"Profile {key} must map strings to strings")
    return default
