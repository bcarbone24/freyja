#!/usr/bin/env python3
"""Read a kicadsexpr netlist with its layout flattened to one canonical form.

KiCad 9 writes `(comp (ref "C1")`; KiCad 10 puts every token on its own line.
Collapsing whitespace outside quoted strings makes both read the same, so the
callers' regexes work on either version."""
import re

_TOK = re.compile(r'"(?:[^"\\]|\\.)*"|\s+')

def read(path):
    t = open(path, encoding='utf-8').read()
    t = _TOK.sub(lambda m: m.group(0) if m.group(0).startswith('"') else ' ', t)
    return t.replace('( ', '(').replace(' )', ')')
