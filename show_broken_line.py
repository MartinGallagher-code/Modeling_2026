#!/usr/bin/env python3
"""Show the exact broken line with its indentation"""
import sys
from pathlib import Path

repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()

for family, proc in [('intel', 'i80286'), ('motorola', 'm68000')]:
    path = repo / family / proc / 'current' / f'{proc}_validated.py'
    if path.exists():
        with open(path) as f:
            lines = f.readlines()
        
        print(f"\n{proc}:")
        for i, line in enumerate(lines):
            if 'base_cpi' in line and 'pipeline_stages' in line:
                print(f"  Line {i+1}: {repr(line)}")
                # Show surrounding context
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    marker = ">>>" if j == i else "   "
                    print(f"  {marker} {j+1}: {lines[j].rstrip()}")
                break
