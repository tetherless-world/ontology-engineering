# Human annotations to RDF

The installable `cjf-serializer` package implements the file-based core workflow:

```text
human-reviewed XLSX + supplied ontology + transcript source
    -> build -> asserted-individuals.rdf
    -> shacl -> current-individuals.rdf
```

Each public stage writes its output and returns its path and reports. `run`
calls those same stages and retains the asserted file. Failed SHACL validation
does not replace a previous final RDF. The asserted file remains available for
inspection in Protégé or a later standalone SHACL run.

## Install and run

Python 3.10+ is required. From the `oe2026/tracking-cjf` project folder:

```powershell
# From the repository root, first run: cd oe2026/tracking-cjf
python -m pip install .
cjf-serialize --help
cjf-serialize validate-input --config configs/example.yaml
cjf-serialize build --config configs/example.yaml --output outputs/asserted.rdf
cjf-serialize shacl --config configs/example.yaml --individuals outputs/asserted.rdf --output outputs/current.rdf --report outputs/shacl.json
cjf-serialize run --config configs/example.yaml --intermediate-output outputs/asserted.rdf --output outputs/current.rdf
```

`python -m cjf_serializer` is an equivalent entry point. Configuration paths are
relative to the config file; CLI paths are relative to the invoking directory.
Use `--ontology path/to/any-name.rdf` to override `ontology.file`. No ontology
release filename is required. `.rdf/.owl/.xml`, `.ttl`, `.nt`, and `.jsonld` are
recognized; `ontology.format` can identify the format of another filename.
The ontology must declare one ontology IRI and the terms used by its profile.
The package records the input hash and imports the declared ontology IRI.

Specify `--overwrite` to replace existing outputs. Inputs cannot be outputs.
`--dry-run` computes and validates without publishing RDF or backups; explicitly
requested diagnostic reports may be written. `--report PATH` writes JSON and,
for SHACL, `PATH.shacl.txt` and `PATH.shacl.ttl`. Build writes a manifest beside
the RDF as `<output>.manifest.json` by default. Set
`outputs.artifacts_directory` to put build manifests in a separate folder,
including when using the combined command. For example,
`artifacts_directory: ../ontology/run_outputs` in a config under `configs/`.
Use `--report ontology/run_outputs/<stage>-report.json` for stage reports. Path collisions are rejected before the
first pipeline stage writes. Input hashes are rechecked before publication to
detect concurrent edits during conversion.

Configuration failures return CLI status 2; input nonconformance returns 1;
successful commands return 0. Public exceptions include `InputValidationError`,
`ShaclValidationError` (with its report), and `OutputWriteError`.

## Library interface

```python
from cjf_serializer import load_config, build_individuals, run_shacl, run_pipeline

config = load_config("configs/example.yaml", ontology_path="ontology/my-ontology.rdf")
built = build_individuals(config, output="outputs/asserted.rdf")
current = run_shacl(built.output_path, config=config, output="outputs/current.rdf")

# Or execute both file-writing stages:
result = run_pipeline(config, intermediate_output="outputs/asserted.rdf",
                      output="outputs/current.rdf", overwrite=True)
```

Results contain `output_path`, `report_paths`, and `summary`. Callers do not pass
RDFLib graphs or call a separate save operation. Explicit path arguments override
config values. The internal RDF/XML and graph helpers are implementation details.

## Inputs and mapping

Supply exactly one transcript source:

- `inputs.transcript_sheet`: an XLSX sheet with `source_turn_id`, `sequence`,
  `speaker`, and `utterance`; optional `end_time`.
- `inputs.transcript` and an explicit adapter: `numbered_speakers`, `corpus_chat`,
  or `dialogue_xml`. Numbered Markdown and the corpus's legacy `19:48:41 PM`
  timestamps are supported. `continuation_lines` is `reject` by default or `append`.
- `inputs.base_individuals`: a transcript-only RDF graph with utterance types,
  source `dc:identifier`, turn numbers, text, and speaker attribution. Graphs
  containing state histories/current pointers are rejected; use `shacl` to
  refresh populated graphs. Base utterances are selected by conversation identity.

