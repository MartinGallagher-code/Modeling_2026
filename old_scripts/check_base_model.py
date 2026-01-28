#!/usr/bin/env python3
"""Check what's in common/base_model.py WorkloadProfile"""
import sys
from pathlib import Path

repo_path = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
base_model = repo_path / 'common' / 'base_model.py'

if base_model.exists():
    with open(base_model, 'r') as f:
        content = f.read()
    
    print(f"File: {base_model}")
    print("=" * 70)
    
    # Find WorkloadProfile class
    lines = content.split('\n')
    in_class = False
    brace_count = 0
    
    for i, line in enumerate(lines, 1):
        if 'class WorkloadProfile' in line:
            in_class = True
        
        if in_class:
            print(f"{i:4}: {line}")
            # Stop after class definition
            if line.strip().startswith('class ') and 'WorkloadProfile' not in line:
                break
            if i > 100:  # Safety limit
                break
else:
    print(f"File not found: {base_model}")
