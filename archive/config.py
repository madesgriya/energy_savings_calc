import json

def parse(eui_file):
    with open(eui_file) as f:
        cfg = json.load(f)
        return cfg 