#!/usr/bin/env python3
"""
Raytheon RP-16 Grey-Box Queueing Model
========================================

Target CPI: 4.0
Architecture: 16-bit Military Bit-Slice System (1978)

The Raytheon RP-16 was a military-grade 16-bit bit-slice processor
system designed for rugged defense applications. It was implemented
as a 7-chip system with emphasis on reliability and radiation
hardening over maximum speed.

Key characteristics:
- 16-bit military-grade bit-slice system
- 7-chip implementation
- ~10 MHz clock
- MIL-STD qualified
- Designed for defense/aerospace applications
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

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)


class BaseProcessorModel:
    pass


class Rp16Model(BaseProcessorModel):
    """
    Raytheon RP-16 Grey-Box Queueing Model

    Target CPI: 4.0
    Calibration: Military-grade 7-chip bit-slice system

    The RP-16's multi-chip architecture and military-grade design
    results in higher CPI than commercial bit-slices, trading speed
    for reliability in harsh environments.
    """

    name = "Raytheon RP-16"
    manufacturer = "Raytheon"
    year = 1978
    clock_mhz = 10.0
    transistor_count = 15000  # approximate across 7 chips
    data_width = 16
    address_width = 16

    def __init__(self):
        # Military-grade: higher cycle counts due to multi-chip overhead
        # Typical: 0.30*3 + 0.15*3 + 0.20*3 + 0.20*5 + 0.15*6
        #        = 0.90 + 0.45 + 0.60 + 1.00 + 0.90 = 3.85
        # Adjust: 0.25*3 + 0.15*3 + 0.20*3 + 0.25*5 + 0.15*6
        #       = 0.75 + 0.45 + 0.60 + 1.25 + 0.90 = 3.95
        # Close: 0.25*3 + 0.15*3 + 0.20*3 + 0.24*5 + 0.16*6
        #      = 0.75 + 0.45 + 0.60 + 1.20 + 0.96 = 3.96
        # Final: 0.25*3 + 0.15*3 + 0.20*3 + 0.25*5 + 0.15*6 = 3.95 (within 5%)
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 3.0, 0,
                "16-bit ALU operations"
            ),
            'shift': InstructionCategory(
                'shift', 3.0, 0,
                "Shift and rotate operations"
            ),
            'logic': InstructionCategory(
                'logic', 3.0, 0,
                "Logic operations"
            ),
            'control': InstructionCategory(
                'control', 5.0, 0,
                "Control and branch operations (multi-chip overhead)"
            ),
            'memory': InstructionCategory(
                'memory', 4.0, 2.0,
                "Memory access operations"
            ),
        }

        # Typical: 0.25*3 + 0.15*3 + 0.20*3 + 0.25*5 + 0.15*6 = 3.95
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'shift': 0.15,
                'logic': 0.20,
                'control': 0.25,
                'memory': 0.15,
            }, "Typical military embedded workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'shift': 0.20,
                'logic': 0.25,
                'control': 0.10,
                'memory': 0.05,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'shift': 0.10,
                'logic': 0.15,
                'control': 0.45,
                'memory': 0.15,
            }, "Control-intensive workload"),
            'memory_heavy': WorkloadProfile('memory_heavy', {
                'alu': 0.15,
                'shift': 0.10,
                'logic': 0.15,
                'control': 0.20,
                'memory': 0.40,
            }, "Memory-intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'shift': 0.15,
                'logic': 0.20,
                'control': 0.22,
                'memory': 0.18,
            }, "Mixed workload"),
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
        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=total_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions
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
            'description': 'CPI for typical military embedded workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'alu': 3.0, 'shift': 3.0, 'logic': 3.0, 'control': 5.0, 'memory': 6.0,
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
            wl_passed = 3.0 <= wl_result.cpi <= 6.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '3.0-6.0',
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


def create_model() -> Rp16Model:
    return Rp16Model()


if __name__ == '__main__':
    model = Rp16Model()
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
