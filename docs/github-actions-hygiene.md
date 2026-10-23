# CJF ontology hygiene on GitHub Actions

The `Ontology hygiene` workflow runs the course's 18 queries in
`.hygiene/curated_tests_some_errors` against `oe2026/tracking-cjf`. It runs on
pushes to `tracking-cjf` and `codex/**`, and on pull requests targeting
`tracking-cjf`.

The namespace filter covers resources whose IRIs start with
`https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/`. Imported vocabulary
IRIs are outside that filter. Files under `archived/` retain the course's
exclusion policy. Errors fail the check; warnings remain visible without
failing it. Change `HYGIENE_FAIL_ON_WARNINGS` in the workflow to `'true'` when
warnings should also fail the check.

## Read results

Open **Actions → Ontology hygiene → a run → CJF ontology hygiene**, and expand
**Run ontology hygiene tests**. Read the `Errors in DEV` section and the
`ERROR:` / `WARN:` result rows. A CSV column named `error` is a header, not a
violation by itself.

Download **cjf-ontology-hygiene-results** from the run summary for the publisher
output and `hygiene_test.dev.xml`. Reports are retained after a failed test step
when the publisher produced them. Missing, malformed, or empty DEV reports
fail the check too; a green publisher exit alone is insufficient.

## Run locally

Start Docker with Compose support and have Python 3 available. From this
repository's root, on a checked-out Git branch, run:

```bash
ONTPUB_SUBDIR=oe2026/tracking-cjf \
HYGIENE_NAMESPACE_REGEX='^https:\/\/tw[.]rpi[.]edu\/ontology-engineering\/oe2026\/tracking-cjf\/' \
bash .hygiene/run_github_actions.sh
```

Outputs are ignored by Git under `.hygiene/output/run.*/`. The container is
removed on exit. The Compose configuration uses the course's container name
`hygiene`, so run one local hygiene job at a time.

The existing CircleCI runner and its default scope remain available.
`set_env.sh` now accepts environment overrides so the Actions job can narrow
the scope without changing the course-wide defaults.

## Confirm namespace coverage

In a temporary branch, add a `.ttl` file under `oe2026/tracking-cjf` containing:

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/hygiene-canary>
    a owl:Ontology .
<https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/HygieneCanary>
    a owl:Class .
```

Commit and push it, then confirm the log reports that `HygieneCanary` lacks
a label and definition. Remove the temporary file afterward. This checks
both file discovery and namespace matching; a report with executed queries
alone does not prove that the intended resources were in scope.

## Manual runs and required checks

The workflow includes `workflow_dispatch`. GitHub exposes its **Run workflow**
button after the workflow also exists on the repository's default branch
(`master`). It runs automatically from pushes and pull requests to the branches
listed above before that default-branch installation.

Once the workflow has run, you can select **CJF ontology hygiene** as a required
status check in the rule protecting `tracking-cjf`.
