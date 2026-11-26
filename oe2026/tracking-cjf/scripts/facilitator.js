(() => {
  "use strict";

  const CJF = "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/";
  const RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
  const PROV = "http://www.w3.org/ns/prov#";
  const STATES = ["Resolved", "Addressed", "Open"];

  function properties(node, name, namespace = CJF) {
    return Array.from(node?.children ?? []).filter(
      (child) => child.namespaceURI === namespace && child.localName === name
    );
  }

  function references(node, name, namespace = CJF) {
    return properties(node, name, namespace).map((child) => child.getAttributeNS(RDF, "resource"));
  }

  function value(node, name) {
    return properties(node, name)[0]?.textContent.trim() ?? "";
  }

  function hasType(node, name) {
    return (node?.namespaceURI === CJF && node.localName === name) ||
      references(node, "type", RDF).includes(CJF + name);
  }

  function readDiscussion(xml) {
    const doc = new DOMParser().parseFromString(xml, "application/xml");
    if (doc.documentElement.namespaceURI !== RDF || doc.querySelector("parsererror")) {
      throw new Error("Invalid sample RDF/XML");
    }

    const resources = new Map(Array.from(doc.documentElement.children, (node) => [
      node.getAttributeNS(RDF, "about"), node
    ]));
    const nodes = Array.from(resources.values());
    const turns = new Map();
    for (const [id, node] of resources) {
      if (!hasType(node, "Utterance")) continue;
      const speaker = resources.get(references(node, "wasAttributedTo", PROV)[0]);
      turns.set(id, {
        number: Number(value(node, "hasTurnNumber")),
        speaker: value(speaker, "hasSpeakerName"),
        text: value(node, "hasConversationText")
      });
    }

    const outcomes = new Set(nodes.filter((node) => hasType(node, "Outcome"))
      .flatMap((node) => references(node, "makesResolves")));
    const issues = [];

    for (const [id, node] of resources) {
      if (!hasType(node, "Issue")) continue;
      const opened = turns.get(references(node, "hasUtterance")[0]);
      if (!opened) continue;

      // The current assignment and its predecessor links give the validated history order.
      const history = [];
      const visited = new Set();
      let assignmentId = references(node, "hasCurrentStateAssignment")[0];
      while (assignmentId) {
        if (visited.has(assignmentId)) throw new Error("Cyclic issue-state history");
        visited.add(assignmentId);
        const assignment = resources.get(assignmentId);
        const effectiveTurn = turns.get(references(assignment, "assignedAtUtterance")[0]);
        if (!effectiveTurn) throw new Error("Missing effective turn in issue-state history");
        history.push({ assignment, effectiveTurn });
        assignmentId = references(assignment, "hasPreviousAssignment")[0];
      }

      let previousStates = new Set();
      for (const event of history.reverse()) {
        const { assignment, effectiveTurn } = event;
        const state = resources.get(references(assignment, "assignedState")[0]);
        const states = new Set(STATES.filter((name) => hasType(state, name)));
        const triggers = references(assignment, "hasTriggeringRelationship");

        // Apply the sample ontology's two issue transitions to the recorded assignment chain.
        if ((previousStates.has("Open") || previousStates.has("Addressed")) &&
            triggers.some((trigger) => hasType(resources.get(trigger), "Address"))) {
          states.add("Addressed");
        }
        if (previousStates.has("Addressed") && triggers.some((trigger) => {
          const relationship = resources.get(trigger);
          return outcomes.has(trigger) && hasType(relationship, "Resolve") &&
            references(relationship, "isAimedAtResolves").includes(id);
        })) {
          states.add("Resolved");
        }

        const evidence = references(assignment, "hasStateEvidence")
          .flatMap((span) => references(resources.get(span), "isPartOfUtterance"))
          .map((utterance) => turns.get(utterance))
          .filter((turn) => turn && turn.number <= effectiveTurn.number);
        event.evidence = Array.from(new Set(evidence)).sort((a, b) => a.number - b.number);
        event.state = STATES.find((name) => states.has(name)) ?? "Unclassified";
        previousStates = states;
      }

      issues.push({ summary: value(node, "hasSummary"), opened, history });
    }

    if (!turns.size || !issues.length) throw new Error("The sample has no discussion issues");
    return { turns: Array.from(turns.values()).sort((a, b) => a.number - b.number), issues };
  }

  function element(tag, content) {
    const node = document.createElement(tag);
    if (content !== undefined) node.textContent = content;
    return node;
  }

  function turnText(turn) {
    return `Turn ${turn.number} · ${turn.speaker} — ${turn.text}`;
  }

  function renderEvidence(turns, expanded = false) {
    const details = element("details");
    details.open = expanded;
    const turnNumbers = turns.map((turn) => turn.number).join(", ");
    const label = turns.length === 1 ? "Evidence from turn" : "Evidence from turns";
    details.append(element("summary", `${label} ${turnNumbers}`));
    const list = element("ul");
    for (const turn of turns) list.append(element("li", turnText(turn)));
    details.append(list);
    return details;
  }

  function renderDiscussion(root, discussion) {
    const get = (name) => root.querySelector(`#facilitator-${name}`);
    const { turns, issues } = discussion;
    const select = get("turn");
    const previous = get("previous");
    const next = get("next");
    const suggestion = get("suggestion");
    const issueList = get("issues");

    for (const turn of turns) select.append(element("option", `Turn ${turn.number}`));
    select.selectedIndex = turns.length - 1;

    function render() {
      const index = select.selectedIndex;
      const turn = turns[index];
      previous.disabled = index === 0;
      next.disabled = index === turns.length - 1;
      get("utterance").textContent = turnText(turn);

      const visible = issues.filter(({ opened }) => opened.number <= turn.number)
        .map((issue) => {
          const latest = issue.history.findLast((event) => event.effectiveTurn.number <= turn.number);
          return {
            ...issue,
            state: latest?.state ?? "Unclassified",
            evidence: latest?.evidence.length ? latest.evidence : [issue.opened]
          };
        });
      visible.sort((a, b) => b.opened.number - a.opened.number);
      const open = visible.find((issue) => issue.state === "Open");

      if (open) {
        suggestion.replaceChildren(element("p", open.summary),
          element("p", "What information or action would settle this issue?"),
          renderEvidence(open.evidence, true));
      } else {
        suggestion.replaceChildren(element("p", "There is no recorded open issue at this turn."));
      }

      issueList.replaceChildren();
      for (const issue of visible) {
        const item = element("div");
        item.className = "facilitator-issue";
        const heading = element("p");
        const badge = element("span", issue.state);
        badge.className = "facilitator-state";
        badge.dataset.state = issue.state;
        heading.append(badge, issue.summary);
        item.append(heading, renderEvidence(issue.evidence));
        issueList.append(item);
      }
      if (!visible.length) issueList.append(element("p", "No issues have been raised yet."));
      get("status").textContent = `Showing ${visible.length} ${visible.length === 1 ? "issue" : "issues"} through turn ${turn.number}.`;
    }

    select.addEventListener("change", render);
    previous.addEventListener("click", () => { select.selectedIndex -= 1; render(); });
    next.addEventListener("click", () => { select.selectedIndex += 1; render(); });
    get("replay").hidden = false;
    render();
  }

  const root = document.querySelector("#cjf-facilitator");
  const status = root.querySelector("#facilitator-status");

  async function loadDiscussion() {
    for (const week of [13, 12]) {
      const path = `ontology/OE_${week}_TeamCJF_Individuals.rdf`;
      const response = await fetch(path);
      if (response.status === 404) continue;
      if (!response.ok) throw new Error(`Sample RDF returned HTTP ${response.status}`);
      renderDiscussion(root, readDiscussion(await response.text()));
      const source = element("a", `OE Week ${week} sample RDF`);
      source.href = path;
      root.querySelector("#facilitator-source").append(" · ", source);
      return;
    }
    throw new Error("No published sample RDF found");
  }

  status.textContent = "Loading the discussion…";
  loadDiscussion().catch((error) => {
    console.error(error);
    status.textContent = "The discussion could not be loaded. Reload the page to try again.";
  });
})();
