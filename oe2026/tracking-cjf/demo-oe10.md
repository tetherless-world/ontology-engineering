---
layout: default
title: OE Week 10 Demonstration and Queries
---

<link rel="stylesheet" href="styles/demo.css">
<script src="scripts/demo.js" defer></script>

[Current OE Week 11 demonstration](demo.html)

## OE Week 10 Sample Conversation

The demonstration uses the [CQ sample conversation individuals with current assignments](prev-ontology-versions/OE_10/OE_10_TeamCJF_Individuals.rdf) with the [OE Week 10 CJF schema](prev-ontology-versions/OE_10/OE_10_TeamCJF.rdf). The [source conversation transcript](inputs/Oct21_A_Discussion.md) preserves the 28 turns and speaker labels used by the [current generation configuration](configs/cq-sample.yaml). The [earlier conversation XML](files/conversations/CQ-sample-conversation.xml) is retained for reference.

## Running the Queries

These queries use OWL DL reasoning. Open `prev-ontology-versions/OE_10/OE_10_TeamCJF_Individuals.rdf` in Protégé with the matching `OE_10_TeamCJF.rdf` schema and its imports. Select HermiT and start the reasoner, then run each query in SNAP SPARQL, copying it from the first `PREFIX` line through its final line. The queries and recorded answers are displayed below; each answer table includes all recorded rows.

- [Download the combined CQ1, CQ2, CQ3, CQ5, and CQ6 queries (.txt)](CQAnswers/oe10/OE_10_TeamCJF_SPARQLQueries.txt)
- [Earlier OE Week 9 query set (.txt)](CQAnswers/OE_9_TeamCJF_SPARQLQueries.txt)

## CQ1 Conversation Moves and Current States

**Question:** Which CJF conversation moves have occurred in the conversation, and what is the latest known state of each conversation move, where a state applies?

### SPARQL query

