"""Atomic file publication and input/output separation."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import tempfile
from .models import OutputWriteError


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_destination(path, *, inputs=(), overwrite=False):
    path = Path(path).resolve()
    if path in {Path(p).resolve() for p in inputs if p is not None}:
        raise OutputWriteError(f"Output must not overwrite an input: {path}")
    if path.exists() and not overwrite:
        raise OutputWriteError(f"Output exists; use overwrite=True/--overwrite: {path}")
    return path


def atomic_bytes(path, data):
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + target.name + ".", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path, data):
    atomic_bytes(path, (json.dumps(data, indent=2, default=str, ensure_ascii=False) + "\n").encode("utf-8"))


def rdf_format(path, explicit=None):
    if explicit:
        if explicit not in {"xml", "turtle", "nt", "json-ld"}:
            raise OutputWriteError(f"Unsupported RDF format {explicit}")
        return explicit
    extension = Path(path).suffix.lower()
    if extension not in {".rdf", ".owl", ".xml", ".ttl", ".nt", ".jsonld"}:
        raise OutputWriteError("Use an RDF extension (.rdf/.owl/.ttl/.nt/.jsonld) or configure ontology.format")
    return {".rdf": "xml", ".owl": "xml", ".xml": "xml", ".ttl": "turtle", ".nt": "nt", ".jsonld": "json-ld"}[extension]


def save_graph(graph, output):
    atomic_bytes(output, graph.serialize(format=rdf_format(output), encoding="utf-8"))
