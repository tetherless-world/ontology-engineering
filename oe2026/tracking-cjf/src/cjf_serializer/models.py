"""Public file results and normalized source records."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class InputValidationError(ValueError):
    pass


class OutputWriteError(OSError):
    pass


class ConfigurationError(InputValidationError):
    pass


class ShaclValidationError(InputValidationError):
    def __init__(self, text, report_graph=None):
        super().__init__(text)
        self.report_text = text
        self.report_graph = report_graph


@dataclass
class StageResult:
    output_path: Path | None
    report_paths: dict[str, Path] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class Turn:
    source_id: str
    sequence: int
    speaker: str
    text: str
    timestamp: str = ""
    provenance: dict = field(default_factory=dict)


@dataclass
class Move:
    source_id: str
    kind: str
    turn_ids: list[str]
    raw: dict


@dataclass
class RelationshipEvent:
    event_id: str
    source: str
    target: str
    kind: str
    evidence: list[str]
    turn: int
    raw: dict


@dataclass
class StateEvent:
    event_id: str
    owner: str
    turn: int
    origin: str
    evidence: list[str]
    state_types: list[str] = field(default_factory=list)
    triggers: list[str] = field(default_factory=list)
    reason: str = ""
    order: int | None = None
    raw: dict = field(default_factory=dict)


@dataclass
class EvidenceSpan:
    utterance: str
    text: str
    start: int
    end: int
