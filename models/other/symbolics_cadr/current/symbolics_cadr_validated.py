#!/usr/bin/env python3
"""
Symbolics CADR Grey-Box Queueing Model
=========================================

Target CPI: 5.5
Architecture: 32-bit Tagged LISP Machine CPU (1981)

The Symbolics CADR was the CPU of the CADR LISP machine, developed
at the MIT AI Lab and commercialized by Symbolics. It was a
microcoded processor with tagged architecture supporting native
LISP operations including CAR/CDR, CONS, and garbage collection.

Key characteristics:
- 32-bit tagged data width
- 5 MHz clock
- ~50,000 transistors
- Microcoded architecture
- Hardware type checking via tags
- Native LISP operations (CAR, CDR, CONS)
- Hardware-assisted garbage collection
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                   base_cpi=base_cpi if base_cpi is not None else cpi,
                   correction_delta=correction_delta)


class BaseProcessorModel:
    pass


class SymbolicsCadrModel(BaseProcessorModel):
    """
    Symbolics CADR Grey-Box Queueing Model

    Target CPI: 5.5
    Calibration: Microcoded LISP machine with tagged architecture

    The CADR was a microcoded processor designed specifically for
    LISP execution, with hardware support for tagged data types,
    CAR/CDR operations, and garbage collection.
    """

    name = "Symbolics CADR"
    manufacturer = "Symbolics (MIT AI Lab)"
    year = 1981
    clock_mhz = 5.0
    data_width = 32
    address_width = 24

    def __init__(self):
        # Typical: 0.15*2 + 0.10*5 + 0.25*8 + 0.05*12 + 0.25*6 + 0.20*3 = 5.50
        self.instruction_categories = {
            'car_cdr': InstructionCategory(
                'car_cdr', 2.0, 0,
                "CAR/CDR list operations (hardware-assisted)"
            ),
            'cons': InstructionCategory(
                'cons', 5.0, 0,
                "CONS cell allocation (memory allocation + pointer setup)"
            ),
            'eval': InstructionCategory(
                'eval', 8.0, 0,
                "Evaluation/function dispatch (microcoded)"
            ),
            'gc': InstructionCategory(
                'gc', 12.0, 0,
                "Garbage collection operations"
            ),
            'memory': InstructionCategory(
                'memory', 6.0, 0,
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
                'cons': 0.10,
                'eval': 0.25,
                'gc': 0.05,
                'memory': 0.25,
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
                'eval': 0.30,
                'gc': 0.05,
                'memory': 0.20,
                'type_check': 0.30,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'car_cdr': 0.05,
                'cons': 0.05,
                'eval': 0.10,
                'gc': 0.10,
                'memory': 0.50,
                'type_check': 0.20,
            }, "Memory-intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'car_cdr': 0.15,
                'cons': 0.15,
                'eval': 0.20,
                'gc': 0.10,
                'memory': 0.20,
                'type_check': 0.20,
            }, "Mixed LISP workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'car_cdr': -0.592365,
            'cons': -0.778561,
            'eval': -1.906034,
            'gc': -4.633551,
            'memory': 2.801913,
            'type_check': 1.887585
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
        target_cpi = 5.5
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
            'car_cdr': 2.0, 'cons': 5.0, 'eval': 8.0,
            'gc': 12.0, 'memory': 6.0, 'type_check': 3.0,
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


def create_model() -> SymbolicsCadrModel:
    return SymbolicsCadrModel()


if __name__ == '__main__':
    model = SymbolicsCadrModel()
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
