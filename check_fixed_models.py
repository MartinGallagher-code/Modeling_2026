#!/usr/bin/env python3
"""Check if fixed pipelined models are working"""
import sys
import traceback
from pathlib import Path
import importlib.util

def check_model(repo_path, proc_name):
    if str(repo_path) not in sys.path:
        sys.path.insert(0, str(repo_path))
    
    for family in ['intel', 'motorola', 'other']:
        model_path = repo_path / family / proc_name / 'current' / f'{proc_name}_validated.py'
        if model_path.exists():
            break
    else:
        print(f"Not found: {proc_name}")
        return
    
    print(f"\n{'='*60}")
    print(f"CHECKING: {proc_name}")
    print(f"{'='*60}")
    
    # 1. Try to load
    print("\n1. Loading module...")
    try:
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("   ✅ Module loaded")
    except Exception as e:
        print(f"   ❌ LOAD FAILED: {e}")
        traceback.print_exc()
        return
    
    # 2. Instantiate
    print("\n2. Instantiating...")
    try:
        model = None
        for name in dir(module):
            if name.endswith('Model') and name != 'BaseProcessorModel':
                model = getattr(module, name)()
                print(f"   ✅ Created {name}")
                break
        if not model:
            print("   ❌ No model class found")
            return
    except Exception as e:
        print(f"   ❌ INSTANTIATE FAILED: {e}")
        traceback.print_exc()
        return
    
    # 3. Check instruction_categories
    print("\n3. Checking instruction_categories...")
    if hasattr(model, 'instruction_categories'):
        cats = model.instruction_categories
        print(f"   Found {len(cats)} categories")
        for name, cat in list(cats.items())[:3]:
            print(f"   - {name}: base={cat.base_cycles}")
    else:
        print("   ❌ No instruction_categories!")
    
    # 4. Check workload_profiles
    print("\n4. Checking workload_profiles...")
    if hasattr(model, 'workload_profiles'):
        profiles = model.workload_profiles
        print(f"   Found {len(profiles)} profiles: {list(profiles.keys())}")
    else:
        print("   ❌ No workload_profiles!")
    
    # 5. Try analyze
    print("\n5. Running analyze('typical')...")
    try:
        result = model.analyze('typical')
        print(f"   ✅ Result: CPI={result.cpi:.4f}, IPC={result.ipc:.4f}")
    except Exception as e:
        print(f"   ❌ ANALYZE FAILED: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    
    # Check all pipelined processors
    for proc in ['i80286', 'm68000', 'm68008', 'm68010', 'm68020', 'ns32016']:
        check_model(repo, proc)
