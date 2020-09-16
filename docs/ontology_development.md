# Ontology Development

## Ontology Hygiene

Every time you push commits to your branch, a continuous integration job will run ontology hygiene checks on your branch.
These checks will examine the ontologies in the repository and report errors if the ontologies do not conform to certain best practices.

The checks will pick up ontologies in files with extensions `.rdf`, `.ttl`, or `.jsonld`.
These files can be anywhere in the repository.

Resources in your ontology that do not contain `twc` in the namespace will not be checked.
This is done to prevent checking of imported ontologies.
*All of the resources for ontologies you develop must contain `twc` in the namespace.*

If the hygiene checks find errors in your ontologies, then the CI job will fail.
This will update the status of your latest commit to indicate that it did not pass checks.
*When submitting assignments, your ontologies must pass all hygiene checks.*

You can view details about the hygiene test runs on the project [CircleCI page](https://app.circleci.com/pipelines/github/tetherless-world/ontology-engineering).
