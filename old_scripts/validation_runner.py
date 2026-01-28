#!/usr/bin/env python3
"""
Validation Test Runner for Modeling_2026
==========================================

This script runs validation tests for processor models:

1. Loads model and validation JSON
2. Executes timing tests
3. Compares predicted vs expected values
4. Calculates accuracy metrics
5. Updates validation JSON with results

Usage:
    python validation_runner.py [repo_path] [options]

Options:
    --processor NAME    Run validation for specific processor
    --family NAME       Run validation for specific family
    --run-all           Run validation for all processors
    --update-json       Update validation JSON with results
    --verbose           Show detailed test output

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import importlib.util
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Tuple
from dataclasses import dataclass, field


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TestResult:
    """Result of a single validation test"""
    name: str
    category: str
    expected: Optional[float]
    predicted: Optional[float]
    error_percent: Optional[float] = None
    passed: bool = False
    notes: str = ""
    
    def compute_error(self):
        if self.expected and self.predicted and self.expected > 0:
            self.error_percent = abs(self.predicted - self.expected) / self.expected * 100
            self.passed = self.error_percent < 10.0  # 10% threshold


@dataclass
class WorkloadResult:
    """Result of a workload validation"""
    name: str
    expected_cpi: Optional[float]
    predicted_cpi: Optional[float]
    expected_ipc: Optional[float]
    predicted_ipc: Optional[float]
    error_percent: Optional[float] = None
    passed: bool = False


@dataclass
class ValidationResult:
    """Complete validation result for a processor"""
    processor: str
    family: str
    timestamp: str
    
    # Test results
    timing_tests: List[TestResult] = field(default_factory=list)
    workload_results: List[WorkloadResult] = field(default_factory=list)
    
    # Aggregate metrics
    tests_run: int = 0
    tests_passed: int = 0
    ipc_error_percent: Optional[float] = None
    cpi_error_percent: Optional[float] = None
    overall_pass: bool = False
    
    # Issues
    issues: List[str] = field(default_factory=list)
    
    def compute_summary(self):
        """Compute summary statistics"""
        self.tests_run = len(self.timing_tests)
        self.tests_passed = sum(1 for t in self.timing_tests if t.passed)
        
        # Calculate average IPC error from workload results
        ipc_errors = [w.error_percent for w in self.workload_results if w.error_percent is not None]
        if ipc_errors:
            self.ipc_error_percent = sum(ipc_errors) / len(ipc_errors)
        
        # Overall pass: >80% tests pass AND IPC error < 5%
        test_pass_rate = self.tests_passed / max(1, self.tests_run)
        self.overall_pass = (test_pass_rate >= 0.8 and 
                           (self.ipc_error_percent is None or self.ipc_error_percent < 5.0))


# =============================================================================
# MODEL LOADER
# =============================================================================

def load_processor_model(model_path: Path, repo_root: Path = None) -> Tuple[Any, Optional[str]]:
    """Dynamically load a processor model from file
    
    Args:
        model_path: Path to the *_validated.py file
        repo_root: Repository root path (for imports from 'common')
    
    Returns:
        Tuple of (model_instance_or_module, error_message)
        If successful, error_message is None
        If failed, model is None and error_message describes the issue
    """
    try:
        # Set up sys.path for imports from 'common' module
        if repo_root is None:
            # Infer repo root: model_path is like repo/family/processor/current/file.py
            repo_root = model_path.parent.parent.parent.parent
        
        # Add repo root to path if not already there
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)
        
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the model class (look for class ending with 'Model' but not BaseProcessorModel)
        for name in dir(module):
            if name == 'BaseProcessorModel':
                continue  # Skip the base class
            obj = getattr(module, name)
            if isinstance(obj, type) and name.endswith('Model'):
                try:
                    return obj(), None
                except Exception as e:
                    return None, f"Failed to instantiate {name}: {e}"
        
        # Fallback: look for analyze function
        if hasattr(module, 'analyze'):
            return module, None
        
        # Fallback: return the module itself (might have other usable attributes)
        return module, None
        
    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    except ImportError as e:
        return None, f"Import error: {e}"
    except Exception as e:
        return None, f"Load error: {type(e).__name__}: {e}"


def load_validation_json(json_path: Path) -> Optional[Dict[str, Any]]:
    """Load validation JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


# =============================================================================
# VALIDATION RUNNER
# =============================================================================

