#!/usr/bin/env python3
"""Lowercase and space out rdfs:label values, but only on entities defined in
this ontology (IRIs under the base URI). Labels on imported entities are left alone.

Usage: python3 normalize_labels.py [--base <IRI>] <file.rdf> [more files...]
Edits files in place. The base defaults to the file's xml:base attribute.
Example: "hasPolicyAssessment" -> "has policy assessment".
"""
import re
import sys

BLOCK_RE = re.compile(
    r'^(\s*)<([\w:\-]+)\s+rdf:about="([^"]*)"[^>]*(?<!/)>(.*?)^\1</\2>',  # (?<!/) skips self-closing tags
    re.S | re.M,
)
LABEL_RE = re.compile(r'(<rdfs:label(?:\s[^>]*)?>)([^<]*)(</rdfs:label>)')
XML_BASE_RE = re.compile(r'xml:base="([^"]*)"')


def normalize(text: str) -> str:
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)       # camelCase -> camel Case
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)    # HVACSystem -> HVAC System
    text = re.sub(r'[_\-]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()


def is_local(about: str, base: str) -> bool:
    # Absolute IRI under the base, or a relative IRI (resolved against xml:base).
    return about.startswith(base) or '://' not in about


def process(path: str, base: str | None) -> tuple[int, int]:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if base is None:
        m = XML_BASE_RE.search(content)
        if not m:
            sys.exit(f'{path}: no xml:base found; pass --base <IRI>')
        base = m.group(1)

    changed = skipped = 0

    def label_repl(m):
        nonlocal changed
        new = normalize(m.group(2))
        if new != m.group(2):
            changed += 1
        return m.group(1) + new + m.group(3)

    def block_repl(m):
        nonlocal skipped
        indent, tag, about, body = m.groups()
        if not is_local(about, base):
            skipped += len(LABEL_RE.findall(body))
            return m.group(0)
        whole = m.group(0)
        start, end = m.start(4) - m.start(0), m.end(4) - m.start(0)
        return whole[:start] + LABEL_RE.sub(label_repl, body) + whole[end:]

    result = BLOCK_RE.sub(block_repl, content)
    if result != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(result)
    return changed, skipped


if __name__ == '__main__':
    args = sys.argv[1:]
    base = None
    if args[:1] == ['--base']:
        base = args[1]
        args = args[2:]
    if not args:
        sys.exit(__doc__)
    for p in args:
        changed, skipped = process(p, base)
        print(f'{p}: {changed} label(s) changed, {skipped} imported label(s) left as-is')
