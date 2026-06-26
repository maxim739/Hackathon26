import json
import os
import sys

def _maps_dir(maps_dir='maps'):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # _MEIPASS puts us at bundle root; without it we're in logic/, so go up one
    if not hasattr(sys, '_MEIPASS'):
        base = os.path.dirname(base)
    return os.path.join(base, maps_dir)

def list_maps(maps_dir='maps'):
    d = _maps_dir(maps_dir)
    return sorted([f[:-5] for f in os.listdir(d) if f.endswith('.json')])

def load_map(name, maps_dir='maps'):
    path = os.path.join(_maps_dir(maps_dir), name + '.json')
    with open(path) as f:
        return json.load(f)
