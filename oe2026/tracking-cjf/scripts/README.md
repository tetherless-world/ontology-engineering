# Import annotated dialogue XML into the individuals ontology

`xml_to_individuals.py` uses Python 3.10+ and the standard library only. It appends
to `../tracking-cjf-individuals.rdf`, following the three existing manual examples
and retaining the ontology IRI, imports, prefixes, original individuals, comments,
and unrelated RDF statements. The main `tracking-cjf.rdf` is never modified.

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
19:48:41. For turns sharing a timestamp, the first utterance retains the example's
name (e.g. `Mar11GroupB200536`); later ones get a suffix such as
`Mar11GroupB200536Turn36`. They share the same DateTime individual.

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
