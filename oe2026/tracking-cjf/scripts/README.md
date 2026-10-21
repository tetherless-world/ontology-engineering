# Import annotated dialogue XML into the individuals ontology

`xml_to_individuals.py` uses Python 3.10+ and the standard library only. It appends
to `../tracking-cjf-individuals.rdf`, following the existing individual structure
and using turn numbers in utterance IRIs. It retains the ontology IRI, imports,
prefixes, existing individuals, comments, and unrelated RDF statements. The main
`tracking-cjf.rdf` is never modified.

Save any pending edits in Protégé before running the converter. Afterward, reload
or reopen `tracking-cjf-individuals.rdf` to see the generated individuals; saving
an older in-memory copy from Protégé could overwrite the generated data.

From this directory:

```sh
python3 xml_to_individuals.py /Users/devindesilva/Downloads/Mar11_GroupB_annotated.xml
```

From another directory, invoke the script by its full path. The default RDF path
is resolved relative to the script, so it does not depend on the working directory.
Use `--individuals PATH` for a different existing individuals file or
`--output PATH` to generate a preview/copy. Use `--report PATH` for a JSON report
containing every source attribute and the source-turn-to-individual mapping.
Existing targets receive a `.bak` backup on the first changed run. `--backup PATH`
selects another backup location; an existing backup is never overwritten.

## Mapping used

| Source | RDF representation |
| --- | --- |
| Each `<turn>` | One `owl:NamedIndividual` of type `tracking-cjf:Utterance` |
| Utterance IRI | Conversation prefix + `Turn` + integer `hasTurnNumber`, e.g. `tracking-cjf:Mar11GroupBTurn1` |
| `speaker="moderator"` | `prov:wasAttributedTo` → `tracking-cjf:Mar11GroupBModerator`, typed `tracking-cjf:Speaker` |
| `end_time="19:48:41 PM"` | `DatesAndTimes:hasDateTime` → `tracking-cjf:DTMar11194841`, typed `DatesAndTimes:DateTime` |
| Turn text | `tracking-cjf:hasConversationText`, preserving parsed text and whitespace |
| XML document order | `tracking-cjf:hasTurnNumber`, an integer starting at 1, with the same `xsd:integer` datatype as the example |
| Original `turn_no` when it differs from the integer sequence | `dc:identifier`, preserving the exact original value |

All new individual IRIs use the same `tracking-cjf` namespace as the examples.
Speakers are reused within the conversation. DateTime individuals have only their
type assertion, exactly as in the manual example; no new date-value property or
timezone is introduced. The source date and full original timestamp are retained
in the optional JSON report.

The XML uses redundant 24-hour timestamps such as `19:48:41 PM`; these are read as
19:48:41 and used for the DateTime individuals. Utterance IRIs use the integer turn
sequence instead: `Mar11GroupBTurn1` through `Mar11GroupBTurn480` for this source.
Turns sharing a timestamp still have distinct utterance IRIs and share the same
DateTime individual. The URI suffix always matches `hasTurnNumber`.

The provided file contains 480 XML turn elements but original turn numbers up to
479, because source turn 117 is split into `117.0` and `117.1`. Generated
`hasTurnNumber` values are unique integers 1–480. The two split turns have sequence
numbers 117 and 118, and source turn 118 has sequence number 119. From this point,
`dc:identifier` retains each original source number. No subturn is dropped or
rounded into another turn.

The attributes `comm_act_type`, `dialog_act`, `link_to`, `mode`, `polarity`, `pos`,
`pos_count`, `pos_origin`, and `topic` have no mapping in the user's manual example.
They are preserved in the optional JSON report and source XML, rather than used
to infer milestone classes or relationships automatically.

Repeated runs with the same source do not duplicate individuals or change the
RDF bytes. If existing individuals disagree with the expected text, attribution,
timestamp link, or sequence, the script stops before editing the RDF. It preserves
extra annotations on otherwise matching individuals. It does not refresh or delete
data from earlier imports: use the backup or a fresh template if the source changes.

The defaults reproduce this dataset's naming convention, including the yearless
`DTMar11` prefix. For additional datasets/years, use `--conversation-prefix` and
`--datetime-prefix` to choose distinct prefixes and avoid naming collisions.

## Verification

```sh
python3 -m unittest discover -s . -p 'test_xml_to_individuals.py' -v
```

The checks cover the existing example, same-second turns, split source numbers,
text escaping, repeat runs, backups, conflicting existing data, and invalid input.
The converter checks every mapped statement after serialization. These checks
verify the conversion; they are not an OWL reasoner consistency check.

## Import the Milestones worksheet

`milestones_to_individuals.py` reads only the worksheet named `Milestones` from an
annotation workbook. It reads workbook routing metadata and only the shared-string
values referenced by that sheet; it never opens other worksheet contents.

```sh
python3 milestones_to_individuals.py '/Users/devindesilva/Downloads/Annotation workbook CJF (1).xlsx'
```

Each row with a `milestone_id` creates one individual with that exact identifier
in the tracking-cjf namespace, for example `tracking-cjf:MAR11_B-M0001`. Summaries,
original type names, attributes, annotation questions, and source row references
are preserved as annotations. Rows without milestone IDs are reported and skipped.
Missing milestone IDs are not invented or renumbered.

The workbook's Claim, Option, Issue, Information Request, Expressed Position, and
Outcome types map to their existing ontology classes. Conversation Management
maps to `CollectiveJudgmentFormationConversationMove`, because there is no
dedicated class for it. Expressed positions are asserted only as `ExpressedPosition`.
Explicit agreement and disagreement attributes select positive or negative
supporting evidence links; the ontology's class definitions infer `Agreement` or
`Disagreement`. Preference, uncertainty, and requested-response types remain
source annotations.

Each quoted source turn creates a TextSpan linked to its existing utterance with
`isPartOfUtterance`. Milestones link to those spans through SIO `is supported by`,
or its positive/negative subproperties for explicit agreement/disagreement.
The existing property chain can then infer `hasSpeaker`. Multi-turn ranges and
semicolon-separated source IDs are resolved to separate evidence spans.

The inferred position definitions are `Agreement EquivalentTo ExpressedPosition
and (isPositiveSupportedBy some TextSpan)` and `Disagreement EquivalentTo
ExpressedPosition and (isNegativeSupportedBy some TextSpan)`. Polarity comes from
the workbook annotation; the OWL reasoner does not interpret the quotation's
natural-language text. The report's `expected_inferred_position_subtypes` counts
these annotated polarities, rather than claiming to have run a reasoner.

Original source turn IDs are looked up through `dc:identifier`, falling back to
`hasTurnNumber` where those numbers coincide. They are not assumed to equal the
current URI suffix: source turn 361 resolves to `Mar11GroupBTurn362` in this data.
Workbook quotations are preserved even when they differ from the existing
transcript; differences are recorded in the optional JSON report.

The same `--individuals`, `--ontology`, `--output`, `--backup`, and `--report` path
options are available. Repeat runs do not duplicate existing individuals. The
importer does not modify the workbook or schema, import states from other tabs,
or infer inter-milestone relationships from annotation questions.
