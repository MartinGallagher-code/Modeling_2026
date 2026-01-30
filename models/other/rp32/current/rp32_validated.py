#!/usr/bin/env python3
"""
Raytheon RP-32 Grey-Box Queueing Model
=========================================

Target CPI: 2.8
Architecture: 32-bit Military Bit-Slice Processor (1980s)

The Raytheon RP-32 was a 32-bit military-grade processor built
using bit-slice technology. Designed for defense applications
requiring radiation hardness and reliability, it featured a
cascaded bit-slice architecture with ALU, shift, and memory
operations typical of military computing systems.

Key characteristics:
- 32-bit data width (cascaded bit-slices)
- 10 MHz clock
- ~8,000 transistors
- Military-grade radiation-hardened
- Bit-slice cascaded architecture
- Used in defense computing systems
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


class Rp32Model(BaseProcessorModel):
    """
    Raytheon RP-32 Grey-Box Queueing Model

    Target CPI: 2.8
    Calibration: 32-bit military bit-slice processor

    The RP-32 used cascaded bit-slice components to create a
    32-bit processor for military applications. ALU and shift
    operations were relatively fast while memory and cascade
    operations added latency.
    """

    name = "Raytheon RP-32"
    manufacturer = "Raytheon"
    year = 1982
    clock_mhz = 10.0
    data_width = 32
    address_width = 24

    def __init__(self):
        # Typical: 0.20*2 + 0.20*2 + 0.20*4 + 0.20*3 + 0.20*3 = 2.80
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 2.0, 0,
                "ALU operations (cascaded bit-slice)"
            ),
            'shift': InstructionCategory(
                'shift', 2.0, 0,
                "Shift and rotate operations"
            ),
            'memory': InstructionCategory(
                'memory', 4.0, 0,
                "Memory access (military-spec bus)"
            ),
            'control': InstructionCategory(
                'control', 3.0, 0,
                "Control flow (branch, jump)"
            ),
            'cascade': InstructionCategory(
                'cascade', 3.0, 0,
                "Bit-slice cascade propagation"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.20,
                'shift': 0.20,
                'memory': 0.20,
                'control': 0.20,
                'cascade': 0.20,
            }, "Typical military computing workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.35,
                'shift': 0.25,
                'memory': 0.10,
                'control': 0.15,
                'cascade': 0.15,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.10,
                'shift': 0.10,
                'memory': 0.20,
                'control': 0.40,
                'cascade': 0.20,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.10,
                'shift': 0.05,
                'memory': 0.40,
                'control': 0.15,
                'cascade': 0.30,
            }, "Memory-intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'shift': 0.15,
                'memory': 0.25,
                'control': 0.15,
                'cascade': 0.20,
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
        target_cpi = 2.8
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
            'description': 'CPI for typical military computing workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'alu': 2.0, 'shift': 2.0, 'memory': 4.0,
            'control': 3.0, 'cascade': 3.0,
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
            wl_passed = 2.0 <= wl_result.cpi <= 4.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '2.0-4.0',
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


def create_model() -> Rp32Model:
    return Rp32Model()


if __name__ == '__main__':
    model = Rp32Model()
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
