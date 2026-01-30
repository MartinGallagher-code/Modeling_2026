#!/usr/bin/env python3
"""
LMI Lambda Grey-Box Queueing Model
=====================================

Target CPI: 5.0
Architecture: 32-bit Tagged LISP Machine CPU (1984)

The LMI Lambda was a LISP machine CPU developed by LISP Machines
Inc. (LMI), a derivative of the MIT CADR architecture. It retained
the tagged architecture and hardware LISP support but with modest
improvements over the original CADR design.

Key characteristics:
- 32-bit tagged data width
- 4 MHz clock
- ~60,000 transistors
- CADR-derivative architecture
- Hardware type checking via tags
- Native LISP operations
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class InstructionCategory:
    name: str
    base_cycles: float
    memory_cycles: float = 0
    description: str = ""

    @property
    def total_cycles(self):
        return self.base_cycles + self.memory_cycles


@dataclass
class WorkloadProfile:
    name: str
    category_weights: Dict[str, float]
    description: str = ""


@dataclass
class AnalysisResult:
    processor: str
    workload: str
    ipc: float
    cpi: float
    ips: float
    bottleneck: str
    utilizations: Dict[str, float]
    base_cpi: float = 0.0
    correction_delta: float = 0.0

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations, base_cpi=None, correction_delta=0.0):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)


class BaseProcessorModel:
    pass


class LmiLambdaModel(BaseProcessorModel):
    """
    LMI Lambda Grey-Box Queueing Model

    Target CPI: 5.0
    Calibration: CADR-derivative LISP machine

    The LMI Lambda was a CADR derivative with modest improvements,
    retaining the microcoded tagged architecture while slightly
    improving some operations over the original CADR.
    """

    name = "LMI Lambda"
    manufacturer = "LISP Machines Inc."
    year = 1984
    clock_mhz = 4.0
    data_width = 32
    address_width = 24

    def __init__(self):
        # Typical: 0.15*2 + 0.15*4 + 0.20*7 + 0.10*11 + 0.20*5 + 0.20*3 = 5.00
        self.instruction_categories = {
            'car_cdr': InstructionCategory(
                'car_cdr', 2.0, 0,
                "CAR/CDR list operations (hardware-assisted)"
            ),
            'cons': InstructionCategory(
                'cons', 4.0, 0,
                "CONS cell allocation (slightly improved over CADR)"
            ),
            'eval': InstructionCategory(
                'eval', 7.0, 0,
                "Evaluation/function dispatch (microcoded)"
            ),
            'gc': InstructionCategory(
                'gc', 11.0, 0,
                "Garbage collection operations"
            ),
            'memory': InstructionCategory(
                'memory', 5.0, 0,
                "Memory access (tagged read/write)"
            ),
            'type_check': InstructionCategory(
                'type_check', 3.0, 0,
                "Type tag checking and dispatch"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'car_cdr': 0.15,
                'cons': 0.15,
                'eval': 0.20,
                'gc': 0.10,
                'memory': 0.20,
                'type_check': 0.20,
            }, "Typical LISP program workload"),
            'compute': WorkloadProfile('compute', {
                'car_cdr': 0.20,
                'cons': 0.15,
                'eval': 0.35,
                'gc': 0.05,
                'memory': 0.15,
                'type_check': 0.10,
            }, "Compute-intensive LISP workload"),
            'control': WorkloadProfile('control', {
                'car_cdr': 0.10,
                'cons': 0.05,
                'eval': 0.25,
                'gc': 0.05,
                'memory': 0.25,
                'type_check': 0.30,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'car_cdr': 0.05,
                'cons': 0.05,
                'eval': 0.10,
                'gc': 0.15,
                'memory': 0.45,
                'type_check': 0.20,
            }, "Memory-intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'car_cdr': 0.15,
                'cons': 0.10,
                'eval': 0.25,
                'gc': 0.10,
                'memory': 0.20,
                'type_check': 0.20,
            }, "Mixed LISP workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'car_cdr': 0.550108,
            'cons': -2.051844,
            'eval': 0.097846,
            'gc': 1.247537,
            'memory': 0.213264,
            'type_check': 0.191423
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze performance for a given workload profile."""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=corrected_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Validate the model against expected CPI target."""
        target_cpi = 5.0
        tolerance = 0.05

        tests: List[Dict[str, Any]] = []
        passed = 0

        result = self.analyze('typical')
        error = abs(result.cpi - target_cpi) / target_cpi
        test_passed = error <= tolerance
        tests.append({
            'name': 'typical_workload_cpi',
            'expected': target_cpi,
            'actual': result.cpi,
            'error_percent': error * 100,
            'passed': test_passed,
            'description': 'CPI for typical LISP workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'car_cdr': 2.0, 'cons': 4.0, 'eval': 7.0,
            'gc': 11.0, 'memory': 5.0, 'type_check': 3.0,
        }
        for cat_name, expected in expected_cycles.items():
            actual = self.instruction_categories[cat_name].total_cycles
            cat_passed = actual == expected
            tests.append({
                'name': f'{cat_name}_cycles',
                'expected': expected,
                'actual': actual,
                'passed': cat_passed,
                'description': f'Cycle count for {cat_name} operations'
            })
            if cat_passed:
                passed += 1

        for wl_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            ws_passed = abs(weight_sum - 1.0) < 0.001
            tests.append({
                'name': f'{wl_name}_weight_sum',
                'expected': 1.0,
                'actual': weight_sum,
                'passed': ws_passed,
                'description': f'Weight sum for {wl_name} workload'
            })
            if ws_passed:
                passed += 1

        for wl_name in self.workload_profiles:
            wl_result = self.analyze(wl_name)
            wl_passed = 3.0 <= wl_result.cpi <= 8.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '3.0-8.0',
                'actual': wl_result.cpi,
                'passed': wl_passed,
                'description': f'CPI range check for {wl_name} workload'
            })
            if wl_passed:
                passed += 1

        total = len(tests)
        accuracy = (passed / total * 100) if total > 0 else 0

        return {
            'processor': self.name,
            'target_cpi': target_cpi,
            'predicted_cpi': result.cpi,
            'cpi_error_percent': error * 100,
            'tests': tests,
            'passed': passed,
            'total': total,
            'accuracy_percent': accuracy,
            'validation_passed': passed == total
        }

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles


def create_model() -> LmiLambdaModel:
    return LmiLambdaModel()


if __name__ == '__main__':
    model = LmiLambdaModel()
    print(f"{model.name} Processor Model")
    print(f"Year: {model.year}, Clock: {model.clock_mhz} MHz")
    print()
    print("Instruction Categories:")
    for name, cat in model.instruction_categories.items():
        print(f"  {name}: {cat.total_cycles} cycles - {cat.description}")
    print()
    print("Workload Analysis:")
    for wl_name in model.workload_profiles:
        result = model.analyze(wl_name)
        print(f"  {wl_name}: CPI={result.cpi:.2f}, IPC={result.ipc:.3f}, "
              f"bottleneck={result.bottleneck}")
    print()
    print("Validation:")
    validation = model.validate()
    print(f"  Passed: {validation['passed']}/{validation['total']}")
    print(f"  Target CPI: {validation['target_cpi']}")
    print(f"  Predicted CPI: {validation['predicted_cpi']:.2f}")
    print(f"  CPI Error: {validation['cpi_error_percent']:.2f}%")
    print(f"  Validation: {'PASSED' if validation['validation_passed'] else 'FAILED'}")
