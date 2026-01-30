#!/usr/bin/env python3
"""
TI Explorer Grey-Box Queueing Model
======================================

Target CPI: 4.0
Architecture: 32-bit Tagged LISP Machine CPU (1985)

The TI Explorer was Texas Instruments' LISP machine processor,
an improved design with pipelined elements that reduced CPI
compared to earlier LISP machines like the Symbolics CADR.
It featured hardware type checking and native LISP operations.

Key characteristics:
- 32-bit tagged data width
- 8 MHz clock
- ~80,000 transistors
- Pipelined microcode execution
- Hardware type tag checking
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                   base_cpi=base_cpi if base_cpi is not None else cpi,
                   correction_delta=correction_delta)


class BaseProcessorModel:
    pass


class TiExplorerModel(BaseProcessorModel):
    """
    TI Explorer Grey-Box Queueing Model

    Target CPI: 4.0
    Calibration: Pipelined LISP machine with improved microcode

    The TI Explorer improved on the CADR design with pipelined
    microcode execution, reducing cycle counts for common LISP
    operations while maintaining tagged architecture support.
    """

    name = "TI Explorer"
    manufacturer = "Texas Instruments"
    year = 1985
    clock_mhz = 8.0
    data_width = 32
    address_width = 24

    def __init__(self):
        # Typical: 0.15*1 + 0.10*3 + 0.20*6 + 0.10*10 + 0.225*4 + 0.225*2 = 4.00
        self.instruction_categories = {
            'car_cdr': InstructionCategory(
                'car_cdr', 1.0, 0,
                "CAR/CDR list operations (pipelined, single-cycle)"
            ),
            'cons': InstructionCategory(
                'cons', 3.0, 0,
                "CONS cell allocation (improved allocator)"
            ),
            'eval': InstructionCategory(
                'eval', 6.0, 0,
                "Evaluation/function dispatch (pipelined microcode)"
            ),
            'gc': InstructionCategory(
                'gc', 10.0, 0,
                "Garbage collection operations"
            ),
            'memory': InstructionCategory(
                'memory', 4.0, 0,
                "Memory access (tagged read/write)"
            ),
            'type_check': InstructionCategory(
                'type_check', 2.0, 0,
                "Type tag checking (improved hardware)"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'car_cdr': 0.15,
                'cons': 0.10,
                'eval': 0.20,
                'gc': 0.10,
                'memory': 0.225,
                'type_check': 0.225,
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
                'cons': 0.10,
                'eval': 0.10,
                'gc': 0.15,
                'memory': 0.45,
                'type_check': 0.15,
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
            'car_cdr': -0.479599,
            'cons': -1.614048,
            'eval': -0.519192,
            'gc': -0.207920,
            'memory': 1.107823,
            'type_check': 1.139669
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
        target_cpi = 4.0
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
            'car_cdr': 1.0, 'cons': 3.0, 'eval': 6.0,
            'gc': 10.0, 'memory': 4.0, 'type_check': 2.0,
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
            wl_passed = 2.0 <= wl_result.cpi <= 7.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '2.0-7.0',
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


def create_model() -> TiExplorerModel:
    return TiExplorerModel()


if __name__ == '__main__':
    model = TiExplorerModel()
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
