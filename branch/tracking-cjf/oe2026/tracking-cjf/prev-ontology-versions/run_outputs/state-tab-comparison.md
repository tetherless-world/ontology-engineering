# States worksheet compared with Week 9 individuals

Source: original Annotation Workbook Synthetic Example (CQs).xlsx, States tab
https://docs.google.com/spreadsheets/d/15tMB0D3c1_Yh5iuZsq--GGefnmhH8agB/edit

The workbook used to generate Week 9 outputs had its States tab removed. This
comparison uses the original workbook as a reference, without importing it or
changing either RDF output.

## Results

- 80 States rows; 85 RDF assignments.
- All 80 rows match an RDF assignment by move and effective turn.
- Evidence turn sets match exactly for all 80 rows, with inclusive ranges expanded.
- All 54 starter assignments have the annotated initial state type.
- All 26 later annotated events have matching assignment records, but their RDF
  states are generic State individuals. Their expected specific types have not
  been checked by a DL reasoner; this is record/evidence agreement, not verified
  state-classification agreement.
- Five additional generic assignments come from further relationship events.
- Assignment data is identical in the asserted and CurrentStateAdded RDF files;
  the latter only adds current pointers.

## Additional assignments absent from the States tab

| Move | Turn | Evidence turns | Move summary |
| --- | --- | --- | --- |
| OCT21_A-M0001 | 9 | 1, 9 | Choose a platform for the new development project. |
| OCT21_A-M0023 | 13 | 10, 13 | C expects Platform B to cost less overall than Platform A. |
| OCT21_A-M0023 | 14 | 10, 13, 14 | C expects Platform B to cost less overall than Platform A. |
| OCT21_A-M0010 | 15 | 5, 6, 15 | Platform A may exceed the team's current tooling budget. |
| OCT21_A-M0055 | 24 | 22, 23, 24 | Onboarding limited to a product overview may leave developers unprepared for their first deployment. |

These extra relationship events do not necessarily signify a different state.
They produce additional generic candidates because the new package records
relationship events independently of the older States worksheet. They also
change immediate-predecessor links relative to the worksheet's sparse history.
State reasons in this run are generated from starter/relationship events rather
than copied from this reference States tab. No DL inference was run for this
comparison. No ontology, source workbook, or individuals files were modified.

Full row-by-row results: state-tab-comparison.json.
