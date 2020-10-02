---
toc: true
---

# Ontology Development

## Git Serializer

The git serializer will run whenever you make a git commit and will ensure that your ontology source files are formatted in such a way that they can be easily diffed when changes are made.

The serializer requires Java and should work with version 8 or later.
If you don't have Java installed on your machine, download and install it from
[the Java website](https://java.com/en/download/).

Installing the serializer will involve modifications to a hidden folder within the repository: `.git`.
**Make sure that the file browser you are using is capable of displaying hidden files**.

Instructions for installing the serializer:

1. Download the
    [rdf-toolkit jar file](https://jenkins.edmcouncil.org/job/rdf-toolkit-build/lastSuccessfulBuild/artifact/target/scala-2.12/rdf-toolkit.jar)
    and place it in `.git/hooks/` within the ontology-engineering repository.
1. Copy the pre-commit script from `serializer/pre-commit` to `.git/hooks/`.
1. In `.git/hooks/pre-commit`, set line 12 (`export JAVA_HOME=...`) to match your java installation.
    * If you don't know where or what that is, [this site may help](https://www.baeldung.com/find-java-home).
    * If you are sure that the `JAVA_HOME` environment variable is set properly on your system, you can comment this line out: `#export JAVA_HOME=...`.
    * If you are not sure, you will need to locate the directory where Java is installed, which will vary from system to system, and set that as the value of `JAVA_HOME`.
    This directory should have a `bin` folder containing the `java` executable.
1. To make sure everything is working, open a command line interface and navigate to the ontology-engineering repository directory.
    When you run `git commit`, you should see output similar to below preceding the normal git output:

    ```
    rdf-toolkit: sesame-serializer: This is the pre-commit hook
    rdf-toolkit: sesame-serializer: java_home = /usr/lib/jvm/default
    rdf-toolkit: sesame-serializer: whichJava = /usr/lib/jvm/default/bin/java
    openjdk version "1.8.0_265"
    OpenJDK Runtime Environment (build 1.8.0_265-b01)
    OpenJDK 64-Bit Server VM (build 25.265-b01, mixed mode)
    rdf-toolkit: sesame-serializer: versionJava =  1.8.0_265
    rdf-toolkit: sesame-serializer: java_major=1
    rdf-toolkit: sesame-serializer: java_minor=8
    rdf-toolkit: sesame-serializer: Found rdf-toolkit: /home/sam/workspace/ontology-engineering/.git/hooks/rdf-toolkit.jar
    ```

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