{% capture cq1_query %}{% include_relative CQAnswers/oe10/CQ1/CQ1.conversation-moves.current-states.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ1 SPARQL query"><code class="language-sparql">{{ cq1_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ1 recorded answers" data-csv-source="CQAnswers/oe10/CQ1/CQ1.conversation-moves.current-states.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/oe10/CQ1/CQ1.conversation-moves.current-states.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/oe10/CQ1/CQ1.conversation-moves.current-states.answers.csv">Recorded answers (.csv)</a></p>

The query returns each move, its move type, state result, and summary. Its optional state pattern retains conversation moves without an applicable or known specific state. When querying `hasState`, the ontology's property chain derives the state through `hasCurrentStateAssignment` followed by `assignedState`; the corresponding inferred triples must be available to the query engine. Multiple state classifications can produce more than one row for a move.

The [SHACL rules](shacl/current-state-assignment-rules.ttl) identify terminal assignments in each move's recorded history. The [Python pipeline](src/cjf_serializer/pipeline.py) refreshes the current assignment links and validates the histories. “Current” refers to the latest assignment in the loaded conversation data. The [pipeline documentation](PIPELINE.html) describes the import and validation workflow.

## CQ2 Issues Currently Addressed or Resolved

**Question:** Which issues are currently addressed or resolved, and what evidence supports each current state?

### SPARQL query

{% capture cq2_query %}{% include_relative CQAnswers/oe10/CQ2/CQ2.issues-currently-addressed-or-resolved.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ2 SPARQL query"><code class="language-sparql">{{ cq2_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ2 recorded answers" data-csv-source="CQAnswers/oe10/CQ2/CQ2.issues-currently-addressed-or-resolved.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/oe10/CQ2/CQ2.issues-currently-addressed-or-resolved.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/oe10/CQ2/CQ2.issues-currently-addressed-or-resolved.answers.csv">Recorded answers (.csv)</a></p>

The query starts from each Issue's `hasCurrentStateAssignment` and returns the classes of its assigned state, excluding the generic State, SIO entity, and `owl:Thing` classes. It then follows `hasTriggeringRelationship` to the relationship that triggered the assignment and returns that relationship's supporting text as evidence. The recorded answers cover six Issues. The platform-selection Issue (M0001) and the funding Issue (M0010) are Resolved; their state individuals are also classified as Addressed, so each evidence passage appears under both classes. The training (M0014), cost-comparison (M0028), attendance (M0050), and onboarding-content (M0055) Issues are Addressed.

## CQ3 Claims Supporting or Challenging Platform A

**Question:** What Claims support or challenge Platform A? Are any of the Claims Supported?

### Claims and their current states

#### SPARQL query

{% capture cq3_all_query %}{% include_relative CQAnswers/oe10/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ3 claims and states SPARQL query"><code class="language-sparql">{{ cq3_all_query | escape }}</code></pre>

#### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ3 claims and states recorded answers" data-csv-source="CQAnswers/oe10/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/oe10/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/oe10/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv">Recorded answers (.csv)</a></p>

### Supported Claims

#### SPARQL query

{% capture cq3_supported_query %}{% include_relative CQAnswers/oe10/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ3 supported Claims SPARQL query"><code class="language-sparql">{{ cq3_supported_query | escape }}</code></pre>

#### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ3 supported Claims recorded answers" data-csv-source="CQAnswers/oe10/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/oe10/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/oe10/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.answers.csv">Recorded answers (.csv)</a></p>

The first query finds Claims that support or challenge Platform A and shows their current states and summaries. Property chains infer the `supports`, `challenges`, and `hasState` links used by the query. The second query keeps Claims whose current state is `Supported`. A Claim can challenge Platform A and still have a Supported state. The recorded answers contain six supporting and three challenging Claims; five supporting Claims and one challenging Claim have a Supported current state.

## CQ5 Speakers Agreeing with the Selected Option

**Question:** For the final platform-selection Outcome, which speakers explicitly agreed with its selected Option, and which ExpressedPosition moves and source turns provide the evidence?

### SPARQL query

{% capture cq5_query %}{% include_relative CQAnswers/oe10/CQ5/CQ5.speakers-that-agreed-with-group-outcome.span.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ5 SPARQL query"><code class="language-sparql">{{ cq5_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ5 recorded answers" data-csv-source="CQAnswers/oe10/CQ5/CQ5.speakers-that-agreed-with-group-outcome.answer.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/oe10/CQ5/CQ5.speakers-that-agreed-with-group-outcome.span.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/oe10/CQ5/CQ5.speakers-that-agreed-with-group-outcome.answer.csv">Recorded answers (.csv)</a></p>

The query follows `selects` from the final Outcome to the chosen Option, then finds Agreement moves targeting that Option. It returns each position, speaker, supporting text, and turn number. The reasoner infers `Agreement` from the positions’ `isPositiveSupportedBy` links to TextSpans. Property chains infer `hasPositionTowards`, `hasSpeaker`, and `hasUtterance`. The recorded answer identifies Speaker D at turn 25, Speaker B at turn 26, Speaker C at turn 27, and Speaker A at turn 28.

## CQ6 Speaker C's Positions toward Platforms A and B

**Question:** What positions did Speaker C express toward Platform A and B throughout the conversation?

### SPARQL query

{% capture cq6_query %}{% include_relative CQAnswers/oe10/CQ6/CQ6.speaker-c-positions-platform-a-b.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ6 SPARQL query"><code class="language-sparql">{{ cq6_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ6 recorded answers" data-csv-source="CQAnswers/oe10/CQ6/CQ6.speaker-c-positions-platform-a-b.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/oe10/CQ6/CQ6.speaker-c-positions-platform-a-b.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/oe10/CQ6/CQ6.speaker-c-positions-platform-a-b.answers.csv">Recorded answers (.csv)</a></p>

The query finds Speaker C's ExpressedPosition moves through the inferred `hasSpeaker` link and keeps those whose `hasPositionTowards` target is Platform A (M0003) or Platform B (M0021). For each position, it returns the summary, the supporting text, and the turn of the source utterance, which must be attributed to Speaker C and belong to the sample conversation. It does not filter for Agreement, so the earlier preference is retained. The recorded answers show Speaker C preferring Platform B at turn 9 (M0020) and agreeing with Platform A at turn 27 (M0063).

CQ4 has no recorded query in the OE Week 10 query set. Its scenario and sample answer are described in the [OE Week 10 use case (.docx)](files/use-cases/OE_10_TeamCJF_UseCase.docx).
