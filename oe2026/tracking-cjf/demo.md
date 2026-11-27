---
layout: default
title: Demonstration and Queries
---

<link rel="stylesheet" href="styles/demo.css">
<script src="scripts/demo.js" defer></script>

## Demonstration Walkthrough

The demonstration follows a 28-turn discussion in which four speakers choose between two software platforms. For each of the six competency questions, it builds the SPARQL query one pattern at a time, names the inferences HermiT contributes at each step, and shows the answer in Protégé.

- **Slides:** the walkthrough deck below steps through every query and its Protégé output.
- **Interactive graphs:** the [competency question graphs](answer-graphs.html) let you pick a question and a worked answer, advance through the query step by step, and see which recorded, inferred, and SHACL-derived RDF links each pattern matches.
- **Queries and answers:** the sections below give each question's steps, its full query with a **Copy query** button, and every recorded answer row.

<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=https%3A%2F%2Ftetherless-world.github.io%2Fontology-engineering%2Fbranch%2Ftracking-cjf%2Foe2026%2Ftracking-cjf%2Ffiles%2Fdemo%2FCJF-OE12-CQ-demo-walkthrough.pptx" title="Competency question demonstration walkthrough slides" style="width:100%;aspect-ratio:16/10;border:0;" loading="lazy" allowfullscreen></iframe>

[Download the walkthrough slides (.pptx)](files/demo/CJF-OE12-CQ-demo-walkthrough.pptx)

## Sample Conversation

The demonstration uses the [sample conversation individuals with current assignments](ontology/TeamCJF_Individuals.rdf) with the [Tracking CJF 1.0 schema](ontology/TeamCJF.rdf). The [source conversation transcript](inputs/Oct21_A_Discussion.md) preserves the 28 turns and speaker labels used by the [CQ sample generation configuration](configs/cq-sample.yaml). The [earlier conversation XML](files/conversations/CQ-sample-conversation.xml) is retained for reference.

The [facilitation prototype](facilitator.html) uses the same individuals to replay issues and suggest a follow-up at a selected turn.

## Running the Queries

These queries use OWL DL reasoning. Open [`ontology/TeamCJF_Individuals.rdf`](ontology/TeamCJF_Individuals.rdf) in Protégé, either downloaded or with *File → Open from URL*; it imports the schema, `TeamCJF.rdf`, from this site. To work offline, save it together with `TeamCJF.rdf` and `catalog-v001.xml`. Select HermiT and start the reasoner, then run each query in SNAP SPARQL. Use the **Copy query** button above each query to copy it in full, from the first `PREFIX` line through its final line, and paste it into the SNAP SPARQL tab or a triple store. The queries and recorded answers are displayed below; each answer table includes all recorded rows. Scroll within a wide table to see all columns.

- [Download all competency question queries (.txt)](CQAnswers/TeamCJF_SPARQLQueries.txt)
- [OE Week 10 demonstration and recorded answers](demo-oe10.html)

## CQ1 Conversation Moves and Current States

