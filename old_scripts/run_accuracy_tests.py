#!/usr/bin/env python3
"""
Run Accuracy Tests for Modeling_2026
=====================================

Runs processor models and compares predicted CPI/IPC to expected values
from datasheets. Updates validation JSON files with accuracy results.

Usage:
    python run_accuracy_tests.py [repo_path] [--dry-run]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import argparse
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


# Expected CPI values - updated 2026-01-29 with cross-validated targets
# Many values revised based on detailed research and cross-validation
EXPECTED_CPI = {
    # Intel 4-bit
    'i4004': 10.8,
    'i4040': 10.5,
    # Intel 8-bit
    'i8008': 11.0,
    'i8080': 9.2,
    'i8085': 5.5,
    # Intel 16-bit
    'i8086': 4.5,
    'i8088': 5.2,
    'i80186': 4.0,
    'i80188': 4.2,
    'i80286': 4.0,
    # Intel 32-bit
    'i80386': 4.5,
    'i80486': 2.0,
    'pentium': 1.0,
    'i860': 1.2,
    # MOS/WDC - cross-validated
    'mos6502': 3.0,     # Cross-validated (was 3.5)
    'mos6510': 3.0,     # Cross-validated (was 3.5)
    'wdc65c02': 2.85,   # Cross-validated (was 3.2)
    'wdc65816': 3.8,
    # Motorola 8-bit
    'm6800': 4.0,
    'm6801': 3.8,
    'm6802': 4.0,       # Same as 6800
    'm6805': 5.0,       # Microcontroller
    'm6809': 3.5,
    'm68hc11': 4.5,     # Microcontroller
    # Motorola 68k
    'm68000': 6.5,
    'm68008': 7.0,
    'm68010': 6.0,
    'm68020': 3.5,
    'm68030': 3.0,
    'm68040': 2.0,
    'm68060': 1.5,      # Superscalar
    'm68881': 10.0,     # FPU coprocessor
    'm68882': 10.0,     # FPU coprocessor
    # Zilog
    'z8': 10.0,         # 8-bit MCU
    'z80': 5.5,
    'z80a': 5.5,
    'z80b': 5.5,
    'z180': 4.5,
    'z8000': 4.5,
    'z80000': 6.0,      # 32-bit Z8000 extension
    # ARM - cross-validated
    'arm1': 1.8,
    'arm2': 1.43,       # Cross-validated (was 1.5)
    'arm3': 1.33,       # Cross-validated (was 1.4) - first with cache
    # RISC - cross-validated
    'sparc': 1.3,       # Cross-validated (was 1.5)
    'sun_spark': 1.5,
    'r2000': 2.0,       # Cross-validated (was 1.5) - MIPS R2000
    'alpha21064': 0.77, # Cross-validated (was 1.0) - IPC 1.3
    'hp_pa_risc': 0.91, # Cross-validated (was 1.2) - IPC 1.1
    't414': 2.0,
    # Intel FPU coprocessors
    'i80287': 100.0,    # FPU coprocessor
    'i80387': 50.0,     # FPU coprocessor (faster than 287)
    # Intel MCUs
    'i8048': 1.5,       # 8-bit MCU
    'i8051': 12.0,      # 8-bit MCU
    'i8748': 1.5,       # EPROM version of 8048
    'i8751': 12.0,      # EPROM version of 8051
    'iapx432': 50.0,    # Complex capability-based architecture
    # Other - cross-validated
    'am2901': 1.0,
    'am2903': 1.0,      # Bit-slice
    'am29000': 1.5,     # RISC
    'amd_29000': 1.33,  # AMD 29000 RISC
    'aim__ppc_601': 0.67,  # PowerPC 601 (IPC ~1.5)
    'arm6': 1.43,       # ARM6
    'berkeley_risc1': 1.3, # Original RISC
    'f8': 7.0,          # Cross-validated (was 5.0)
    'intersil6100': 10.5,  # PDP-8 on a chip
    'nc4016': 1.2,      # Novix Forth
    'nec_v20': 3.4,     # 8088 compatible
    'ns32016': 12.0,    # Cross-validated (was 4.0) - CISC slower
    'ns32032': 10.0,    # National Semi 32-bit
    'pic1650': 1.15,    # Microchip PIC
    'rca1802': 12.0,    # Cross-validated (was 8.0) - 2-phase slow
    'rca1805': 10.0,    # Enhanced 1802
    'rtx2000': 1.1,     # Forth stack processor
    'scmp': 10.0,       # Cross-validated (was 6.0)
    'signetics2650': 3.0,  # Cross-validated (was 5.5) - actually faster
    'tms1000': 6.0,     # 4-bit MCU
    'tms9900': 20.0,    # Cross-validated (was 4.5) - memory-to-memory very slow
    'tms9995': 12.0,    # Enhanced TMS9900
    'tms320c10': 1.5,   # DSP
    'we32000': 8.0,     # AT&T WE32000
}


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


def run_model_analysis(model: Any) -> Dict[str, Any]:
    """Run model analysis and extract metrics"""
    results = {
        'success': False,
        'cpi': None,
        'ipc': None,
        'workloads': {}
    }
    
    workloads = ['typical', 'compute', 'memory', 'control', 'mixed']
    
    for workload in workloads:
        try:
            if hasattr(model, 'analyze'):
                result = model.analyze(workload)
                if result:
                    cpi = getattr(result, 'cpi', None)
                    ipc = getattr(result, 'ipc', None)
                    
                    if cpi and cpi > 0:
                        results['workloads'][workload] = {
                            'cpi': round(cpi, 4),
                            'ipc': round(1.0/cpi, 4) if cpi > 0 else None
                        }
                        
                        # Use 'typical' as primary if available
                        if workload == 'typical':
                            results['cpi'] = cpi
                            results['ipc'] = 1.0/cpi if cpi > 0 else None
                            results['success'] = True
        except Exception as e:
            results['workloads'][workload] = {'error': str(e)}
    
    # Fallback to first successful workload
    if not results['success'] and results['workloads']:
        for wl, data in results['workloads'].items():
            if 'cpi' in data and data['cpi']:
                results['cpi'] = data['cpi']
                results['ipc'] = data.get('ipc')
                results['success'] = True
                break
    
    return results


def calculate_accuracy(predicted_cpi: float, expected_cpi: float) -> Dict[str, float]:
    """Calculate accuracy metrics"""
    if not predicted_cpi or not expected_cpi:
        return {'error_percent': None, 'passed': False}
    
    error = abs(predicted_cpi - expected_cpi) / expected_cpi * 100
    
    return {
        'predicted_cpi': round(predicted_cpi, 4),
        'expected_cpi': expected_cpi,
        'error_percent': round(error, 2),
        'passed': error < 10.0,  # Pass if within 10%
        'fully_validated': error < 5.0  # Fully validated if within 5%
    }


def update_validation_json(
    json_path: Path,
    accuracy_data: Dict[str, Any],
    dry_run: bool = False
) -> Tuple[bool, str]:
    """Update validation JSON with accuracy results"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Error reading JSON: {e}"
    
    # Update accuracy section
    if 'accuracy' not in data:
        data['accuracy'] = {}
    
    data['accuracy']['predicted_cpi'] = accuracy_data.get('predicted_cpi')
    data['accuracy']['expected_cpi'] = accuracy_data.get('expected_cpi')
    data['accuracy']['cpi_error_percent'] = accuracy_data.get('error_percent')
    data['accuracy']['ipc_error_percent'] = accuracy_data.get('error_percent')
    data['accuracy']['validation_passed'] = accuracy_data.get('passed', False)
    data['accuracy']['fully_validated'] = accuracy_data.get('fully_validated', False)
    data['accuracy']['validated_workloads'] = list(accuracy_data.get('workloads', {}).keys())
    data['accuracy']['validation_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Update validation_date at top level too
    data['validation_date'] = datetime.now().strftime('%Y-%m-%d')
    
    if not dry_run:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            return False, f"Error writing JSON: {e}"
    
    error = accuracy_data.get('error_percent')
    if error is not None:
        status = "✅ VALIDATED" if accuracy_data.get('fully_validated') else (
            "🟡 PASSED" if accuracy_data.get('passed') else "❌ FAILED"
        )
        return True, f"{status} ({error:.1f}% error)"
    else:
        return False, "Could not calculate accuracy"


def run_accuracy_tests(repo_path: Path, dry_run: bool = False, verbose: bool = False) -> Dict:
    """Run accuracy tests for all processors"""
    results = {
        'total': 0,
        'tested': 0,
        'passed': 0,
        'fully_validated': 0,
        'failed': 0,
        'errors': 0,
        'details': []
    }
    
    families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
    
    for family in families:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for proc_dir in sorted(family_path.iterdir()):
            if not proc_dir.is_dir() or proc_dir.name.startswith('.'):
                continue
            
            proc_name = proc_dir.name
            results['total'] += 1
            
            # Find model file
            model_dir = proc_dir / 'current'
            model_files = list(model_dir.glob('*_validated.py')) if model_dir.exists() else []
            
            if not model_files:
                results['details'].append({
                    'processor': f"{family}/{proc_name}",
                    'status': 'NO_MODEL',
                    'message': 'No validated model file'
                })
                continue
            
            # Find validation JSON
            validation_dir = proc_dir / 'validation'
            json_files = list(validation_dir.glob('*_validation.json')) if validation_dir.exists() else []
            
            if not json_files:
                results['details'].append({
                    'processor': f"{family}/{proc_name}",
                    'status': 'NO_JSON',
                    'message': 'No validation JSON'
                })
                continue
            
            # Get expected CPI
            expected_cpi = EXPECTED_CPI.get(proc_name)
            if not expected_cpi:
                results['details'].append({
                    'processor': f"{family}/{proc_name}",
                    'status': 'NO_EXPECTED',
                    'message': 'No expected CPI in database'
                })
                continue
            
            # Load and run model
            model, load_error = load_model(model_files[0], repo_path)
            
            if model is None:
                results['errors'] += 1
                results['details'].append({
                    'processor': f"{family}/{proc_name}",
                    'status': 'LOAD_ERROR',
                    'message': load_error
                })
                continue
            
            # Run analysis
            analysis = run_model_analysis(model)
            
            if not analysis['success']:
                results['errors'] += 1
                results['details'].append({
                    'processor': f"{family}/{proc_name}",
                    'status': 'RUN_ERROR',
                    'message': 'Model analysis failed'
                })
                continue
            
            # Calculate accuracy
            accuracy = calculate_accuracy(analysis['cpi'], expected_cpi)
            accuracy['workloads'] = analysis['workloads']
            
            # Update validation JSON
            updated, message = update_validation_json(json_files[0], accuracy, dry_run)
            
            results['tested'] += 1
            
            if accuracy.get('fully_validated'):
                results['fully_validated'] += 1
                status = 'FULLY_VALIDATED'
            elif accuracy.get('passed'):
                results['passed'] += 1
                status = 'PASSED'
            else:
                results['failed'] += 1
                status = 'FAILED'
            
            results['details'].append({
                'processor': f"{family}/{proc_name}",
                'status': status,
                'predicted_cpi': accuracy.get('predicted_cpi'),
                'expected_cpi': expected_cpi,
                'error_percent': accuracy.get('error_percent'),
                'message': message
            })
    
    return results


def print_results(results: Dict, verbose: bool = False):
    """Print formatted results"""
    print()
    print("=" * 70)
    print("ACCURACY TEST RESULTS")
    print("=" * 70)
    print()
    print(f"Total processors:     {results['total']}")
    print(f"Models tested:        {results['tested']}")
    print(f"Fully validated (<5%): {results['fully_validated']}")
    print(f"Passed (<10%):        {results['passed']}")
    print(f"Failed (>10%):        {results['failed']}")
    print(f"Errors:               {results['errors']}")
    print()
    
    # Group by status
    validated = [d for d in results['details'] if d['status'] == 'FULLY_VALIDATED']
    passed = [d for d in results['details'] if d['status'] == 'PASSED']
    failed = [d for d in results['details'] if d['status'] == 'FAILED']
    errors = [d for d in results['details'] if d['status'] in ('LOAD_ERROR', 'RUN_ERROR', 'NO_EXPECTED')]
    
    if validated:
        print("✅ FULLY VALIDATED (<5% error):")
        print("-" * 50)
        for d in validated:
            print(f"  {d['processor']:25} {d['error_percent']:5.1f}% error (predicted {d['predicted_cpi']:.2f}, expected {d['expected_cpi']:.2f})")
        print()
    
    if passed:
        print("🟡 PASSED (<10% error):")
        print("-" * 50)
        for d in passed:
            print(f"  {d['processor']:25} {d['error_percent']:5.1f}% error (predicted {d['predicted_cpi']:.2f}, expected {d['expected_cpi']:.2f})")
        print()
    
    if failed and verbose:
        print("❌ FAILED (>10% error):")
        print("-" * 50)
        for d in failed:
            print(f"  {d['processor']:25} {d['error_percent']:5.1f}% error (predicted {d['predicted_cpi']:.2f}, expected {d['expected_cpi']:.2f})")
        print()
    
    if errors and verbose:
        print("⚠️  ERRORS:")
        print("-" * 50)
        for d in errors:
            print(f"  {d['processor']:25} {d['status']}: {d.get('message', 'Unknown')}")
        print()
    
    # Summary
    if results['tested'] > 0:
        pass_rate = (results['fully_validated'] + results['passed']) / results['tested'] * 100
        print(f"Pass rate: {pass_rate:.1f}% ({results['fully_validated'] + results['passed']}/{results['tested']})")


def main():
    parser = argparse.ArgumentParser(
        description='Run accuracy tests for processor models'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Repository path'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview only, do not update JSON files'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output including failures'
    )
    parser.add_argument(
        '--processor', '-p',
        help='Test specific processor only'
    )
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 70)
    print("PROCESSOR MODEL ACCURACY TESTING")
    print("=" * 70)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'UPDATE JSON FILES'}")
    print()
    
    if args.processor:
        # Test single processor
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            proc_path = repo_path / family / args.processor
            if proc_path.exists():
                print(f"Testing: {family}/{args.processor}")
                
                model_files = list((proc_path / 'current').glob('*_validated.py'))
                if not model_files:
                    print("  ❌ No model file found")
                    return
                
                model, error = load_model(model_files[0], repo_path)
                if not model:
                    print(f"  ❌ Load error: {error}")
                    return
                
                print("  ✅ Model loaded")
                
                analysis = run_model_analysis(model)
                if analysis['success']:
                    print(f"  📊 Predicted CPI: {analysis['cpi']:.4f}")
                    
                    expected = EXPECTED_CPI.get(args.processor)
                    if expected:
                        accuracy = calculate_accuracy(analysis['cpi'], expected)
                        print(f"  📊 Expected CPI: {expected}")
                        print(f"  📊 Error: {accuracy['error_percent']:.2f}%")
                        print(f"  {'✅ PASSED' if accuracy['passed'] else '❌ FAILED'}")
                    else:
                        print(f"  ⚠️  No expected CPI in database")
                else:
                    print(f"  ❌ Analysis failed")
                return
        
        print(f"Processor not found: {args.processor}")
        return
    
    # Run all tests
    results = run_accuracy_tests(repo_path, args.dry_run, args.verbose)
    print_results(results, args.verbose)
    
    print()
    print("=" * 70)
    if args.dry_run:
        print("DRY RUN - No JSON files were modified")
        print("Run without --dry-run to update validation files")
    else:
        print("Validation JSON files have been updated with accuracy results")
    print("=" * 70)


if __name__ == '__main__':
    main()
