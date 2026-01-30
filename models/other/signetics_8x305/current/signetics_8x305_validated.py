#!/usr/bin/env python3
"""
Signetics 8X305 Grey-Box Queueing Model
==========================================

Target CPI: 2.0
Architecture: 8-bit Enhanced Bipolar Signal Processor (1982)

The Signetics 8X305 was an enhanced version of the 8X300 bipolar
signal processor, designed for high-speed I/O-intensive applications.
It featured fast register-based ALU operations and optimized
bus transfer operations for signal processing and communications.

Key characteristics:
- 8-bit data width
- 8 MHz clock
- ~5,000 transistors
- Bipolar Schottky technology
- Register-based architecture
- Optimized for I/O-intensive applications
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


class Signetics8x305Model(BaseProcessorModel):
    """
    Signetics 8X305 Grey-Box Queueing Model

    Target CPI: 2.0
    Calibration: Enhanced bipolar signal processor

    The 8X305 featured single-cycle ALU operations with multi-cycle
    transfers and I/O operations for signal processing applications.
    """

    name = "Signetics 8X305"
    manufacturer = "Signetics"
    year = 1982
    clock_mhz = 8.0
    data_width = 8
    address_width = 13

    def __init__(self):
        # Typical: 0.20*1 + 0.25*2 + 0.10*3 + 0.35*2 + 0.10*3 = 2.00
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 1.0, 0,
                "ALU operations (single-cycle register ops)"
            ),
            'transfer': InstructionCategory(
                'transfer', 2.0, 0,
                "Data transfer between registers/buses"
            ),
            'io': InstructionCategory(
                'io', 3.0, 0,
                "I/O bus operations"
            ),
            'control': InstructionCategory(
                'control', 2.0, 0,
                "Control flow (branch, conditional)"
            ),
            'memory': InstructionCategory(
                'memory', 3.0, 0,
                "External memory access"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.20,
                'transfer': 0.25,
                'io': 0.10,
                'control': 0.35,
                'memory': 0.10,
            }, "Typical signal processing workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'transfer': 0.25,
                'io': 0.05,
                'control': 0.25,
                'memory': 0.05,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.10,
                'transfer': 0.15,
                'io': 0.10,
                'control': 0.50,
                'memory': 0.15,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.10,
                'transfer': 0.20,
                'io': 0.35,
                'control': 0.15,
                'memory': 0.20,
            }, "I/O-intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.20,
                'transfer': 0.20,
                'io': 0.20,
                'control': 0.20,
                'memory': 0.20,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
        bottleneck = max(contributions, key=contributions.get)
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
            'description': 'CPI for typical signal processing workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'alu': 1.0, 'transfer': 2.0, 'io': 3.0,
            'control': 2.0, 'memory': 3.0,
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
            wl_passed = 1.0 <= wl_result.cpi <= 3.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '1.0-3.0',
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


def create_model() -> Signetics8x305Model:
    return Signetics8x305Model()


if __name__ == '__main__':
    model = Signetics8x305Model()
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
