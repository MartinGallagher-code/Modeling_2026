#!/usr/bin/env python3
"""
Motorola MC10800 Grey-Box Queueing Model
==========================================

Target CPI: 2.0
Architecture: 4-bit ECL Bit-Slice (1979)

The Motorola MC10800 was an ECL (Emitter-Coupled Logic) bit-slice
processor designed for maximum speed applications. It was used in
high-performance systems including the UNIVAC 1100/60 mainframe.

Key characteristics:
- 4-bit ECL bit-slice
- ~3000 transistors
- 50 MHz clock (extremely fast for 1979)
- Used in UNIVAC 1100/60
- ECL technology for minimum propagation delay
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


class Mc10800Model(BaseProcessorModel):
    """
    Motorola MC10800 Grey-Box Queueing Model

    Target CPI: 2.0
    Calibration: ECL bit-slice with very fast propagation

    The MC10800 leveraged ECL technology for extreme speed. At 50 MHz,
    it was one of the fastest processors available in 1979. ECL provides
    the lowest propagation delay of any logic family, enabling very
    low cycle counts.
    """

    name = "Motorola MC10800"
    manufacturer = "Motorola"
    year = 1979
    clock_mhz = 50.0
    transistor_count = 3000
    data_width = 4
    address_width = 4

    def __init__(self):
        # ECL is very fast - low cycle counts
        # Typical: 0.30*1.5 + 0.15*2.0 + 0.25*1.5 + 0.20*3.0 + 0.10*2.5
        #        = 0.45 + 0.30 + 0.375 + 0.60 + 0.25 = 1.975 ~ 2.0
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 1.5, 0,
                "ALU operations (ADD, SUB) - very fast ECL"
            ),
            'shift': InstructionCategory(
                'shift', 2.0, 0,
                "Shift and rotate operations"
            ),
            'logic': InstructionCategory(
                'logic', 1.5, 0,
                "Logic operations (AND, OR, XOR) - fast ECL"
            ),
            'control': InstructionCategory(
                'control', 3.0, 0,
                "Microsequencer control operations"
            ),
            'cascade': InstructionCategory(
                'cascade', 2.5, 0,
                "Cascade/carry propagation between slices"
            ),
        }

        # Typical: 0.30*1.5 + 0.15*2.0 + 0.25*1.5 + 0.20*3.0 + 0.10*2.5 = 1.975
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'shift': 0.15,
                'logic': 0.25,
                'control': 0.20,
                'cascade': 0.10,
            }, "Typical ECL bit-slice workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'shift': 0.20,
                'logic': 0.20,
                'control': 0.10,
                'cascade': 0.05,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'shift': 0.10,
                'logic': 0.20,
                'control': 0.40,
                'cascade': 0.10,
            }, "Control-intensive workload"),
            'cascaded': WorkloadProfile('cascaded', {
                'alu': 0.25,
                'shift': 0.10,
                'logic': 0.20,
                'control': 0.15,
                'cascade': 0.30,
            }, "Multi-slice cascade-heavy workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.28,
                'shift': 0.17,
                'logic': 0.25,
                'control': 0.18,
                'cascade': 0.12,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 1.037783,
            'cascade': 0.231583,
            'control': -1.014266,
            'logic': 0.135690,
            'shift': -1.021464
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
        target_cpi = 2.0
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
            'description': 'CPI for typical ECL bit-slice workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'alu': 1.5, 'shift': 2.0, 'logic': 1.5, 'control': 3.0, 'cascade': 2.5,
        }
        for cat_name, expected in expected_cycles.items():
            actual = self.instruction_categories[cat_name].total_cycles
            cat_passed = actual == expected
            tests.append({
                'name': f'{cat_name}_cycles',
                'expected': expected,
                'actual': actual,
                'passed': cat_passed,
                'description': f'Cycle count for {cat_name} instructions'
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
            wl_passed = 1.5 <= wl_result.cpi <= 3.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '1.5-3.0',
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


def create_model() -> Mc10800Model:
    return Mc10800Model()


if __name__ == '__main__':
    model = Mc10800Model()
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
