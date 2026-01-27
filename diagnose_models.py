#!/usr/bin/env python3
"""
Model Diagnostic Script for Modeling_2026
==========================================

This script diagnoses why processor models fail to load.
Run this to identify import errors, syntax errors, or missing dependencies.

Usage:
    python diagnose_models.py [repo_path] [--processor NAME] [--fix]
"""

import os
import sys
import ast
import argparse
from pathlib import Path


def check_syntax(file_path: Path) -> tuple:
    """Check Python file for syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def check_imports(file_path: Path) -> list:
    """Extract and check imports from a Python file"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name
                    try:
                        __import__(module)
                    except ImportError as e:
                        issues.append(f"Import '{module}': {e}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                # Check if it's a relative import from common or similar
                if module.startswith('common') or module.startswith('.'):
                    issues.append(f"Relative/local import: 'from {module} import ...' - may need path setup")
                elif module:
                    try:
                        __import__(module)
                    except ImportError as e:
                        # Skip common local imports
                        if 'common' not in module and 'base_model' not in module:
                            issues.append(f"Import 'from {module}': {e}")
    except Exception as e:
        issues.append(f"Parse error: {e}")
    
    return issues


def try_load_model(file_path: Path) -> tuple:
    """Attempt to load a model file and report detailed errors"""
    import importlib.util
    
    try:
        # Add parent directories to path
        repo_root = file_path.parent.parent.parent.parent  # Go up to repo root
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        
        # Also add the processor's parent (family) directory
        family_dir = file_path.parent.parent.parent
        if str(family_dir) not in sys.path:
            sys.path.insert(0, str(family_dir))
        
        spec = importlib.util.spec_from_file_location("model", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find model class
        model_classes = [name for name in dir(module) if name.endswith('Model') and isinstance(getattr(module, name), type)]
        
        if model_classes:
            return True, f"Found model class(es): {model_classes}"
        elif hasattr(module, 'analyze'):
            return True, "Found analyze() function"
        else:
            return True, "Module loaded but no Model class or analyze() found"
            
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except ImportError as e:
        return False, f"Import error: {e}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def diagnose_processor(processor_path: Path, processor_name: str, verbose: bool = True):
    """Diagnose a single processor model"""
    print(f"\n{'='*60}")
    print(f"Diagnosing: {processor_name}")
    print(f"Path: {processor_path}")
    print('='*60)
    
    current_dir = processor_path / 'current'
    if not current_dir.exists():
        print("❌ No 'current/' directory found")
        return False
    
    model_files = list(current_dir.glob('*_validated.py'))
    if not model_files:
        print("❌ No *_validated.py file found")
        return False
    
    model_file = model_files[0]
    print(f"📄 Model file: {model_file.name}")
    
    # Step 1: Syntax check
    print("\n1️⃣  Checking syntax...")
    syntax_ok, syntax_error = check_syntax(model_file)
    if syntax_ok:
        print("   ✅ Syntax OK")
    else:
        print(f"   ❌ Syntax Error: {syntax_error}")
        return False
    
    # Step 2: Check imports
    print("\n2️⃣  Checking imports...")
    import_issues = check_imports(model_file)
    if import_issues:
        for issue in import_issues:
            print(f"   ⚠️  {issue}")
    else:
        print("   ✅ No obvious import issues")
    
    # Step 3: Try to load
    print("\n3️⃣  Attempting to load module...")
    load_ok, load_result = try_load_model(model_file)
    if load_ok:
        print(f"   ✅ {load_result}")
    else:
        print(f"   ❌ {load_result}")
    
    # Step 4: Show first few lines of file for context
    if verbose:
        print("\n4️⃣  File header (first 30 lines):")
        print("-" * 40)
        try:
            with open(model_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    if i > 30:
                        print("   ... (truncated)")
                        break
                    print(f"   {i:3}: {line.rstrip()}")
        except Exception as e:
            print(f"   Error reading file: {e}")
    
    return load_ok


def main():
    parser = argparse.ArgumentParser(description='Diagnose model loading issues')
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--processor', '-p', help='Specific processor to diagnose')
    parser.add_argument('--family', '-f', help='Specific family to diagnose')
    parser.add_argument('--all', '-a', action='store_true', help='Diagnose all processors')
    parser.add_argument('--quiet', '-q', action='store_true', help='Less verbose output')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    print("MODEL DIAGNOSTIC TOOL")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    
    families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
    
    if args.processor:
        # Find specific processor
        for family in families:
            proc_path = repo_path / family / args.processor
            if proc_path.exists():
                diagnose_processor(proc_path, args.processor, not args.quiet)
                break
        else:
            print(f"Processor not found: {args.processor}")
    elif args.family:
        # Diagnose specific family
        family_path = repo_path / args.family
        if family_path.exists():
            for item in sorted(family_path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    diagnose_processor(item, item.name, not args.quiet)
        else:
            print(f"Family not found: {args.family}")
    elif args.all:
        # Diagnose all
        success = 0
        total = 0
        for family in families:
            family_path = repo_path / family
            if family_path.exists():
                for item in sorted(family_path.iterdir()):
                    if item.is_dir() and not item.name.startswith('.'):
                        total += 1
                        if diagnose_processor(item, item.name, not args.quiet):
                            success += 1
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {success}/{total} processors loaded successfully")
    else:
        # Default: diagnose first processor found for quick test
        print("\nNo processor specified. Diagnosing first Intel processor as example...")
        intel_path = repo_path / 'intel'
        if intel_path.exists():
            for item in sorted(intel_path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    diagnose_processor(item, item.name, not args.quiet)
                    break
        print("\nUse --processor NAME, --family NAME, or --all for more diagnostics")


if __name__ == '__main__':
    main()
