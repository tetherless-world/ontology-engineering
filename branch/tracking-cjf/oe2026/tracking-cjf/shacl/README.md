# Run the current assignment SHACL rule

The shapes in this folder define the terminal-assignment rule and history
constraints. The supported file-writing command is provided by the installed
`cjf-serializer` package; see [the pipeline guide](../../../PIPELINE.md).

```powershell
cjf-serialize shacl --individuals asserted-individuals.rdf --output current-individuals.rdf --report shacl-report.json
cjf-serialize shacl --individuals asserted-individuals.rdf --output current-individuals.rdf --dry-run
```

The command reads the source, clears old current pointers in memory, calls
pySHACL once, and writes the output only on conformance. Inputs remain unchanged.
An explicit `--shapes path/to/shapes.ttl` selects custom shapes; otherwise the
installed package includes a copy of this resource. The packaged template aligns
its turn datatype to a supplied ontology or the unambiguous input datatype;
custom shapes are never silently changed. `--overwrite` permits replacing an
existing destination. The complete input graph is processed.

Python does not independently traverse state histories, compare its own endpoint
selection, inspect rule output scope, or automatically repeat the operation.
Those removed checks are not restored. Rules add current pointers, while shapes
validate cardinality, ownership, predecessors, cycles and turn order. No OWL
inference/imports occur, and no specific state classification is generated.

Settings remain advanced=True, inference='none', inplace=True,
iterate_rules=True, do_owl_imports=False, meta_shacl=True. Iteration is redundant
for this single rule but retained for compatibility. Meta-SHACL checks shapes
structure, not domain correctness. Validation failures produce diagnostics and
leave previous RDF outputs untouched. The JSON report has `.shacl.txt` and
`.shacl.ttl` sidecars when `--report` is requested.