[CQ1 in the use case](usecase.html#cq1) · [Explore the CQ1 answer graph](answer-graphs.html#cq1)

**Question:** Which CJF conversation moves have occurred in the conversation, and what are their identifiers, types, summaries, and current recorded state(s), where applicable?

### How the query works

1. Find moves of each of the six types. Each `UNION` branch matches one class and writes its name into the same `?moveClass` column.
2. Get the annotator's summary for the same move.
3. Follow the move to its current State, if it has one. `OPTIONAL` keeps moves without a state.
   *Inference:* `hasState` follows the property chain `hasCurrentStateAssignment` → `assignedState`.
4. Read the specific class of that State. `MINUS` drops the generic State class.
   *Inference:* State individuals are classified by equivalent class definitions that consider the previous state assignment, the move, and the relationship that triggered the change.
5. Return the state class, or `N/A` when the move has no state.

**Result:** The 70 rows cover 67 distinct moves; 13 rows show `N/A`. The funding issue M0010 has two current classes, Addressed and Resolved, because its current State satisfies both definitions.

### SPARQL query

{% capture cq1_query %}{% include_relative CQAnswers/CQ1/CQ1.conversation-moves.current-states.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ1 SPARQL query"><code class="language-sparql">{{ cq1_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ1 recorded answers" data-csv-source="CQAnswers/CQ1/CQ1.conversation-moves.current-states.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ1/CQ1.conversation-moves.current-states.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ1/CQ1.conversation-moves.current-states.answers.csv">Recorded answers (.csv)</a></p>

The query returns each move, its move type, state result, and summary. Its optional state pattern retains conversation moves without an applicable or known specific state. When querying `hasState`, the ontology's property chain derives the state through `hasCurrentStateAssignment` followed by `assignedState`; the corresponding inferred triples must be available to the query engine. Multiple state classifications can produce more than one row for a move.

The [SHACL rules](shacl/current-state-assignment-rules.ttl) identify terminal assignments in each move's recorded history. The [Python pipeline](src/cjf_serializer/pipeline.py) refreshes the current assignment links and validates the histories. “Current” refers to the latest assignment in the loaded conversation data. The [pipeline documentation](PIPELINE.html) describes the import and validation workflow.

## CQ2 Issues Currently Addressed or Resolved

[CQ2 in the use case](usecase.html#cq2) · [Explore the CQ2 answer graph](answer-graphs.html#cq2)

**Question:** Which Issues raised during the conversation have been assigned an Addressed or Resolved state, and what conversational evidence is associated with each Issue and its current recorded states?

### How the query works

1. Start with the moves classified as Issue.
2. Follow the Issue's current assignment, written by the SHACL rule for the loaded conversation, and read its State.
3. Read the specific state class, excluding the generic State class.
   *Inference:* Addressed and Resolved are inferred from the Issue's previous state assignment and the relationship that triggered the change.
4. Find the relationship that triggered the assignment. The assignment and its trigger are separate records.
5. Follow the SIO evidence property from that relationship to its text span and read the words.

**Result:** Six Issues produce 32 distinct evidence rows. For example, the training concern M0014 is Addressed at turn 20 by the proposal to use Monday's training slot for a vendor-led session; the transcript still leaves the arrangements to be confirmed.

### SPARQL query

{% capture cq2_query %}{% include_relative CQAnswers/CQ2/CQ2.issues-currently-addressed-or-resolved.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ2 SPARQL query"><code class="language-sparql">{{ cq2_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ2 recorded answers" data-csv-source="CQAnswers/CQ2/CQ2.issues-currently-addressed-or-resolved.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ2/CQ2.issues-currently-addressed-or-resolved.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ2/CQ2.issues-currently-addressed-or-resolved.answers.csv">Recorded answers (.csv)</a></p>

The query follows each Issue’s current assignment and returns the assigned state classes and supporting text from the triggering relationship. Rows are sorted by Issue, state class, and evidence, so the order matches the recorded answers.

## CQ3 Claims Supporting or Challenging Platform A

[CQ3 in the use case](usecase.html#cq3) · [Explore the CQ3 answer graph](answer-graphs.html#cq3)

**Question:** Which Claims support or challenge Platform A, what are their summaries and current recorded states, and which of these Claims have been assigned a Supported state?

### How the query works

1. Find moves that support or challenge Platform A (M0003). Two `UNION` branches bind `?relation` to the matched relationship.
   *Inference:* `supports` and `challenges` are inferred through the property chains over the reified relationships.
2. Keep the moves that are Claims.
3. Find the Claim's current State.
   *Inference:* `hasState` follows `hasCurrentStateAssignment` → `assignedState`.
4. Read the specific State class, removing the broad types named in the filter.
   *Inference:* Supported and Contested are inferred from the Claim's previous state and the Support or Challenge relationship that triggered the assignment.
5. Get the Claim's summary, if one is recorded.

**Result:** Nine Claims appear: six support Platform A and three challenge it. Six are Supported, including M0013, the $6,000 funding-gap Claim, which challenges Platform A and itself has a Supported state.

### SPARQL query

{% capture cq3_all_query %}{% include_relative CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ3 claims and states SPARQL query"><code class="language-sparql">{{ cq3_all_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ3 claims and states recorded answers" data-csv-source="CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv">Recorded answers (.csv)</a></p>

The query returns Claims that support or challenge Platform A, their current state classifications, and their summaries. A Claim can challenge Platform A and still have a Supported state.

## CQ4 Platform A Issues and Their States

[CQ4 in the use case](usecase.html#cq4) · [Explore the CQ4 answer graph](answer-graphs.html#cq4)

**Question:** Which Issues challenge Platform A, how have their states changed throughout the conversation, and what evidence supports these changes?

### How the query works

1. Follow the Challenge relationships to Platform A and keep the moves classified as Issue.
2. Follow `hasStateAssignment` to read each Issue's whole history; each assignment points to its own State.
3. Read its Open, Addressed, or Resolved state.
   *Inference:* Addressed and Resolved are inferred from previous state assignments and triggering relationships.
4. Find the triggering relationship and the move whose `makesAddresses` link points to it, if recorded. Initial Open assignments have no trigger.
5. Follow the source move to its evidence span and read the words.

**Result:** Eleven rows cover eight assignments for three Issues. The funding issue M0010 was Open at turn 5, Addressed at turns 9 and 15, and both Addressed and Resolved at turn 18, with the evidence “That settles the funding concern.” from turn 19.

### SPARQL query

{% capture cq4_query %}{% include_relative CQAnswers/CQ4/CQ4.issues-platform-a-historical-states.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ4 SPARQL query"><code class="language-sparql">{{ cq4_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ4 recorded answers" data-csv-source="CQAnswers/CQ4/CQ4.issues-platform-a-historical-states.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ4/CQ4.issues-platform-a-historical-states.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ4/CQ4.issues-platform-a-historical-states.answers.csv">Recorded answers (.csv)</a></p>

The query finds Issues that explicitly challenge Platform A. Each row shows one Open, Addressed, or Resolved classification from the Issue’s recorded assignments, with the source move and evidence that triggered it. Initial Open assignments have no source move or evidence. Rows are sorted by Issue, state, source move, and evidence.

## CQ5 Speakers Agreeing with the Selected Option

[CQ5 in the use case](usecase.html#cq5) · [Explore the CQ5 answer graph](answer-graphs.html#cq5)

**Question:** Which speakers explicitly agreed with the Option selected by the group, and what are the identifiers, supporting utterances, and turn numbers of their Expressed Positions?

### How the query works

1. Find the Option selected by the final Outcome.
   *Inference:* `selects` follows the property chain `makesSelects` → `isAimedAtSelects`.
2. Find agreeing positions about that Option.
   *Inference:* `hasPositionTowards` follows `makesPositionTowards` → `isAimedAtPositionTowards`, and an ExpressedPosition positively supported by a TextSpan is classified as an Agreement.
3. Get each position's speaker and name.
   *Inference:* `hasSpeaker` follows a chain from the move to its TextSpan, the Utterance, and the Speaker.
4. Get the evidence span and its supporting text.
5. Get the source utterance and its turn number.

### SPARQL query

{% capture cq5_query %}{% include_relative CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.span.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ5 SPARQL query"><code class="language-sparql">{{ cq5_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ5 recorded answers" data-csv-source="CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.answer.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.span.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.answer.csv">Recorded answers (.csv)</a></p>

The query follows `selects` from the final Outcome to the chosen Option, then finds Agreement moves targeting that Option. It returns each position, speaker, supporting text, and turn number. The reasoner infers `Agreement` from the positions’ `isPositiveSupportedBy` links to TextSpans. Property chains infer `hasPositionTowards`, `hasSpeaker`, and `hasUtterance`. The recorded answer identifies Speaker D at turn 25, Speaker B at turn 26, Speaker C at turn 27, and Speaker A at turn 28.

## CQ6 Speaker C's Positions toward Platforms A and B

[CQ6 in the use case](usecase.html#cq6) · [Explore the CQ6 answer graph](answer-graphs.html#cq6)

**Question:** What positions did Speaker C express toward Platform A and Platform B throughout the conversation, and what are the identifiers, target Options, summaries, supporting utterances, and turn numbers of these Expressed Positions?

### How the query works

1. Find the ExpressedPositions whose speaker is Speaker C. The question includes preferences as well as explicit agreements.
   *Inference:* `hasSpeaker` follows the chain from the position to its TextSpan, Utterance, and Speaker.
2. Keep positions toward Platform A (M0003) or Platform B (M0021).
   *Inference:* `hasPositionTowards` follows `makesPositionTowards` → `isAimedAtPositionTowards`.
3. Get the annotator's summary, if one is recorded.
4. Read the evidence for the position through the SIO evidence property.
5. Check that the utterance belongs to this conversation and to Speaker C, and sort by turn.

### SPARQL query

{% capture cq6_query %}{% include_relative CQAnswers/CQ6/CQ6.speaker-c-platform-positions.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ6 SPARQL query"><code class="language-sparql">{{ cq6_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ6 recorded answers" data-csv-source="CQAnswers/CQ6/CQ6.speaker-c-platform-positions.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ6/CQ6.speaker-c-platform-positions.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ6/CQ6.speaker-c-platform-positions.answers.csv">Recorded answers (.csv)</a></p>

The query finds Speaker C's ExpressedPosition moves through the inferred `hasSpeaker` link and keeps those whose `hasPositionTowards` target is Platform A (M0003) or Platform B (M0021). For each position, it returns the summary, the supporting text, and the turn of the source utterance, which must be attributed to Speaker C and belong to the sample conversation. It does not filter for Agreement, so the earlier preference is retained. The recorded answers show Speaker C preferring Platform B at turn 9 (M0020) and agreeing with Platform A at turn 27 (M0063).
