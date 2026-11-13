#!/usr/bin/env python3
"""Footprint field access that works on both KiCad 9 and KiCad 10 pcbnew.

KiCad 10 dropped GetFieldByName/HasFieldByName/AddField/RemoveField/
GetNextFieldId; fields are now looked up by name with GetField/HasField and
attached or detached like any other footprint item."""
import pcbnew

def get(fp, name):
    if hasattr(fp, 'GetFieldByName'): return fp.GetFieldByName(name)
    return fp.GetField(name)

def has(fp, name):
    if hasattr(fp, 'HasFieldByName'): return fp.HasFieldByName(name)
    return fp.HasField(name)

def new(fp, name):
    """A new, attached user field."""
    if hasattr(fp, 'AddField'):
        return fp.AddField(pcbnew.PCB_FIELD(fp, fp.GetNextFieldId(), name))
    field = pcbnew.PCB_FIELD(fp, pcbnew.FIELD_T_USER, name)
    fp.Add(field)
    return get(fp, name)

def remove(fp, name):
    if hasattr(fp, 'RemoveField'): fp.RemoveField(name)
    else: fp.Remove(get(fp, name))
