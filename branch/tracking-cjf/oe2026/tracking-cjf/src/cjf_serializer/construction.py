"""Annotation-to-RDF construction. No DL transition/classification rules."""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote
import zipfile
import xml.etree.ElementTree as ET
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD, DC
from .adapters import transcript_turns
from .annotations import read_worksheet, parse_turn_ids, split_quotes
from .config import load_profile, read_yaml
from .models import InputValidationError, StateEvent
from .serialization import digest, rdf_format

PROV = Namespace("http://www.w3.org/ns/prov#")
SIO = URIRef("http://semanticscience.org/resource/SIO_000206")
DT = Namespace("https://www.omg.org/spec/Commons/DatesAndTimes/")


def stable(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:20]


def parse_graph(path, format=None):
    path = Path(path).resolve()
    if not path.is_file():
        raise InputValidationError(f"RDF input file does not exist: {path}")
    try:
        return Graph().parse(data=path.read_bytes(), format=rdf_format(path, format), publicID=path.as_uri())
    except Exception as exc:
        raise InputValidationError(f"Cannot read RDF {path}: {exc}") from exc


def numeric_alias(value):
    try:
        number = Decimal(value)
        return str(int(number)) if number.is_finite() and number == number.to_integral() else None
    except (InvalidOperation, ValueError):
        return None


