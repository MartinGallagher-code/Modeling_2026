#!/usr/bin/env python3
"""Diagnose why pipelined models aren't responding to calibration"""
import sys
from pathlib import Path
import importlib.util

def diagnose(repo_path, proc_name):
    # Add to path
    if str(repo_path) not in sys.path:
        sys.path.insert(0, str(repo_path))
    
    # Find model
    for family in ['intel', 'motorola', 'other']:
        model_path = repo_path / family / proc_name / 'current' / f'{proc_name}_validated.py'
        if model_path.exists():
            break
    else:
        print(f"Not found: {proc_name}")
        return
    
    # Load
    spec = importlib.util.spec_from_file_location("model", model_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    model = None
    for name in dir(module):
        if name.endswith('Model') and name != 'BaseProcessorModel':
            model = getattr(module, name)()
            break
    
    if not model:
        print("No model class")
        return
    
    print(f"\n{'='*60}")
    print(f"DIAGNOSIS: {proc_name}")
    print(f"{'='*60}")
    
    # Check what parameters exist
    print("\n1. Model attributes:")
    for attr in dir(model):
        if not attr.startswith('_') and not callable(getattr(model, attr)):
            val = getattr(model, attr)
            if isinstance(val, (int, float, str)):
                print(f"   {attr}: {val}")
    
    # Check instruction categories
    print("\n2. Instruction categories:")
    if hasattr(model, 'instruction_categories'):
        for name, cat in model.instruction_categories.items():
            print(f"   {name}: base={cat.base_cycles}, mem={getattr(cat, 'memory_cycles', 'N/A')}")
    
    # Run analyze and show internals
    print("\n3. Analyze internals:")
    try:
        # Get the source of analyze method
        import inspect
        analyze_src = inspect.getsource(model.analyze)
        
        # Find what drives CPI calculation
        if 'return' in analyze_src:
            # Extract the CPI calculation logic
            lines = analyze_src.split('\n')
            for i, line in enumerate(lines):
                if 'cpi' in line.lower() or 'total' in line.lower():
                    print(f"   Line {i}: {line.strip()}")
    except:
        pass
    
    # Test if changing base_cycles affects output
    print("\n4. Parameter sensitivity test:")
    
    original_cpi = model.analyze('typical').cpi
    print(f"   Original CPI: {original_cpi:.4f}")
    
    # Double all base_cycles
    if hasattr(model, 'instruction_categories'):
        for cat in model.instruction_categories.values():
            cat.base_cycles *= 2
        
        new_cpi = model.analyze('typical').cpi
        print(f"   After 2x base_cycles: {new_cpi:.4f}")
        print(f"   Change: {(new_cpi - original_cpi) / original_cpi * 100:.1f}%")
        
        # Restore
        for cat in model.instruction_categories.values():
            cat.base_cycles /= 2

if __name__ == '__main__':
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    proc = sys.argv[2] if len(sys.argv) > 2 else 'i80286'
    diagnose(repo, proc)
