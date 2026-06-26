import json
import os

def list_maps(maps_dir='maps'):
    return sorted([
        f[:-5] for f in os.listdir(maps_dir) if f.endswith('.json')
    ])

def load_map(name, maps_dir='maps'):
    path = os.path.join(maps_dir, name + '.json')
    with open(path) as f:
        return json.load(f)
