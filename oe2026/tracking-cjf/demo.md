---
layout: default
title: Demonstration and Queries
---

<link rel="stylesheet" href="styles/demo.css">
<script src="scripts/demo.js" defer></script>

## Sample Conversation

The demonstration uses the [CQ sample conversation individuals](prev-ontology-versions/OE_9_TeamCJF_Individuals_CurrentStateAdded.rdf) with the [OE Week 9 CJF schema](prev-ontology-versions/OE_9_TeamCJF.rdf). The [source conversation transcript](inputs/Oct21_A_Discussion.md) preserves the 28 turns and speaker labels used by the [current generation configuration](configs/cq-sample.yaml). The [earlier conversation XML](files/conversations/CQ-sample-conversation.xml) is retained for reference.

## Running the Queries

These queries use OWL DL reasoning. Open the current-state-added individuals file linked above in Protégé, with the schema and its imports available. Run HermiT, then execute the queries in SNAP SPARQL. The queries and recorded answers are displayed below; each answer table includes all recorded rows.

- [Download the combined CQ1, CQ3, and CQ5 queries (.txt)](CQAnswers/OE_9_TeamCJF_SPARQLQueries.txt)

## CQ1 Conversation Moves and Current States

**Question:** Which CJF conversation moves have occurred in the conversation, and what is the latest known state of each conversation move, where a state applies?

### SPARQL query

{% capture cq1_query %}{% include_relative CQAnswers/CQ1/CQ1.conversation-moves.current-states.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ1 SPARQL query"><code class="language-sparql">{{ cq1_query | escape }}</code></pre>

### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ1 recorded answers" data-csv-source="CQAnswers/CQ1/CQ1.claims-that-supports-platform-a.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ1/CQ1.conversation-moves.current-states.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ1/CQ1.claims-that-supports-platform-a.answers.csv">Recorded answers (.csv)</a></p>

The query returns each move, its move type, state result, and summary. Its optional state pattern retains conversation moves without an applicable or known specific state. When querying `hasState`, the ontology's property chain derives the state through `hasCurrentStateAssignment` followed by `assignedState`; the corresponding inferred triples must be available to the query engine. Multiple state classifications can produce more than one row for a move.

The [SHACL rules](shacl/current-state-assignment-rules.ttl) identify terminal assignments in each move's recorded history. The [Python pipeline](src/cjf_serializer/pipeline.py) refreshes the current assignment links and validates the histories. “Current” refers to the latest assignment in the loaded conversation data. The [pipeline documentation](PIPELINE.html) describes the import and validation workflow.

## CQ3 Claims Supporting or Challenging Platform A

**Question:** What Claims support or challenge Platform A? Are any of the Claims Supported?

### Claims and their current states

#### SPARQL query

{% capture cq3_all_query %}{% include_relative CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ3 claims and states SPARQL query"><code class="language-sparql">{{ cq3_all_query | escape }}</code></pre>

#### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ3 claims and states recorded answers" data-csv-source="CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv">Recorded answers (.csv)</a></p>

### Supported Claims

#### SPARQL query

{% capture cq3_supported_query %}{% include_relative CQAnswers/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.snap.rq %}{% endcapture %}
<pre class="cjf-query" tabindex="0" aria-label="CQ3 supported Claims SPARQL query"><code class="language-sparql">{{ cq3_supported_query | escape }}</code></pre>

#### Recorded answers

<div class="cjf-results" tabindex="0" role="region" aria-label="CQ3 supported Claims recorded answers" data-csv-source="CQAnswers/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.answers.csv">
  <p class="cjf-results-status" role="status">Loading recorded answers…</p>
</div>
<noscript><p>Enable JavaScript to view the recorded answer table, or use the CSV download below.</p></noscript>

<p class="cjf-downloads">Downloads: <a href="CQAnswers/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.snap.rq">SPARQL query (.rq)</a> · <a href="CQAnswers/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.answers.csv">Recorded answers (.csv)</a></p>

The first query finds Claims that support or challenge Platform A and shows their current states and summaries. Property chains infer the `supports`, `challenges`, and `hasState` links used by the query. The second query keeps Claims whose current state is `Supported`. A Claim can challenge Platform A and still have a Supported state. The recorded answers contain six supporting and three challenging Claims; five supporting Claims and one challenging Claim have a Supported current state.

## CQ5 Speakers Agreeing with the Selected Option

**Question:** For the final platform-selection Outcome, which speakers explicitly agreed with its selected Option, and which ExpressedPosition moves and source turns provide the evidence?

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

The remaining competency questions and their scenarios are described in the [current use case](usecase.html#competency-questions).
