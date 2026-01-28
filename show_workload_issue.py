#!/usr/bin/env python3
"""Show the actual workload profile code"""
import sys
from pathlib import Path

repo_path = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()

# Find i8086 model
model_file = repo_path / 'intel' / 'i8086' / 'current' / 'i8086_validated.py'

if model_file.exists():
    with open(model_file, 'r') as f:
        lines = f.readlines()
    
    print("Lines containing 'workload' or 'category_weights':")
    print("=" * 70)
    
    in_workload_section = False
    for i, line in enumerate(lines, 1):
        if 'workload' in line.lower() or 'category_weights' in line:
            in_workload_section = True
        
        if in_workload_section:
            print(f"{i:4}: {line.rstrip()}")
            if line.strip() == '}' or line.strip() == '},':
                in_workload_section = False
                print()
else:
    print(f"File not found: {model_file}")