class ValidationRunner:
    """Runs validation tests for processor models"""
    
    def __init__(self, repo_path: Path, verbose: bool = False):
        self.repo_path = repo_path
        self.verbose = verbose
        self.results: List[ValidationResult] = []
    
    def log(self, message: str):
        if self.verbose:
            print(f"  {message}")
    
    def run_timing_tests(self, model: Any, validation_data: Dict[str, Any]) -> List[TestResult]:
        """Run timing tests from validation JSON against model"""
        results = []
        
        timing_tests = validation_data.get('timing_tests', [])
        
        for test in timing_tests:
            test_name = test.get('name', 'unknown')
            expected = test.get('expected_cycles')
            
            # Try to get predicted value from model
            predicted = None
            
            # Method 1: Try get_instruction_timing method
            if hasattr(model, 'get_instruction_timing'):
                try:
                    timing = model.get_instruction_timing(test.get('category', 'general'))
                    if isinstance(timing, dict):
                        predicted = timing.get('cycles') or timing.get('base_cycles')
                    elif isinstance(timing, (int, float)):
                        predicted = timing
                except Exception:
                    pass
            
            # Method 2: Try instruction_categories attribute
            if predicted is None and hasattr(model, 'instruction_categories'):
                try:
                    cats = model.instruction_categories
                    if isinstance(cats, dict):
                        cat_name = test.get('category', test_name)
                        if cat_name in cats:
                            cat = cats[cat_name]
                            if hasattr(cat, 'base_cycles'):
                                predicted = cat.base_cycles
                            elif isinstance(cat, dict):
                                predicted = cat.get('base_cycles') or cat.get('cycles')
                except Exception:
                    pass
            
            result = TestResult(
                name=test_name,
                category=test.get('category', 'general'),
                expected=expected,
                predicted=predicted,
            )
            
            if expected and predicted:
                result.compute_error()
                self.log(f"Test {test_name}: expected={expected}, predicted={predicted}, error={result.error_percent:.1f}%")
            else:
                self.log(f"Test {test_name}: skipped (expected={expected}, predicted={predicted})")
            
            results.append(result)
        
        return results
    
    def run_workload_tests(self, model: Any, validation_data: Dict[str, Any]) -> List[WorkloadResult]:
        """Run workload validation tests"""
        results = []
        
        workload_profiles = validation_data.get('workload_profiles', {})
        validated_workloads = workload_profiles.get('validated', [])
        available_workloads = workload_profiles.get('available', ['typical'])
        
        # Get expected values from validation data or specs
        specs = validation_data.get('specifications', {})
        accuracy_data = validation_data.get('accuracy', {})
        
        for workload_name in available_workloads:
            # Try to run model analysis
            predicted_cpi = None
            predicted_ipc = None
            
            if hasattr(model, 'analyze'):
                try:
                    result = model.analyze(workload_name)
                    if hasattr(result, 'cpi'):
                        predicted_cpi = result.cpi
                    if hasattr(result, 'ipc'):
                        predicted_ipc = result.ipc
                except Exception:
                    pass
            
            # Get expected values (would need to be in validation JSON)
            expected_cpi = None
            expected_ipc = None
            
            # Calculate error if we have both
            error_percent = None
            passed = False
            
            if predicted_ipc and expected_ipc:
                error_percent = abs(predicted_ipc - expected_ipc) / expected_ipc * 100
                passed = error_percent < 5.0
            
            result = WorkloadResult(
                name=workload_name,
                expected_cpi=expected_cpi,
                predicted_cpi=predicted_cpi,
                expected_ipc=expected_ipc,
                predicted_ipc=predicted_ipc,
                error_percent=error_percent,
                passed=passed,
            )
            
            self.log(f"Workload {workload_name}: CPI={predicted_cpi}, IPC={predicted_ipc}")
            results.append(result)
        
        return results
    
    def validate_processor(self, processor_path: Path, processor_name: str, family: str) -> ValidationResult:
        """Run complete validation for a processor"""
        result = ValidationResult(
            processor=processor_name,
            family=family,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Find model file
        current_dir = processor_path / 'current'
        model_files = list(current_dir.glob('*_validated.py')) if current_dir.exists() else []
        
        if not model_files:
            result.issues.append("No validated model file found")
            return result
        
        model_path = model_files[0]
        
        # Find validation JSON
        validation_dir = processor_path / 'validation'
        json_files = list(validation_dir.glob('*_validation.json')) if validation_dir.exists() else []
        
        if not json_files:
            result.issues.append("No validation JSON found")
            return result
        
        json_path = json_files[0]
        
        # Load model (now returns tuple with error message)
        model, error = load_processor_model(model_path, self.repo_path)
        if model is None:
            result.issues.append(f"Failed to load model: {error}")
            return result
        
        # Load validation data
        validation_data = load_validation_json(json_path)
        if validation_data is None:
            result.issues.append(f"Failed to load validation JSON from {json_path}")
            return result
        
        self.log(f"Loaded model: {model_path.name}")
        self.log(f"Loaded validation: {json_path.name}")
        
        # Run timing tests
        result.timing_tests = self.run_timing_tests(model, validation_data)
        
        # Run workload tests
        result.workload_results = self.run_workload_tests(model, validation_data)
        
        # Compute summary
        result.compute_summary()
        
        return result
    
    def validate_family(self, family: str) -> List[ValidationResult]:
        """Validate all processors in a family"""
        family_path = self.repo_path / family
        results = []
        
        if not family_path.exists():
            return results
        
        for item in sorted(family_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                print(f"Validating {family}/{item.name}...")
                result = self.validate_processor(item, item.name, family)
                results.append(result)
        
        return results
    
    def validate_all(self) -> List[ValidationResult]:
        """Validate all processors"""
        all_results = []
        families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
        
        for family in families:
            results = self.validate_family(family)
            all_results.extend(results)
        
        return all_results


def update_validation_json(json_path: Path, result: ValidationResult):
    """Update validation JSON with test results"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return False
    
    # Update timing tests with results
    for test_result in result.timing_tests:
        for test in data.get('timing_tests', []):
            if test.get('name') == test_result.name:
                test['measured_cycles'] = test_result.predicted
                test['error_percent'] = test_result.error_percent
                test['passed'] = test_result.passed
                break
    
    # Update accuracy
    data['accuracy'] = data.get('accuracy', {})
    data['accuracy']['ipc_error_percent'] = result.ipc_error_percent
    data['accuracy']['cpi_error_percent'] = result.cpi_error_percent
    data['accuracy']['validated_workloads'] = [w.name for w in result.workload_results if w.passed]
    data['accuracy']['notes'] = f"Validation run: {result.timestamp}"
    
    data['validation_date'] = result.timestamp.split()[0]
    
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def generate_report(results: List[ValidationResult]) -> str:
    """Generate validation results report"""
    lines = []
    
    lines.append("=" * 70)
    lines.append("VALIDATION TEST RESULTS")
    lines.append("=" * 70)
    lines.append("")
    
    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.overall_pass)
    
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total processors tested: {total}")
    lines.append(f"Passed validation: {passed} ({100*passed/max(1,total):.1f}%)")
    lines.append("")
    
    # By family
    families = {}
    for r in results:
        if r.family not in families:
            families[r.family] = []
        families[r.family].append(r)
    
    lines.append("BY FAMILY")
    lines.append("-" * 40)
    for family, family_results in sorted(families.items()):
        passed_count = sum(1 for r in family_results if r.overall_pass)
        total_count = len(family_results)
        lines.append(f"  {family:12} {passed_count:2}/{total_count:2} passed")
    lines.append("")
    
    # Detailed results
    lines.append("DETAILED RESULTS")
    lines.append("-" * 40)
    
    for family, family_results in sorted(families.items()):
        lines.append(f"\n{family.upper()}/")
        for r in sorted(family_results, key=lambda x: x.processor):
            status = "✅" if r.overall_pass else "❌"
            error_str = f"{r.ipc_error_percent:.1f}%" if r.ipc_error_percent else "N/A"
            lines.append(f"  {status} {r.processor:20} Tests: {r.tests_passed}/{r.tests_run}  Error: {error_str}")
            
            if r.issues:
                for issue in r.issues:
                    lines.append(f"      ⚠️  {issue}")
    
    lines.append("")
    lines.append("=" * 70)
    
    return '\n'.join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Validation Test Runner for Modeling_2026'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to Modeling_2026 repository'
    )
    parser.add_argument(
        '--processor',
        help='Run validation for specific processor'
    )
    parser.add_argument(
        '--family',
        help='Run validation for specific family'
    )
    parser.add_argument(
        '--run-all',
        action='store_true',
        help='Run validation for all processors'
    )
    parser.add_argument(
        '--update-json',
        action='store_true',
        help='Update validation JSON with results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed test output'
    )
    parser.add_argument(
        '--output', '-o',
        help='Write report to file'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    runner = ValidationRunner(repo_path, args.verbose)
    
    print("=" * 60)
    print("VALIDATION TEST RUNNER")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print("")
    
    results = []
    
    if args.run_all:
        results = runner.validate_all()
    elif args.family:
        results = runner.validate_family(args.family)
    elif args.processor:
        # Find processor
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            proc_path = repo_path / family / args.processor
            if proc_path.exists():
                result = runner.validate_processor(proc_path, args.processor, family)
                results.append(result)
                break
        else:
            print(f"Processor not found: {args.processor}")
            return
    else:
        print("No action specified. Use --run-all, --family, or --processor")
        return
    
    # Update JSON files if requested
    if args.update_json:
        print("\nUpdating validation JSON files...")
        for result in results:
            for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
                json_dir = repo_path / family / result.processor / 'validation'
                json_files = list(json_dir.glob('*_validation.json')) if json_dir.exists() else []
                if json_files:
                    if update_validation_json(json_files[0], result):
                        print(f"  Updated: {family}/{result.processor}")
                    break
    
    # Generate report
    report = generate_report(results)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport written to: {args.output}")
    else:
        print("")
        print(report)


if __name__ == '__main__':
    main()
