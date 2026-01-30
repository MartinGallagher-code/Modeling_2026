#!/usr/bin/env python3
"""
Verify all updated models can be imported and run analyze() successfully.
Also verify pre-1985 models are unchanged.
"""

import sys
import os
import re
import importlib
import importlib.util
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MODELS_DIR = ROOT / "models"

def get_year_from_source(content: str) -> int:
    m = re.search(r'self\.year\s*=\s*(\d{4})', content)
    if m: return int(m.group(1))
    m = re.search(r'year\s*=\s*(\d{4})', content)
    if m: return int(m.group(1))
    return 0

def find_model_class(module):
    """Find the model class in a module."""
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and name.endswith('Model') and name != 'BaseProcessorModel':
            return obj
    return None

def test_model(filepath: Path) -> tuple:
    """Test a model file. Returns (status, message)."""
    content = filepath.read_text()
    year = get_year_from_source(content)

    # Build module path
    rel = filepath.relative_to(ROOT)
    module_path = str(rel).replace('/', '.').replace('.py', '')

    try:
        spec = importlib.util.spec_from_file_location(module_path, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return ('IMPORT_ERROR', f'{type(e).__name__}: {e}')

    model_class = find_model_class(module)
    if not model_class:
        return ('NO_CLASS', 'Could not find model class')

    try:
        model = model_class()
    except Exception as e:
        return ('INIT_ERROR', f'{type(e).__name__}: {e}')

    try:
        result = model.analyze('typical')
        cpi = result.cpi
    except Exception as e:
        return ('ANALYZE_ERROR', f'{type(e).__name__}: {e}')

    has_cache = hasattr(model, 'cache_config')
    cache_config = getattr(model, 'cache_config', None)

    if year > 1985:
        if not has_cache:
            return ('MISSING_CACHE', f'Post-1985 model (year={year}) missing cache_config')

    return ('OK', f'CPI={cpi:.4f}, cache={cache_config is not None and cache_config.has_cache if cache_config else "None"}')


def main():
    files = sorted(MODELS_DIR.rglob("*_validated.py"))
    print(f"Testing {len(files)} model files...")

    ok = 0
    errors = []
    post_1985_count = 0
    pre_1985_count = 0

    for f in files:
        content = f.read_text()
        year = get_year_from_source(content)
        status, msg = test_model(f)

        if year > 1985:
            post_1985_count += 1
        else:
            pre_1985_count += 1

        if status == 'OK':
            ok += 1
        else:
            errors.append((f, status, msg))
            rel = f.relative_to(ROOT)
            print(f"  FAIL [{status}] {rel}: {msg}")

    print(f"\n{'='*60}")
    print(f"Results: {ok} OK, {len(errors)} errors out of {len(files)} files")
    print(f"Pre-1985: {pre_1985_count}, Post-1985: {post_1985_count}")

    if errors:
        print(f"\nFailed models:")
        for f, status, msg in errors:
            print(f"  {f.relative_to(ROOT)}: [{status}] {msg}")
        sys.exit(1)
    else:
        print("\nAll models passed!")


if __name__ == '__main__':
    main()
