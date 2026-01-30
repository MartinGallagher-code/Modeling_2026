#!/usr/bin/env python3
"""
AT&T DSP-20 Grey-Box Queueing Model
======================================

Target CPI: 3.0
Architecture: 16-bit Improved Bell Labs DSP (1983)

The AT&T DSP-20 was an improved version of the DSP-1, also developed
at Bell Labs. It featured better performance with lower CPI, operating
at 10 MHz. Like its predecessor, it was primarily used internally
within AT&T for telecommunications applications.

Key characteristics:
- 16-bit data width
- 10 MHz clock (doubled from DSP-1)
- Improved microcode efficiency
- Used in AT&T telecom equipment
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


class AttDsp20Model(BaseProcessorModel):
    """
    AT&T DSP-20 Grey-Box Queueing Model

    Target CPI: 3.0
    Calibration: Improved Bell Labs DSP with better microcode

    The DSP-20 improved on the DSP-1 with more efficient microcode
    and doubled clock speed, reducing CPI from 4.0 to 3.0 while
    maintaining telecommunications focus.
    """

    name = "AT&T DSP-20"
    manufacturer = "AT&T Bell Labs"
    year = 1983
    clock_mhz = 10.0
    data_width = 16
    address_width = 16

    def __init__(self):
        # Improved over DSP-1: lower cycle counts
        # Typical: 0.25*2 + 0.20*2 + 0.20*2 + 0.20*4 + 0.15*5
        #        = 0.50 + 0.40 + 0.40 + 0.80 + 0.75 = 2.85
        # Adjust: 0.20*2 + 0.20*2 + 0.20*2 + 0.25*4 + 0.15*5
        #       = 0.40 + 0.40 + 0.40 + 1.00 + 0.75 = 2.95
        # Final:  0.20*2 + 0.20*2 + 0.15*2 + 0.25*4 + 0.20*5
        #       = 0.40 + 0.40 + 0.30 + 1.00 + 1.00 = 3.10
        # Best:   0.20*2 + 0.20*2 + 0.20*2 + 0.25*4 + 0.15*5 = 2.95 (1.67% err)
        self.instruction_categories = {
            'mac': InstructionCategory(
                'mac', 2.0, 0,
                "Multiply-accumulate (improved over DSP-1)"
            ),
            'alu': InstructionCategory(
                'alu', 2.0, 0,
                "ALU operations (add, subtract)"
            ),
            'data_move': InstructionCategory(
                'data_move', 2.0, 0,
                "Data move operations"
            ),
            'control': InstructionCategory(
                'control', 4.0, 0,
                "Control flow operations"
            ),
            'io': InstructionCategory(
                'io', 5.0, 0,
                "I/O and peripheral interface"
            ),
        }

        # Typical: 0.20*2+0.20*2+0.20*2+0.25*4+0.15*5 = 2.95
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'mac': 0.20,
                'alu': 0.20,
                'data_move': 0.20,
                'control': 0.25,
                'io': 0.15,
            }, "Typical telecom DSP workload"),
            'compute': WorkloadProfile('compute', {
                'mac': 0.35,
                'alu': 0.25,
                'data_move': 0.20,
                'control': 0.15,
                'io': 0.05,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'mac': 0.10,
                'alu': 0.15,
                'data_move': 0.15,
                'control': 0.45,
                'io': 0.15,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'mac': 0.10,
                'alu': 0.10,
                'data_move': 0.15,
                'control': 0.25,
                'io': 0.40,
            }, "I/O-intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'mac': 0.22,
                'alu': 0.20,
                'data_move': 0.18,
                'control': 0.22,
                'io': 0.18,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -5.000000,
            'control': 0.799501,
            'data_move': 2.525521,
            'io': -0.033878,
            'mac': 1.534402
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
            'description': 'CPI for typical telecom DSP workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'mac': 2.0, 'alu': 2.0, 'data_move': 2.0,
            'control': 4.0, 'io': 5.0,
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


def create_model() -> AttDsp20Model:
    return AttDsp20Model()


if __name__ == '__main__':
    model = AttDsp20Model()
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
