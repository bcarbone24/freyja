#!/usr/bin/env python3
"""Locate KiCad's stock symbol and footprint libraries on Linux, macOS or Windows.

KICAD<n>_SYMBOL_DIR / KICAD<n>_FOOTPRINT_DIR win if set; otherwise the usual
install locations are searched, newest Windows version first."""
import os, glob

def _env(kind):
    for k in sorted(os.environ, reverse=True):
        if k.startswith('KICAD') and k.endswith(f'_{kind}_DIR') and os.path.isdir(os.environ[k]):
            return [os.environ[k]]
    return []

def _candidates(sub):
    out = [f'/usr/share/kicad/{sub}', f'/usr/local/share/kicad/{sub}',
           f'/Applications/KiCad/KiCad.app/Contents/SharedSupport/{sub}']
    pf = os.environ.get('ProgramFiles', r'C:\Program Files')
    vers = glob.glob(os.path.join(pf, 'KiCad', '*'))
    vers.sort(key=lambda p: [int(x) for x in os.path.basename(p).split('.') if x.isdigit()],
              reverse=True)
    out += [os.path.join(v, 'share', 'kicad', sub) for v in vers]
    return out

def dirs(kind):
    """Existing stock library directories for kind 'SYMBOL' or 'FOOTPRINT'."""
    sub = 'symbols' if kind == 'SYMBOL' else 'footprints'
    seen = []
    for d in _env(kind) + _candidates(sub):
        if os.path.isdir(d) and d not in seen: seen.append(d)
    return seen

def symbol_dir():
    d = dirs('SYMBOL')
    if not d: raise FileNotFoundError('KiCad symbol library directory not found; set KICAD9_SYMBOL_DIR')
    return d[0]

def footprint_dir():
    d = dirs('FOOTPRINT')
    if not d: raise FileNotFoundError('KiCad footprint library directory not found; set KICAD9_FOOTPRINT_DIR')
    return d[0]

def symbol(name):
    return os.path.join(symbol_dir(), name)

def footprint(path):
    return os.path.join(footprint_dir(), path)
