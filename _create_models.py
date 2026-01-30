
import os, json, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))

def w(path, text):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)
    print(f"  Written: {path}")

print("Creating 8 processor models...")
print("=" * 60)
