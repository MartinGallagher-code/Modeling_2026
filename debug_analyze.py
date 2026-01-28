#!/usr/bin/env python3
"""Debug why model.analyze() is failing"""

import sys
import traceback
from pathlib import Path
import importlib.util

def debug_model(repo_path: Path, processor: str):
    """Debug a specific model's analyze method"""
    
    # Add repo to path
    if str(repo_path) not in sys.path:
        sys.path.insert(0, str(repo_path))
    
    # Find model
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        model_dir = repo_path / family / processor / 'current'
        if model_dir.exists():
            model_files = list(model_dir.glob('*_validated.py'))
            if model_files:
                model_path = model_files[0]
                print(f"Found: {model_path}")
                break
    else:
        print(f"Processor not found: {processor}")
        return
    
    # Load model
    print("\n1. Loading module...")
    try:
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("   ✅ Module loaded")
    except Exception as e:
        print(f"   ❌ Module load failed: {e}")
        traceback.print_exc()
        return
    
    # Find model class
    print("\n2. Finding model class...")
    model_class = None
    for name in dir(module):
        if name.endswith('Model') and name != 'BaseProcessorModel':
            obj = getattr(module, name)
            if isinstance(obj, type):
                model_class = obj
                print(f"   ✅ Found: {name}")
                break
    
    if not model_class:
        print("   ❌ No model class found")
        return
    
    # Instantiate
    print("\n3. Instantiating model...")
    try:
        model = model_class()
        print(f"   ✅ Instance created: {model}")
    except Exception as e:
        print(f"   ❌ Instantiation failed: {e}")
        traceback.print_exc()
        return
    
    # Check attributes
    print("\n4. Checking model attributes...")
    print(f"   Has analyze: {hasattr(model, 'analyze')}")
    print(f"   Has instruction_categories: {hasattr(model, 'instruction_categories')}")
    print(f"   Has workload_profiles: {hasattr(model, 'workload_profiles')}")
    
    if hasattr(model, 'instruction_categories'):
        cats = model.instruction_categories
        print(f"   Instruction categories: {type(cats)} with {len(cats) if cats else 0} items")
        if cats:
            for k, v in list(cats.items())[:3]:
                print(f"      - {k}: {v}")
    
    if hasattr(model, 'workload_profiles'):
        profiles = model.workload_profiles
        print(f"   Workload profiles: {type(profiles)} with {len(profiles) if profiles else 0} items")
        if profiles:
            for k in list(profiles.keys())[:3]:
                print(f"      - {k}")
    
    # Try analyze
    print("\n5. Calling analyze('typical')...")
    try:
        result = model.analyze('typical')
        print(f"   ✅ Result: {result}")
        if result:
            print(f"   CPI: {getattr(result, 'cpi', 'N/A')}")
            print(f"   IPC: {getattr(result, 'ipc', 'N/A')}")
    except Exception as e:
        print(f"   ❌ analyze() failed: {e}")
        print("\n   FULL TRACEBACK:")
        traceback.print_exc()
    
    # Try other workloads
    print("\n6. Trying other workloads...")
    for workload in ['compute', 'memory', 'mixed', 'default']:
        try:
            result = model.analyze(workload)
            if result and hasattr(result, 'cpi') and result.cpi:
                print(f"   ✅ '{workload}' worked: CPI={result.cpi}")
                break
        except Exception as e:
            print(f"   ❌ '{workload}': {type(e).__name__}")

def main():
    repo_path = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    processor = sys.argv[2] if len(sys.argv) > 2 else 'i8086'
    
    print("=" * 60)
    print(f"DEBUG MODEL ANALYZE: {processor}")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    
    debug_model(repo_path, processor)

if __name__ == '__main__':
    main()
