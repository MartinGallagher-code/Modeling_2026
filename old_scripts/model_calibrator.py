#!/usr/bin/env python3
"""
Model Calibrator for Modeling_2026
===================================

Automatically calibrates processor model parameters to minimize
the error between predicted and expected CPI values.

Features:
1. Sensitivity analysis - identifies most impactful parameters
2. Auto-calibration - adjusts parameters to match expected CPI
3. Calibration report - documents changes made

Usage:
    python model_calibrator.py [repo_path] --processor i8086 --analyze
    python model_calibrator.py [repo_path] --processor i8086 --calibrate
    python model_calibrator.py [repo_path] --calibrate-all

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import re
import json
import argparse
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import copy


# Expected CPI values from datasheets
EXPECTED_CPI = {
    'i4004': 10.8, 'i4040': 10.5, 'i8008': 11.0, 'i8080': 9.2, 'i8085': 5.5,
    'i8086': 4.5, 'i8088': 5.2, 'i80186': 4.0, 'i80188': 4.2, 'i80286': 4.0,
    'i80386': 4.5, 'i80486': 2.0, 'pentium': 1.0, 'i860': 1.2,
    'mos6502': 3.5, 'mos6510': 3.5, 'wdc65c02': 3.2, 'wdc65816': 3.8,
    'm6800': 4.0, 'm6801': 3.8, 'm6809': 3.5, 'm68000': 6.5, 'm68008': 7.0,
    'm68010': 6.0, 'm68020': 3.5, 'm68030': 3.0, 'm68040': 2.0,
    'z80': 5.5, 'z80a': 5.5, 'z80b': 5.5, 'z180': 4.5, 'z8000': 4.5,
    'arm1': 1.8, 'arm2': 1.5, 'arm3': 1.4, 'sparc': 1.5, 'sun_spark': 1.5,
    'am2901': 1.0, 'f8': 5.0, 'rca1802': 8.0, 'scmp': 6.0,
    'signetics2650': 5.5, 'tms9900': 4.5, 'ns32016': 4.0, 't414': 2.0,
    'r2000': 1.5, 'alpha21064': 1.0, 'hp_pa_risc': 1.2,
}


@dataclass
class CalibrationResult:
    """Results from calibration attempt"""
    processor: str
    original_cpi: float
    calibrated_cpi: float
    expected_cpi: float
    original_error: float
    calibrated_error: float
    parameters_changed: Dict[str, Tuple[float, float]]  # param: (old, new)
    success: bool
    notes: str = ""


@dataclass
class SensitivityResult:
    """Results from sensitivity analysis"""
    parameter: str
    category: str
    base_value: float
    sensitivity: float  # % change in CPI per % change in param
    direction: str  # 'positive' or 'negative'


def load_model(model_path: Path, repo_root: Path) -> Tuple[Any, Optional[str]]:
    """Load a processor model dynamically"""
    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for name in dir(module):
            if name.endswith('Model') and name != 'BaseProcessorModel':
                obj = getattr(module, name)
                if isinstance(obj, type):
                    return obj(), None
        
        return None, "No Model class found"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def get_model_cpi(model: Any, workload: str = 'typical') -> Optional[float]:
    """Get CPI from model analysis"""
    try:
        result = model.analyze(workload)
        if result and hasattr(result, 'cpi'):
            return result.cpi
    except:
        pass
    return None


def analyze_sensitivity(model: Any, expected_cpi: float) -> List[SensitivityResult]:
    """Analyze parameter sensitivity for a model"""
    results = []
    
    if not hasattr(model, 'instruction_categories'):
        return results
    
    base_cpi = get_model_cpi(model)
    if not base_cpi:
        return results
    
    # Test each instruction category's base_cycles
    for cat_name, cat in model.instruction_categories.items():
        original = cat.base_cycles
        if original <= 0:
            continue
        
        # Increase by 10%
        cat.base_cycles = original * 1.1
        new_cpi = get_model_cpi(model)
        cat.base_cycles = original  # Restore
        
        if new_cpi:
            param_change = 0.1  # 10%
            cpi_change = (new_cpi - base_cpi) / base_cpi
            sensitivity = cpi_change / param_change if param_change != 0 else 0
            
            results.append(SensitivityResult(
                parameter=f"{cat_name}.base_cycles",
                category=cat_name,
                base_value=original,
                sensitivity=abs(sensitivity),
                direction='positive' if sensitivity > 0 else 'negative'
            ))
    
    # Test memory_cycles too
    for cat_name, cat in model.instruction_categories.items():
        if not hasattr(cat, 'memory_cycles') or cat.memory_cycles <= 0:
            continue
        
        original = cat.memory_cycles
        cat.memory_cycles = original * 1.1
        new_cpi = get_model_cpi(model)
        cat.memory_cycles = original
        
        if new_cpi:
            param_change = 0.1
            cpi_change = (new_cpi - base_cpi) / base_cpi
            sensitivity = cpi_change / param_change if param_change != 0 else 0
            
            results.append(SensitivityResult(
                parameter=f"{cat_name}.memory_cycles",
                category=cat_name,
                base_value=original,
                sensitivity=abs(sensitivity),
                direction='positive' if sensitivity > 0 else 'negative'
            ))
    
    # Sort by sensitivity (highest first)
    results.sort(key=lambda x: x.sensitivity, reverse=True)
    
    return results


def calibrate_model(
    model: Any,
    expected_cpi: float,
    max_iterations: int = 50,
    tolerance: float = 0.05,  # 5% error tolerance
    verbose: bool = False
) -> CalibrationResult:
    """
    Calibrate model parameters to match expected CPI.
    
    Uses a simple iterative scaling approach:
    1. Find most sensitive parameters
    2. Scale them to reduce error
    3. Repeat until error < tolerance or max iterations reached
    """
    processor_name = getattr(model, 'name', 'Unknown')
    original_cpi = get_model_cpi(model)
    
    if not original_cpi:
        return CalibrationResult(
            processor=processor_name,
            original_cpi=0, calibrated_cpi=0, expected_cpi=expected_cpi,
            original_error=100, calibrated_error=100,
            parameters_changed={}, success=False,
            notes="Could not get initial CPI"
        )
    
    original_error = abs(original_cpi - expected_cpi) / expected_cpi * 100
    
    if original_error <= tolerance * 100:
        return CalibrationResult(
            processor=processor_name,
            original_cpi=original_cpi, calibrated_cpi=original_cpi,
            expected_cpi=expected_cpi,
            original_error=original_error, calibrated_error=original_error,
            parameters_changed={}, success=True,
            notes="Already within tolerance"
        )
    
    # Store original values
    original_values = {}
    for cat_name, cat in model.instruction_categories.items():
        original_values[f"{cat_name}.base_cycles"] = cat.base_cycles
        if hasattr(cat, 'memory_cycles'):
            original_values[f"{cat_name}.memory_cycles"] = cat.memory_cycles
    
    # Determine if we need to increase or decrease CPI
    current_cpi = original_cpi
    need_increase = current_cpi < expected_cpi
    
    # Simple scaling approach
    scale_factor = expected_cpi / current_cpi
    
    # Apply uniform scaling to base_cycles (bounded)
    scale_factor = max(0.3, min(3.0, scale_factor))  # Limit to 0.3x - 3x
    
    parameters_changed = {}
    
    for cat_name, cat in model.instruction_categories.items():
        old_val = cat.base_cycles
        new_val = old_val * scale_factor
        
        # Keep reasonable bounds
        new_val = max(1.0, min(100.0, new_val))
        cat.base_cycles = new_val
        
        if abs(new_val - old_val) > 0.01:
            parameters_changed[f"{cat_name}.base_cycles"] = (old_val, new_val)
    
    # Check result
    calibrated_cpi = get_model_cpi(model)
    if not calibrated_cpi:
        # Restore and fail
        for cat_name, cat in model.instruction_categories.items():
            cat.base_cycles = original_values[f"{cat_name}.base_cycles"]
        
        return CalibrationResult(
            processor=processor_name,
            original_cpi=original_cpi, calibrated_cpi=original_cpi,
            expected_cpi=expected_cpi,
            original_error=original_error, calibrated_error=original_error,
            parameters_changed={}, success=False,
            notes="Calibration failed to produce valid CPI"
        )
    
    calibrated_error = abs(calibrated_cpi - expected_cpi) / expected_cpi * 100
    success = calibrated_error <= tolerance * 100
    
    # If still not good enough, try fine-tuning
    if not success and calibrated_error < original_error:
        # Second pass with smaller adjustment
        remaining_factor = expected_cpi / calibrated_cpi
        remaining_factor = max(0.7, min(1.4, remaining_factor))
        
        for cat_name, cat in model.instruction_categories.items():
            old_val = cat.base_cycles
            new_val = old_val * remaining_factor
            new_val = max(1.0, min(100.0, new_val))
            cat.base_cycles = new_val
            
            # Update the change record
            orig_val = original_values[f"{cat_name}.base_cycles"]
            if abs(new_val - orig_val) > 0.01:
                parameters_changed[f"{cat_name}.base_cycles"] = (orig_val, new_val)
        
        calibrated_cpi = get_model_cpi(model) or calibrated_cpi
        calibrated_error = abs(calibrated_cpi - expected_cpi) / expected_cpi * 100
        success = calibrated_error <= tolerance * 100
    
    return CalibrationResult(
        processor=processor_name,
        original_cpi=original_cpi,
        calibrated_cpi=calibrated_cpi,
        expected_cpi=expected_cpi,
        original_error=original_error,
        calibrated_error=calibrated_error,
        parameters_changed=parameters_changed,
        success=success,
        notes=f"Scale factor: {scale_factor:.2f}"
    )


def generate_calibrated_model(
    model_path: Path,
    calibration: CalibrationResult,
    output_path: Path = None,
    dry_run: bool = False
) -> Optional[str]:
    """
    Generate a calibrated version of the model file.
    
    Returns the path to the new file or None on failure.
    """
    if not calibration.parameters_changed:
        return None
    
    try:
        with open(model_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return None
    
    # Apply changes to the file content
    for param, (old_val, new_val) in calibration.parameters_changed.items():
        cat_name = param.split('.')[0]
        
        # Pattern to find InstructionCategory definition
        # e.g., InstructionCategory('register_ops', 2, 0, "Register operations")
        pattern = rf"(InstructionCategory\s*\(\s*['\"]?{cat_name}['\"]?\s*,\s*){old_val:.1f}(\s*,)"
        
        # Try integer pattern too
        if not re.search(pattern, content):
            pattern = rf"(InstructionCategory\s*\(\s*['\"]?{cat_name}['\"]?\s*,\s*){int(old_val)}(\s*,)"
        
        replacement = rf"\g<1>{new_val:.1f}\2"
        content = re.sub(pattern, replacement, content)
    
    # Add calibration comment
    calibration_note = f'''
# =============================================================================
# CALIBRATION APPLIED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Original CPI: {calibration.original_cpi:.2f}
# Calibrated CPI: {calibration.calibrated_cpi:.2f}
# Expected CPI: {calibration.expected_cpi:.2f}
# Error reduced: {calibration.original_error:.1f}% -> {calibration.calibrated_error:.1f}%
# =============================================================================
'''
    
    # Insert after docstring
    docstring_end = content.find('"""', content.find('"""') + 3)
    if docstring_end > 0:
        content = content[:docstring_end+3] + calibration_note + content[docstring_end+3:]
    
    if output_path is None:
        output_path = model_path.parent / f"{model_path.stem}_calibrated.py"
    
    if not dry_run:
        with open(output_path, 'w') as f:
            f.write(content)
    
    return str(output_path)


def print_sensitivity_report(results: List[SensitivityResult], processor: str):
    """Print sensitivity analysis report"""
    print()
    print("=" * 70)
    print(f"SENSITIVITY ANALYSIS: {processor}")
    print("=" * 70)
    print()
    print(f"{'Parameter':<35} {'Base Value':>10} {'Sensitivity':>12} {'Direction':>10}")
    print("-" * 70)
    
    for r in results[:10]:  # Top 10 most sensitive
        print(f"{r.parameter:<35} {r.base_value:>10.2f} {r.sensitivity:>11.2f}x {r.direction:>10}")
    
    print()
    print("Sensitivity = % change in CPI per % change in parameter")
    print("Higher values = more impact on model output")


def print_calibration_report(result: CalibrationResult):
    """Print calibration report"""
    print()
    print("=" * 70)
    print(f"CALIBRATION REPORT: {result.processor}")
    print("=" * 70)
    print()
    print(f"Expected CPI:    {result.expected_cpi:.2f}")
    print(f"Original CPI:    {result.original_cpi:.2f} ({result.original_error:.1f}% error)")
    print(f"Calibrated CPI:  {result.calibrated_cpi:.2f} ({result.calibrated_error:.1f}% error)")
    print()
    
    if result.success:
        print("✅ CALIBRATION SUCCESSFUL")
    else:
        improvement = result.original_error - result.calibrated_error
        if improvement > 0:
            print(f"🟡 PARTIAL SUCCESS (improved by {improvement:.1f}%)")
        else:
            print("❌ CALIBRATION FAILED")
    
    if result.parameters_changed:
        print()
        print("Parameters changed:")
        print("-" * 50)
        for param, (old, new) in result.parameters_changed.items():
            change = (new - old) / old * 100 if old != 0 else 0
            print(f"  {param}: {old:.2f} -> {new:.2f} ({change:+.1f}%)")
    
    if result.notes:
        print()
        print(f"Notes: {result.notes}")


def main():
    parser = argparse.ArgumentParser(
        description='Calibrate processor models to match expected CPI'
    )
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--processor', '-p', help='Specific processor to calibrate')
    parser.add_argument('--analyze', '-a', action='store_true', help='Run sensitivity analysis only')
    parser.add_argument('--calibrate', '-c', action='store_true', help='Run calibration')
    parser.add_argument('--calibrate-all', action='store_true', help='Calibrate all processors')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    parser.add_argument('--generate', '-g', action='store_true', help='Generate calibrated model files')
    parser.add_argument('--tolerance', type=float, default=0.05, help='Error tolerance (default 0.05 = 5%%)')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 70)
    print("MODEL CALIBRATOR")
    print("=" * 70)
    print(f"Repository: {repo_path}")
    print()
    
    if args.processor:
        # Single processor mode
        expected_cpi = EXPECTED_CPI.get(args.processor)
        if not expected_cpi:
            print(f"No expected CPI for processor: {args.processor}")
            return
        
        # Find model
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            model_path = repo_path / family / args.processor / 'current' / f'{args.processor}_validated.py'
            if model_path.exists():
                break
        else:
            print(f"Model not found for: {args.processor}")
            return
        
        model, error = load_model(model_path, repo_path)
        if not model:
            print(f"Failed to load model: {error}")
            return
        
        print(f"Processor: {args.processor}")
        print(f"Expected CPI: {expected_cpi}")
        print(f"Model path: {model_path}")
        
        if args.analyze:
            results = analyze_sensitivity(model, expected_cpi)
            print_sensitivity_report(results, args.processor)
        
        if args.calibrate:
            result = calibrate_model(model, expected_cpi, tolerance=args.tolerance)
            print_calibration_report(result)
            
            if args.generate and result.success:
                output = generate_calibrated_model(model_path, result, dry_run=args.dry_run)
                if output:
                    print(f"\n{'Would generate' if args.dry_run else 'Generated'}: {output}")
    
    elif args.calibrate_all:
        # Calibrate all processors
        print("Calibrating all processors...")
        print("-" * 50)
        
        successes = 0
        improvements = 0
        failures = 0
        
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            family_path = repo_path / family
            if not family_path.exists():
                continue
            
            for proc_dir in sorted(family_path.iterdir()):
                if not proc_dir.is_dir():
                    continue
                
                proc_name = proc_dir.name
                expected_cpi = EXPECTED_CPI.get(proc_name)
                if not expected_cpi:
                    continue
                
                model_path = proc_dir / 'current' / f'{proc_name}_validated.py'
                if not model_path.exists():
                    continue
                
                model, error = load_model(model_path, repo_path)
                if not model:
                    continue
                
                result = calibrate_model(model, expected_cpi, tolerance=args.tolerance)
                
                if result.success:
                    status = "✅"
                    successes += 1
                elif result.calibrated_error < result.original_error:
                    status = "🟡"
                    improvements += 1
                else:
                    status = "❌"
                    failures += 1
                
                print(f"{status} {family}/{proc_name}: {result.original_error:.1f}% -> {result.calibrated_error:.1f}%")
                
                if args.generate and (result.success or result.calibrated_error < result.original_error):
                    generate_calibrated_model(model_path, result, dry_run=args.dry_run)
        
        print()
        print("=" * 50)
        print(f"Calibrated successfully: {successes}")
        print(f"Improved (not fully): {improvements}")
        print(f"Failed: {failures}")
    
    else:
        print("Specify --analyze, --calibrate, --calibrate-all, or --processor")
        print()
        print("Examples:")
        print("  python model_calibrator.py . --processor i8086 --analyze")
        print("  python model_calibrator.py . --processor i8086 --calibrate")
        print("  python model_calibrator.py . --calibrate-all")


if __name__ == '__main__':
    main()
