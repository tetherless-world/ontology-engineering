(() => {
  "use strict";
  const get = (id) => document.getElementById(id);
  const svgNS = "http://www.w3.org/2000/svg";
  const question = get("question");
  const example = get("example");
  const step = get("step");
  const nextStep = get("next-step");

  const titles = ["Moves and states", "Issue evidence", "Claims about Platform A",
    "Issue histories", "Agreement with the outcome", "Speaker C’s positions"];

  function svg(tag, attrs = {}) {
    const node = document.createElementNS(svgNS, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    return node;
  }

  function showGraph(q, witness, stage) {
    const graph = get("graph");
    graph.replaceChildren();
    graph.setAttribute("viewBox", "0 0 " + q.size.join(" "));
    const active = q.steps.slice(0, stage + 1);
    const nodes = new Set(active.flatMap(s => s.nodes));
    const edges = new Set(active.flatMap(s => s.edges));
    const defs = svg("defs");
    const marker = svg("marker", {id: "arrow", viewBox: "0 0 10 10", refX: 9, refY: 5,
      markerWidth: 5, markerHeight: 5, orient: "auto"});
    marker.append(svg("path", {d: "M0 0 L10 5 L0 10 Z", fill: "#40555b"}));
    defs.append(marker);
    graph.append(defs);
    for (const edge of q.edges) {
      const origin = witness.edges[edge.id];
      if (!origin || !edges.has(edge.id)) continue;
      const label = svg("text", {x: edge.x, y: edge.y, "text-anchor": "middle"});
      label.textContent = witness.edgeLabels?.[edge.id] ?? edge.predicate;
      graph.append(svg("path", {d: edge.d, class: "edge " + origin, "marker-end": "url(#arrow)"}), label);
    }
    for (const node of q.nodes) {
      const term = witness.terms[node.id];
      if (!nodes.has(node.id) || !term) continue;
      const box = svg("foreignObject", {x: node.x, y: node.y, width: node.w, height: node.h});
      const button = document.createElement("button");
      button.className = "node " + term.origin;
      const heading = document.createElement("strong");
      heading.textContent = node.title;
      const value = document.createElement("span");
      value.textContent = term.display ?? term.value;
      button.append(heading, value);
      button.title = term.value;
      button.addEventListener("click", () => {
        graph.querySelector("[aria-pressed=true]")?.setAttribute("aria-pressed", "false");
        button.setAttribute("aria-pressed", "true");
        get("detail").textContent = node.title + " (" + term.origin + ") · " + term.value;
      });
      button.setAttribute("aria-pressed", "false");
      box.append(button);
      graph.append(box);
    }
  }

  function render() {
    const q = classroomGraphs.questions[question.selectedIndex];
    const witness = q.examples[example.selectedIndex];
    nextStep.textContent = step.selectedIndex === q.steps.length - 1 ? "Restart steps" : "Next step";
    showGraph(q, witness, step.selectedIndex);
    const bindings = get("answer");
    bindings.replaceChildren();
    for (const [key, value] of Object.entries(witness.answer)) {
      const name = document.createElement("dt");
      const term = document.createElement("dd");
      name.textContent = "?" + key;
      term.textContent = value || "Unbound";
      bindings.append(name, term);
    }
    get("ask").textContent = q.question;
    get("detail").textContent = "Select a graph node to see its full value and origin.";
    get("code").textContent = q.steps[step.selectedIndex].code;
    get("query-file").href = q.query;
    get("result-file").href = q.csv;
  }

  function selectQuestion() {

    const q = classroomGraphs.questions[question.selectedIndex];
    example.replaceChildren(...q.examples.map(w => new Option(w.label)));
    step.replaceChildren(...q.steps.map((s, i) => new Option((i + 1) + ". " + s.title)));
    step.selectedIndex = 0;
    render();
  }

  nextStep.addEventListener("click", () => {
    step.selectedIndex = (step.selectedIndex + 1) % step.options.length;
    render();
  });
  for (const q of classroomGraphs.questions) {
    question.add(new Option("CQ" + q.id + " · " + titles[q.id - 1], String(q.id)));
  }
  const initial = /^#cq([1-6])$/i.exec(location.hash);
  question.value = initial?.[1] ?? "5";
  question.addEventListener("change", selectQuestion);
  example.addEventListener("change", render);
  step.addEventListener("change", render);
  selectQuestion();
})();
