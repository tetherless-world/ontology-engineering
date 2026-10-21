#!/usr/bin/env python3
"""Import only Open initial state rows from the States worksheet.

The shared importer also supports Under Consideration and Unassessed states.
This entry point preserves the existing Open-only command and report fields.
"""

from initial_states_to_individuals import REQUIRED_COLUMNS, make_initial_states, main


def make_open_states(rows, rdf_data, schema_data, workbook_name):
    return make_initial_states(rows, rdf_data, schema_data, workbook_name, ("Open",))


if __name__ == "__main__":
    raise SystemExit(main(("Open",)))
