#!/usr/bin/env python3
"""
Debug Model Loading - Shows full traceback for the unhashable dict error
"""

import sys
import traceback
from pathlib import Path
import importlib.util

def try_load_with_traceback(model_path: Path, repo_root: Path):
    """Try to load a model and show full traceback on error"""
    print(f"Loading: {model_path}")
    print("=" * 60)
    
    # Add repo root to path
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    
    try:
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        print("1. Module spec created OK")
        
        spec.loader.exec_module(module)
        print("2. Module loaded OK")
        
        # Find model class
        for name in dir(module):
            if name.endswith('Model') and name != 'BaseProcessorModel':
                obj = getattr(module, name)
                if isinstance(obj, type):
                    print(f"3. Found class: {name}")
                    print(f"4. Attempting to instantiate {name}()...")
                    instance = obj()
                    print(f"5. SUCCESS! Instance created: {instance}")
                    return True
        
        print("No Model class found")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        print("\n" + "=" * 60)
        print("FULL TRACEBACK:")
        print("=" * 60)
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_model_load.py <repo_path> [processor_name]")
        print("Example: python debug_model_load.py . i8086")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1]).resolve()
    processor = sys.argv[2] if len(sys.argv) > 2 else None
    
    if processor:
        # Find specific processor
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            model_dir = repo_path / family / processor / 'current'
            if model_dir.exists():
                model_files = list(model_dir.glob('*_validated.py'))
                if model_files:
                    try_load_with_traceback(model_files[0], repo_path)
                    return
        print(f"Processor not found: {processor}")
    else:
        # Try first Intel processor
        for family in ['intel']:
            family_path = repo_path / family
            if family_path.exists():
                for proc_dir in sorted(family_path.iterdir()):
                    if proc_dir.is_dir():
                        model_dir = proc_dir / 'current'
                        if model_dir.exists():
                            model_files = list(model_dir.glob('*_validated.py'))
                            if model_files:
                                try_load_with_traceback(model_files[0], repo_path)
                                return

if __name__ == '__main__':
    main()