Missing speakers/utterances are never synthesized from move summaries. Times
are recorded only when supplied; missing dates/timezones are never invented.
Numeric source references have unambiguous integer aliases (`1` and `1.0`);
fractional IDs such as `117.1` remain distinct. Canonical sequence is separate.

Required worksheets/headers:

| Sheet | Required columns |
| --- | --- |
| Milestones | milestone_id, milestone_type, summary, source_turn_id |
| Relationships (optional if no relationships) | from_milestone_id, relationship, to_milestone_id, evidence_turn_ids, reason for populated rows |
| States (optional) | milestone_id, state, effective_turn_id, evidence_turn_ids, reason |

Headers are trimmed, blank rows ignored, and formula cells rejected. Preallocated
move rows containing only an ID (with no type, summary, references, text, speaker
or attributes) are skipped and recorded in manifest `skipped_rows`. Partially
annotated rows still fail rather than being silently dropped. Unknown
types and relationships, conflicting IDs, missing references, and ambiguous
quoted evidence fail explicitly. Optional `text_span` narrows move evidence;
relationship/state evidence uses complete utterances. Optional speaker/utterance
columns cross-check against the transcript. Explicit `positionType=agreement`
or `disagreement` selects polarity evidence predicates; it is never inferred
from wording. Summary and reason use `hasSummary` and `hasReason`.

The packaged `cjf` profile supplies class aliases, typed initial states,
direct/reified relationship serialization, and structural relationship-event
targets. A custom YAML profile may override namespace, terms, class mappings,
initial mappings, state classes, sheets, and relationships. `terms` maps logical
names to local names or full IRIs. Changed namespaces/term maps require explicitly
supplied compatible shapes, including their embedded SPARQL; the package does
not pretend a URI-only rewrite updates SPARQL logic.

`annotations.column_map` names a YAML file whose sections are `moves`,
`relationships`, `states`, and `transcript`, each mapping source headers to
logical headers. Example: `moves: {move_id: milestone_id}`. Duplicate aliases
and unknown config keys are rejected.

## Three sources of assignment records

1. **Starter states:** Python creates a distinct initial assignment and typed
   State from the configured move-to-initial mapping. No States row is required.
2. **Relationship events:** Python creates distinct generic `State` records,
   assignments, relationship triggers, evidence, and chronology. No States row
   is used and no specific resulting state is predicted or asserted.
3. **States worksheet:** Python imports explicitly typed, human-evidenced
   transitions. It is not a source of starters or expected inferred labels.

There are no Python DL rules, predecessor-state tests, or expected-state ledger.
The structural default event mapping targets Issue for addresses/resolves,
InformationRequest for answers, Claim for supports/challenges, and Option for
direct selects. Other relationships create no candidate assignment by default.
This maps event ownership only; it does not evaluate a state transition.
`state_events.event_mapping` may name a YAML mapping from relationship names to
target-class lists. It cannot contain predecessor conditions or resulting types.

`state_events.same_turn_relationships` defaults to `reject`, requiring explicit
ordering for separate same-turn events. Set it to `group_by_target_turn` when the
annotation unit is a target move's turn snapshot: relationship rows without an
explicit `event_id` or `event_order` then share one generic candidate assignment
per target and effective utterance, retaining all triggers, evidence, reasons,
and source rows. This does not assert any resulting state type or invent an
intra-turn order. Explicit IDs/orders and human States rows remain distinct.
The CQ sample config opts into this policy because its workbook has no event
ordering controls. Support plus Challenge and Address plus Resolve remain
relationship evidence attached to generic States; Python does not classify them.

Effective relationship time defaults to its latest evidence turn. Optional
`effective_turn_id`, `event_id`, and `event_order` resolve other cases. Repeated
rows for a declared relationship event merge evidence. Distinct same-turn events
require unique nonnegative `event_order`; an initial assignment always precedes
successors at the same turn. Shared event IDs can group joint triggers. Human
events remain separate from relationship candidates. Every assignment owns its
own State and links to its immediate predecessor. State classes may remain
generic in the normal output; classification belongs to ontology DL axioms.

Direct `selects` is serialized directly, never fabricated as a Resolve. Direct
edge evidence remains in the manifest where the ontology lacks a reified class.
Stable IDs use conversation/event identity, not Excel row position.

