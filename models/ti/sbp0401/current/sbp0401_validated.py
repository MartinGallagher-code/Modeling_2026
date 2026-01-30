#!/usr/bin/env python3
"""
TI SBP0401 Grey-Box Queueing Model
=====================================

Target CPI: 3.0
Architecture: 4-bit I2L Bit-Slice with Enhanced Control (1975)

The TI SBP0401 was a variant of the SBP0400 with enhanced control
logic. It maintained the same I2L process and similar performance
characteristics while adding improved microcode sequencing
capabilities.

Key characteristics:
- 4-bit slice, cascadable to 16-bit
- I2L (Integrated Injection Logic) technology
- Enhanced control over SBP0400
- ~2000 transistors per slice
- 10 MHz clock
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)


class BaseProcessorModel:
    pass


class Sbp0401Model(BaseProcessorModel):
    """
    TI SBP0401 Grey-Box Queueing Model

    Target CPI: 3.0
    Calibration: Weighted instruction mix for I2L bit-slice with enhanced control

    The SBP0401 variant adds enhanced control capabilities to the SBP0400.
    Same I2L process and CPI target, but with improved microcode sequencing.
    """

    name = "TI SBP0401"
    manufacturer = "Texas Instruments"
    year = 1975
    clock_mhz = 10.0
    transistor_count = 2000
    data_width = 4
    address_width = 16

    def __init__(self):
        # Same cycle counts as SBP0400 - same CPI target of 3.0
        # Typical: 0.30*2 + 0.15*3 + 0.20*2 + 0.20*4 + 0.15*5 = 3.00
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 2.0, 0,
                "ALU operations (ADD, SUB, INCR, DECR)"
            ),
            'shift': InstructionCategory(
                'shift', 3.0, 0,
                "Shift and rotate operations"
            ),
            'logic': InstructionCategory(
                'logic', 2.0, 0,
                "Logic operations (AND, OR, XOR, NOT)"
            ),
            'control': InstructionCategory(
                'control', 4.0, 0,
                "Enhanced microcode control and sequencing"
            ),
            'io': InstructionCategory(
                'io', 5.0, 0,
                "I/O and bus interface operations"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'shift': 0.15,
                'logic': 0.20,
                'control': 0.20,
                'io': 0.15,
            }, "Typical bit-slice workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'shift': 0.20,
                'logic': 0.20,
                'control': 0.10,
                'io': 0.05,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'shift': 0.10,
                'logic': 0.15,
                'control': 0.40,
                'io': 0.15,
            }, "Control-flow intensive (enhanced sequencing)"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.15,
                'shift': 0.10,
                'logic': 0.15,
                'control': 0.20,
                'io': 0.40,
            }, "I/O-heavy workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'shift': 0.18,
                'logic': 0.22,
                'control': 0.20,
                'io': 0.15,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 1.130394,
            'control': -1.032428,
            'io': -1.546681,
            'logic': 0.158900,
            'shift': 0.450598
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze performance for a given workload profile."""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            total_cpi += contrib
            contributions[cat_name] = contrib
        bottleneck = max(contributions, key=contributions.get)
        # System identification: apply correction terms
        base_cpi = total_cpi
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=corrected_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Validate the model against expected CPI target."""
        target_cpi = 3.0
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
            'description': 'CPI for typical bit-slice workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'alu': 2.0, 'shift': 3.0, 'logic': 2.0, 'control': 4.0, 'io': 5.0,
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
            wl_passed = 2.0 <= wl_result.cpi <= 5.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '2.0-5.0',
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


def create_model() -> Sbp0401Model:
    return Sbp0401Model()


if __name__ == '__main__':
    model = Sbp0401Model()
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
