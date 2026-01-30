#!/usr/bin/env python3
"""Generate all 8 processor models."""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

def w(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w") as f:
        f.write(content)

# Will be populated by append operations
print("Generator loaded")