## Minimal SHACL execution

The stage reads the individuals file, clears existing current pointers in
memory for moves with histories, calls pySHACL once, and writes only after
conformance. Rules derive current pointers; shapes validate ownership,
cardinality, effective turns, cycles, and chronology. Python does not independently
traverse histories, compare a second derived endpoint, inspect rule scope, or
rerun the pipeline to prove repeatability. Tests cover these properties instead.

The supplied ontology is not imported into SHACL and no OWL inference is run.
The packaged shape template aligns its integer datatype to the schema's declared
turn range (or the actual unambiguous datatype in standalone mode). Supplied
custom shapes are not modified. The source shapes and schema are unchanged.

## Optional HermiT worker

Inference is off by default and requires no Java for the core workflow.

```powershell
cjf-serialize materialize --config configs/example.yaml --individuals outputs/current.rdf --output-directory outputs/inference
cjf-serialize run --config configs/example.yaml --output outputs/current.rdf --with-inference
```

`--no-inference` overrides a configuration opt-in. Merely specifying a runtime
path does not enable inference. The library equivalent is `materialize(...)` or
`run_pipeline(..., with_inference=True)`.

This package provides a tested external worker adapter, **not a bundled Java
HermiT/OWLAPI worker**. Supply that integration and runtime YAML explicitly:

```yaml
command: [java, -jar, /absolute/path/cjf-hermit-worker.jar, "{request}"]
timeout_seconds: 120
heap_mb: 2048
```

The adapter runs the argument list with `shell=False`; a missing runtime is an
explicit optional-step failure. A temporary JSON request contains
`protocol_version: 1`, `engine: HermiT`, local `individuals` and `ontology` paths,
`imports` (IRI -> local path), `inferred_output`, `result_output`,
`assertion_kinds: [named_class, object_property, data_property]`, and `heap_mb`.
The worker must verify its OWLAPI import closure, run HermiT consistency and
classification, materialize the requested assertion kinds to inferred Turtle,
and write JSON confirming `engine: HermiT`, `consistent: true`,
`materialized: true`. Merely running a reasoner is insufficient.

The adapter publishes new selected inferred triples and a combined graph,
reasoning log, and report. Worker failures preserve the core RDF and existing
inference outputs. The protocol fixture tests transport/publication, not real
HermiT reasoning. Real worker integration must be supplied and verified before
claiming HermiT execution.

## Explicit implementation limits

- `state_events.as_of_turn` creates a prefix from transcript-file/worksheet inputs,
  excluding future utterances, move evidence and assignment events. Starter evidence
  is limited to the introduction turn. Base-RDF inputs must already be truncated;
  arbitrary external assertions cannot be safely projected into the past.
- Combined inference plus `--dry-run` is rejected; dry-run the core with
  `--no-inference`, or run standalone `materialize --dry-run` against saved RDF
  to validate the optional worker request without starting the worker.
- Conversation-filtered SHACL is not implemented. The SHACL stage processes the
  complete supplied file. Supply a selected-conversation file when needed.
- Extra domain shapes for required evidence/reason fields and trigger semantics
  are not generated; the included shapes validate assignment history. Conversion
  validates known references, explicit fields, event timing, and endpoint types.
- Custom IRI templates, speaker aliases, and per-row source-ID crosswalk files
  are not supported configuration keys; unknown keys fail instead of being ignored.
- Stable graph identities/isomorphism are tested; byte-identical serialization
  is not promised. Original XML formatting need not be retained by the new API.
- Whole multi-artifact publication is not a filesystem transaction; each file
  replacement is atomic. SHACL nonconformance never publishes final RDF.

Legacy script executable paths delegate to package `build` or `shacl`, with a
migration notice. Their old partial-import CLI options are retired. Old internal
helpers remain only for regression fixtures and are not the public library API.

## Tests and distributions

```powershell
python -m unittest discover -s tests/pipeline -v
python -m build --no-isolation
python -m pip install dist/cjf_serializer-0.1.0-py3-none-any.whl
```

Wheel installation includes profiles/shapes and works outside the checkout.