class Builder:
    def __init__(self, config):
        self.config = config
        self.profile = load_profile(config)
        self.schema_path = config.data["ontology"].get("file")
        self.workbook = config.data["inputs"].get("annotations")
        if not self.schema_path or not self.workbook:
            raise InputValidationError("build requires user-supplied ontology and annotation workbook paths")
        self.schema = parse_graph(self.schema_path, config.data["ontology"].get("format"))
        self.ns = Namespace(self.profile["namespace"])
        self.term_map = self.profile.get("terms", {})
        self.graph = Graph()
        self.graph.bind("cjf", self.ns)
        self.graph.bind("prov", PROV)
        conv = config.data["conversation"]
        if not conv.get("id") or not conv.get("key"):
            raise InputValidationError("conversation.id and conversation.key are required")
        self.key = conv["key"]
        self.base = conv.get("base", str(self.ns))
        self.conv = self.iri("Conversation")
        self.ontology_iri = URIRef(conv.get("individuals_iri", self.base + quote(self.key, safe="") + "/individuals"))
        schemas = list(self.schema.subjects(RDF.type, OWL.Ontology))
        if len(schemas) != 1:
            raise InputValidationError("Input schema must declare exactly one owl:Ontology IRI")
        self.schema_iri = schemas[0]
        self.graph.add((self.ontology_iri, RDF.type, OWL.Ontology))
        self.graph.add((self.ontology_iri, OWL.imports, self.schema_iri))
        self.moves, self.turns, self.events = {}, {}, defaultdict(list)
        self.future_moves = set()
        self.manifest = {"schema": str(self.schema_path), "schema_iri": str(self.schema_iri),
                         "schema_sha256": digest(self.schema_path), "workbook": str(self.workbook),
                         "workbook_sha256": digest(self.workbook), "conversation": conv,
                         "events": [], "relationships": [], "moves": [], "turns": [],
                         "inference_enabled": False, "inference_status": "skipped"}
        self.cutoff = config.data["state_events"].get("as_of_turn")
        if self.cutoff is not None and (isinstance(self.cutoff, bool) or not isinstance(self.cutoff, int) or self.cutoff < 1):
            raise InputValidationError("as_of_turn must be null or a positive integer")
        aliases_path = config.data["annotations"].get("column_map")
        self.aliases = read_yaml(aliases_path) if aliases_path else {}
        if set(self.aliases) - {"moves", "relationships", "states", "transcript"}:
            raise InputValidationError("column_map sections must be moves/relationships/states/transcript")
        for section, mapping in self.aliases.items():
            if not isinstance(mapping, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k,v in mapping.items()):
                raise InputValidationError(f"column_map.{section} must map source-header strings to logical-header strings")
            if len(set(mapping.values())) != len(mapping):
                raise InputValidationError(f"column_map.{section} contains duplicate aliases")
        self.datatype = self._turn_datatype()

    def term(self, name):
        value = self.term_map.get(name, name)
        return URIRef(value if "://" in value or value.startswith("urn:") else self.ns[value])

    def require(self, name, cls=False):
        term = self.term(name)
        if not any(self.schema.triples((term, None, None))):
            raise InputValidationError(f"Mapped ontology term is missing: {term}")
        if cls and (term, RDF.type, OWL.Class) not in self.schema and (term, RDF.type, RDFS.Class) not in self.schema:
            raise InputValidationError(f"Mapped class is not declared: {term}")
        return term

    def iri(self, suffix):
        return URIRef(self.base + quote(self.key, safe="") + "/" + quote(str(suffix), safe="_-"))

    def _turn_datatype(self):
        ranges = set(self.schema.objects(self.require("hasTurnNumber"), RDFS.range))
        if len(ranges) != 1 or not ranges <= {XSD.int, XSD.integer, XSD.positiveInteger}:
            raise InputValidationError("hasTurnNumber must have one supported integer datatype range")
        return next(iter(ranges))

    def add(self, subject, predicate, value):
        self.graph.add((subject, self.require(predicate), value))

    def typed(self, iri, kind):
        self.graph.add((iri, RDF.type, self.require(kind, True)))
        return iri

    def sheet(self, logical, required, optional=False):
        name = self.profile["sheets"][logical]
        with zipfile.ZipFile(self.workbook) as book:
            root = ET.fromstring(book.read("xl/workbook.xml"))
            names = {n.get("name").casefold() for n in root.iter() if n.tag.endswith("}sheet")}
        if name.casefold() not in names:
            if optional:
                return []
            raise InputValidationError(f"Missing worksheet {name}")
        aliases = self.aliases.get(logical, {})
        if not isinstance(aliases, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k,v in aliases.items()):
            raise InputValidationError(f"column_map.{logical} must map source headers to logical names")
        rows, routing = read_worksheet(Path(self.workbook), name, required, column_aliases=aliases)
        self.manifest.setdefault("sheets", {})[logical] = routing
        return rows

    def load_turns(self):
        inputs = self.config.data["inputs"]
        sources = [bool(inputs.get(n)) for n in ("transcript", "transcript_sheet", "base_individuals")]
        if sum(sources) != 1:
            raise InputValidationError("Select exactly one transcript, transcript_sheet or base_individuals source")
        self.typed(self.conv, "MultipartyConversation")
        self.add(self.conv, "hasConversationIdentifier", Literal(self.config.data["conversation"]["id"]))
        if inputs.get("base_individuals"):
            existing = parse_graph(inputs["base_individuals"])
            for predicate in ["hasStateAssignment", "hasCurrentStateAssignment"]:
                if any(existing.triples((None, self.term(predicate), None))):
                    raise InputValidationError("base_individuals must be a transcript-only graph without assignment histories/current pointers; use shacl to refresh an existing populated graph")
            # Retain all source assertions, selecting only this conversation's
            # utterances for source reference lookup. Do not guess from IRI suffixes.
            self.graph += existing
            candidates = list(existing.subjects(RDF.type, self.term("Utterance")))
            for utterance in candidates:
                conversations = set(existing.objects(utterance, PROV.wasGeneratedBy))
                if conversations and self.conv not in conversations and not any(
                    str(v) == self.config.data["conversation"]["id"]
                    for c in conversations for v in existing.objects(c, self.term("hasConversationIdentifier"))):
                    continue
                sid = list(existing.objects(utterance, DC.identifier))
                text = list(existing.objects(utterance, self.term("hasConversationText")))
                turn = list(existing.objects(utterance, self.term("hasTurnNumber")))
                speaker = list(existing.objects(utterance, PROV.wasAttributedTo))
                if any(len(v) != 1 for v in [sid, text, turn, speaker]):
                    raise InputValidationError(f"Base utterance needs one dc:identifier/text/turn/speaker: {utterance}")
                if self.cutoff and int(turn[0]) > self.cutoff:
                    raise InputValidationError("For as_of_turn with a base graph, supply an already truncated snapshot; future assertions cannot be safely guessed")
                self._register_turn(str(sid[0]), int(turn[0]), str(text[0]), utterance, speaker[0])
        else:
            turns = transcript_turns(self.config, self.workbook)
            for t in turns:
                # Keep the complete lookup so future annotation references can
                # be recognized and excluded, without emitting future RDF.
                speaker = self.iri("Speaker_" + stable(t.speaker))
                utterance = self.iri("Turn_" + t.source_id)
                self._register_turn(t.source_id, t.sequence, t.text, utterance, speaker)
                if self.cutoff and t.sequence > self.cutoff:
                    continue
                if self.datatype == XSD.int and t.sequence > 2147483647:
                    raise InputValidationError("Turn exceeds xsd:int range")
                speaker = self.typed(self.iri("Speaker_" + stable(t.speaker)), "Speaker")
                self.add(speaker, "hasSpeakerName", Literal(t.speaker))
                utterance = self.typed(self.iri("Turn_" + t.source_id), "Utterance")
                self.add(utterance, "hasConversationText", Literal(t.text))
                self.add(utterance, "hasTurnNumber", Literal(t.sequence, datatype=self.datatype))
                self.graph.add((utterance, DC.identifier, Literal(t.source_id)))
                self.graph.add((utterance, PROV.wasGeneratedBy, self.conv))
                self.graph.add((utterance, PROV.wasAttributedTo, speaker))
                if t.timestamp:
                    dt = self.iri("Time_" + stable(t.timestamp))
                    self.graph.add((dt, RDF.type, DT.DateTime))
                    self.graph.add((dt, RDFS.comment, Literal(t.timestamp)))
                    self.graph.add((utterance, DT.hasDateTime, dt))
                self.manifest["turns"].append({**vars(t), "iri": str(utterance)})
        if not self.turns:
            raise InputValidationError("No utterances for the selected conversation")

    def _register_turn(self, sid, sequence, text, iri, speaker):
        if sid in self.turns or any(t["sequence"] == sequence for t in self.turns.values()):
            raise InputValidationError(f"Duplicate source identifier/sequence: {sid}")
        self.turns[sid] = {"sequence": sequence, "text": text, "iri": iri, "speaker": speaker}

    def lookup(self, value):
        if value in self.turns:
            return value
        alias = numeric_alias(value)
        matches = [sid for sid in self.turns if alias is not None and numeric_alias(sid) == alias]
        if len(matches) != 1:
            raise InputValidationError(f"Unknown or ambiguous source turn: {value}")
        return matches[0]

    def refs(self, value):
        # Existing reference parser preserves fractional source IDs; nonnumeric
        # identifiers are accepted as exact single IDs or semicolon lists.
        if not str(value).strip():
            raise InputValidationError("Evidence/source references must not be empty")
        try:
            values = parse_turn_ids(str(value))
        except ValueError:
            values = [s.strip() for s in str(value).split(";")]
        values = [self.lookup(v) for v in values]
        if len(set(values)) != len(values):
            raise InputValidationError("Repeated references after source-ID normalization")
        return values

    def span(self, source_id, text=None):
        turn = self.turns[source_id]
        text = turn["text"] if text is None else text
        if not text or turn["text"].count(text) != 1:
            raise InputValidationError(f"Evidence quotation is absent or ambiguous in source turn {source_id}")
        span = self.typed(self.iri("Span_" + stable([str(turn["iri"]), text])), "TextSpan")
        self.add(span, "hasConversationText", Literal(text))
        self.add(span, "isPartOfUtterance", turn["iri"])
        return span

    def load_moves(self):
        rows = self.sheet("moves", {"milestone_id", "milestone_type", "summary", "source_turn_id"})
        seen = {}
        for row in rows:
            sid, annotation = row.get("milestone_id", "").strip(), row.get("milestone_type", "").strip()
            semantic_fields = ("milestone_type", "summary", "source_turn_id", "text_span", "utterance", "speaker", "attributes", "attributes (only for Expressed Position and information request)")
            if not any(str(row.get(name, "")).strip() for name in semantic_fields):
                self.manifest.setdefault("skipped_rows", []).append({"sheet": self.profile["sheets"]["moves"], "row": row["excel_row"], "id": sid, "reason": "unannotated placeholder"})
                continue
            logical = {k:v for k,v in row.items() if k != "excel_row"}
            if sid in seen:
                if logical == seen[sid]:
                    continue
                raise InputValidationError(f"Conflicting move rows for {sid}")
            seen[sid] = logical
            kind = self.profile["classes"].get(annotation)
            if not sid or sid in self.moves or not kind or not row.get("summary", "").strip():
                raise InputValidationError(f"Milestones row {row['excel_row']}: duplicate/empty ID, unsupported type or empty summary")
            evidence = self.refs(row["source_turn_id"])
            intro = min(self.turns[x]["sequence"] for x in evidence)
            if self.cutoff and intro > self.cutoff:
                self.future_moves.add(sid)
                continue
            move = self.typed(self.iri("Move_" + sid), kind)
            self.graph.add((move, DC.identifier, Literal(sid)))
            self.add(move, "hasSummary", Literal(row["summary"]))
            quotation = row.get("text_span", "").strip()
            quotes = split_quotes(quotation, evidence) if quotation else {}
            if self.cutoff:
                evidence = [sid for sid in evidence if self.turns[sid]["sequence"] <= self.cutoff]
            attrs = row.get("attributes (only for Expressed Position and information request)", row.get("attributes", ""))
            polarity = re.search(r"positionType\s*=\s*(agreement|disagreement)\b", attrs, re.I)
            predicate = "isPositiveSupportedBy" if polarity and polarity[1].lower() == "agreement" else "isNegativeSupportedBy" if polarity else None
            if polarity and kind != "ExpressedPosition":
                raise InputValidationError("positionType only applies to ExpressedPosition")
            for source_id in evidence:
                turn = self.turns[source_id]
                span = self.span(source_id, quotes.get(source_id))
                self.graph.add((move, self.require(predicate) if predicate else SIO, span))
                self.add(move, "hasUtterance", turn["iri"])
            if row.get("speaker"):
                names = {str(n) for source_id in evidence for n in self.graph.objects(self.turns[source_id]["speaker"], self.term("hasSpeakerName"))}
                if row["speaker"].strip() not in names:
                    raise InputValidationError(f"Milestones row {row['excel_row']}: speaker cross-check failed")
            if row.get("utterance") and len(evidence) == 1 and row["utterance"] != self.turns[evidence[0]]["text"]:
                raise InputValidationError(f"Milestones row {row['excel_row']}: utterance cross-check failed")
            self.moves[sid] = {"iri": move, "kind": kind, "intro": intro}
            self.manifest["moves"].append({"iri": str(move), "row": row})
            initial = self.profile["initial_states"].get(kind)
            if initial:
                self.events[sid].append(StateEvent("initial", sid, intro, "initial", [x for x in evidence if self.turns[x]["sequence"] == intro], [initial], reason="Generated initial assignment from move introduction", order=-1))

    def endpoint(self, node, prop, relation):
        """Validate named/union endpoint classes structurally, never state types."""
        types = set(self.graph.objects(node, RDF.type))
        pending = list(types)
        while pending:
            current = pending.pop()
            for parent in self.schema.objects(current, RDFS.subClassOf):
                if isinstance(parent, URIRef) and parent not in types:
                    types.add(parent); pending.append(parent)
        for constraint in self.schema.objects(prop, relation):
            allowed = {constraint} if isinstance(constraint, URIRef) else set()
            for listing in self.schema.objects(constraint, OWL.unionOf):
                allowed.update(self.schema.items(listing))
            if allowed and not types.intersection(allowed):
                raise InputValidationError(f"Relationship endpoint {node} violates {relation} of {prop}")

    def load_relationships(self):
        rows = self.sheet("relationships", {"from_milestone_id", "relationship", "to_milestone_id", "evidence_turn_ids"}, optional=True)
        # Coalesce declared event rows before constructing records. Additional
        # evidence is not discarded merely because an event ID was seen already.
        grouped = {}
        for row in rows:
            if not row.get("event_id"):
                continue
            key = tuple(row.get(n, "").strip() for n in ["from_milestone_id", "relationship", "to_milestone_id", "event_id"])
            if key not in grouped:
                grouped[key] = row
                continue
            first = grouped[key]
            for name in ["event_order", "effective_turn_id"]:
                if first.get(name, "") != row.get(name, ""):
                    raise InputValidationError(f"Conflicting {name} for declared relationship event {key}")
            first["evidence_turn_ids"] = "; ".join(sorted(set(self.refs(first["evidence_turn_ids"])) | set(self.refs(row["evidence_turn_ids"]))))
            if row.get("reason", "") != first.get("reason", ""):
                first["reason"] += "\n" + row.get("reason", "")
            row["_merged_into"] = first["excel_row"]
        rows = [r for r in rows if "_merged_into" not in r]
        seen = set()
        for row in rows:
            kind, source_id, target_id = (row.get(n, "").strip() for n in ["relationship", "from_milestone_id", "to_milestone_id"])
            mapping = self.profile["relationships"].get(kind)
            if not mapping or source_id not in (self.moves.keys() | self.future_moves) or target_id not in (self.moves.keys() | self.future_moves):
                raise InputValidationError(f"Relationships row {row['excel_row']}: unknown relationship or endpoint")
            evidence = self.refs(row["evidence_turn_ids"])
            latest = max(self.turns[x]["sequence"] for x in evidence)
            effective = self.turns[self.lookup(row["effective_turn_id"])]["sequence"] if row.get("effective_turn_id") else latest
            if self.cutoff and effective > self.cutoff:
                continue
            if source_id in self.future_moves or target_id in self.future_moves:
                raise InputValidationError("Relationship occurs before an endpoint is introduced")
            if latest > effective or effective < max(self.moves[source_id]["intro"], self.moves[target_id]["intro"]):
                raise InputValidationError(f"Relationships row {row['excel_row']}: evidence/endpoint occurs after effective event")
            event_id = row.get("event_id") or stable([source_id, kind, target_id, sorted(evidence), effective])
            identity = (source_id, kind, target_id, event_id)
            if identity in seen:
                continue
            seen.add(identity)
            source, target = self.moves[source_id]["iri"], self.moves[target_id]["iri"]
            reason = row.get("reason", "").strip()
            if not reason:
                raise InputValidationError(f"Relationships row {row['excel_row']}: reason required")
            relationship = None
            if mapping.get("property"):
                prop = self.require(mapping["property"])
                self.endpoint(source, prop, RDFS.domain); self.endpoint(target, prop, RDFS.range)
                if mapping.get("same_type") and self.moves[source_id]["kind"] != self.moves[target_id]["kind"]:
                    raise InputValidationError("refines requires moves of the same type")
                self.graph.add((source, prop, target))
            else:
                relationship = self.typed(self.iri("Relationship_" + stable(identity)), mapping["class"])
                makes, aim = self.require(mapping["makes"]), self.require(mapping["target"])
                self.endpoint(source, makes, RDFS.domain); self.endpoint(target, aim, RDFS.range)
                self.graph.add((source, makes, relationship)); self.graph.add((relationship, aim, target))
                self.add(relationship, "hasReason", Literal(reason))
                for sid in evidence:
                    self.graph.add((relationship, SIO, self.span(sid)))
                    self.add(relationship, "hasUtterance", self.turns[sid]["iri"])
            record = {"id": event_id, "kind": kind, "source": source_id, "target": target_id, "evidence": evidence, "effective_turn": effective, "reason": reason, "row": row}
            self.manifest["relationships"].append(record)
            # event_targets is a structural target-class mapping. There is no
            # predecessor-state test, predicted-state ledger, or DL rule here.
            if self.moves[target_id]["kind"] in mapping.get("event_targets", []):
                if target_id not in self.events:
                    raise InputValidationError("Relationship assignment target lacks an initial mapping")
                # An explicit turn-snapshot policy groups unordered relationship
                # records by their owner and establishing utterance. It does not
                # predict a state, choose a predecessor type, or invent an order.
                group_turn = self.config.data["state_events"].get("same_turn_relationships", "reject") == "group_by_target_turn"
                grouped_turn = group_turn and not row.get("event_id") and self.order(row) is None
                key = "relationship:turn:" + str(effective) if grouped_turn else "relationship:" + event_id
                event = next((e for e in self.events[target_id] if e.event_id == key), None)
                if event is None:
                    event = StateEvent(key, target_id, effective, "relationship", evidence, reason="Generated candidate from relationship event: " + reason, order=self.order(row), raw=dict(row))
                    self.events[target_id].append(event)
                elif event.turn != effective or event.order != self.order(row):
                    raise InputValidationError("Joint relationship event has conflicting time/order")
                if grouped_turn:
                    prior_rows = event.raw.setdefault("grouped_relationship_rows", [])
                    if not prior_rows:
                        event.raw = {"grouping": "target_and_effective_turn", "grouped_relationship_rows": []}
                    event.raw["grouped_relationship_rows"].append(dict(row))
                    explanation = "Generated candidate from relationship event: " + reason
                    if explanation not in event.reason.split("\n"):
                        event.reason += "\n" + explanation
                event.evidence = sorted(set(event.evidence) | set(evidence))
                if relationship:
                    event.triggers.append(str(relationship))

    @staticmethod
    def order(row):
        if str(row.get("event_order", "")).strip():
            try:
                value = int(row["event_order"])
            except ValueError as exc:
                raise InputValidationError("event_order must be a nonnegative integer") from exc
            if value < 0:
                raise InputValidationError("event_order must be nonnegative")
            return value
        return None

    def load_human_states(self):
        mode = self.config.data["annotations"].get("states_sheet", "optional")
        rows = [] if mode == "absent" else self.sheet("states", {"milestone_id", "state", "effective_turn_id", "evidence_turn_ids", "reason"}, optional=mode == "optional")
        seen = {}
        for row in rows:
            owner = row["milestone_id"].strip()
            effective = self.turns[self.lookup(row["effective_turn_id"])]["sequence"]
            if self.cutoff and effective > self.cutoff:
                continue
            if owner not in self.events:
                raise InputValidationError(f"States row {row['excel_row']}: owner has no initial state mapping")
            if row.get("assignment_mode", "explicit").strip() not in {"", "explicit"}:
                raise InputValidationError("States rows are explicit human transitions only; filter legacy initial/relationship rows first")
            states = [s.strip().replace(" ", "") for s in row["state"].split(";")]
            if not states or any(s not in self.profile["state_classes"] for s in states):
                raise InputValidationError(f"States row {row['excel_row']}: unknown state label")
            effective = self.turns[self.lookup(row["effective_turn_id"])]["sequence"]
            evidence = self.refs(row["evidence_turn_ids"])
            if effective < self.moves[owner]["intro"] or any(self.turns[s]["sequence"] > effective for s in evidence):
                raise InputValidationError(f"States row {row['excel_row']}: future evidence or transition before introduction")
            if not row["reason"].strip():
                raise InputValidationError("Human transitions require a reason")
            event_id = "human:" + (row.get("event_id") or stable([owner, effective, sorted(evidence), states, row["reason"]]))
            identity = (owner, event_id)
            content = (effective, tuple(sorted(evidence)), tuple(sorted(states)), row["reason"], self.order(row))
            if identity in seen:
                if seen[identity] != content:
                    raise InputValidationError(f"Conflicting human state event {event_id} for {owner}")
                continue
            seen[identity] = content
            self.events[owner].append(StateEvent(event_id, owner, effective, "explicit-human", evidence, states, reason=row["reason"], order=self.order(row), raw=row))

    def assignments(self):
        by_sequence = {t["sequence"]: t for t in self.turns.values()}
        for owner, events in self.events.items():
            groups = defaultdict(list)
            for event in events:
                if event.origin != "initial":
                    groups[event.turn].append(event)
            for turn, same in groups.items():
                if len(same) > 1 and (any(e.order is None for e in same) or len({e.order for e in same}) != len(same)):
                    raise InputValidationError(f"Move {owner}, turn {turn}: separate same-turn events require unique event_order")
            events.sort(key=lambda e: (e.turn, -1 if e.origin == "initial" else e.order if e.order is not None else 0))
            previous = None
            for event in events:
                assignment = self.typed(self.iri("Assignment_" + stable([owner, event.event_id])), "StateAssignment")
                state = self.typed(self.iri("State_" + stable([owner, event.event_id])), "State")
                for kind in event.state_types:
                    self.typed(state, kind)
                self.add(self.moves[owner]["iri"], "hasStateAssignment", assignment)
                self.add(assignment, "assignedState", state)
                self.add(assignment, "assignedAtUtterance", by_sequence[event.turn]["iri"])
                self.add(assignment, "hasReason", Literal(event.reason))
                for sid in event.evidence:
                    self.add(assignment, "hasStateEvidence", self.span(sid))
                for trigger in sorted(set(event.triggers)):
                    self.add(assignment, "hasTriggeringRelationship", URIRef(trigger))
                if previous:
                    self.add(assignment, "hasPreviousAssignment", previous)
                previous = assignment
                self.manifest["events"].append({**vars(event), "assignment": str(assignment), "state": str(state)})

    def build(self):
        self.load_turns(); self.load_moves(); self.load_relationships(); self.load_human_states(); self.assignments()
        available = {sid: t for sid,t in self.turns.items() if not self.cutoff or t["sequence"] <= self.cutoff}
        self.manifest["source_id_to_iri"] = {sid: str(t["iri"]) for sid,t in available.items()}
        self.manifest["as_of_turn"] = self.cutoff
        self.manifest["turn_datatype"] = str(self.datatype)
        self.manifest["counts"] = {"turns": len(available), "moves": len(self.moves), "assignments": len(self.manifest["events"]), "triples": len(self.graph)}
        return self.graph, self.manifest
