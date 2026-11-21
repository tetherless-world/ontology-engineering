(() => {
  "use strict";

  // Read the canonical CSV downloads, including quoted commas, quoted newlines,
  // escaped quotation marks, UTF-8 BOMs, and CRLF line endings.
  function parseCsv(text) {
    const rows = [];
    let row = [];
    let field = "";
    let quoted = false;
    text = text.replace(/^\uFEFF/, "");

    for (let i = 0; i < text.length; i += 1) {
      const char = text[i];
      if (quoted) {
        if (char === '"' && text[i + 1] === '"') {
          field += '"';
          i += 1;
        } else if (char === '"') {
          quoted = false;
        } else {
          field += char;
        }
      } else if (char === '"' && field.length === 0) {
        quoted = true;
      } else if (char === ",") {
        row.push(field);
        field = "";
      } else if (char === "\n" || char === "\r") {
        row.push(field);
        rows.push(row);
        row = [];
        field = "";
        if (char === "\r" && text[i + 1] === "\n") i += 1;
      } else {
        field += char;
      }
    }
    if (quoted) throw new Error("Incomplete quoted CSV value");
    if (field.length || row.length) {
      row.push(field);
      rows.push(row);
    }
    return rows.filter((values) => values.some((value) => value.trim()));
  }

  async function showAnswers(container) {
    try {
      const response = await fetch(container.dataset.csvSource);
      if (!response.ok) throw new Error(`CSV request failed (${response.status})`);
      const [headers, ...rows] = parseCsv(await response.text());
      if (!headers || rows.some((row) => row.length !== headers.length)) {
        throw new Error("Unexpected CSV columns");
      }

      const columns = headers.map((header, index) => {
        const name = header.trim().replace(/^\?/, "");
        let className = "";
        if (/^(summary|support_text|evidence)$/.test(name)) {
          className = "cjf-result-text";
        } else if (/^(move|issues|pos|option)$/.test(name) || index === 0) {
          className = "cjf-result-identifier";
        } else if (name === "turn") {
          className = "cjf-result-turn";
        }
        return { name, className };
      });

      const table = document.createElement("table");
      const caption = table.createCaption();
      caption.textContent = `Recorded answers (${rows.length} rows)`;
      const heading = table.createTHead().insertRow();
      for (const column of columns) {
        const cell = document.createElement("th");
        cell.scope = "col";
        cell.textContent = column.name;
        cell.className = column.className;
        heading.append(cell);
      }

      const body = table.createTBody();
      for (const values of rows) {
        const row = body.insertRow();
        values.forEach((value, index) => {
          const cell = row.insertCell();
          // Render source values as text so evidence and IRIs cannot become HTML.
          cell.textContent = value.trim();
          cell.className = columns[index].className;
        });
      }
      container.replaceChildren(table);
    } catch (error) {
      container.querySelector(".cjf-results-status").textContent =
        "The recorded answers could not be loaded. Use the CSV download below.";
    }
  }

  document.querySelectorAll("[data-csv-source]").forEach(showAnswers);
})();
