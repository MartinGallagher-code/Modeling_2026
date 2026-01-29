#!/usr/bin/env python3
"""
AMI S28211 Grey-Box Queueing Model
=====================================

Target CPI: 5.0
Architecture: DSP Peripheral for Motorola 6800 Bus (1979)

The AMI S28211 was a DSP peripheral chip designed to interface with
the Motorola 6800 bus system. Unlike standalone DSPs, it operated
as a coprocessor/peripheral, adding signal processing capability
to 6800-based systems.

Key characteristics:
- DSP peripheral for Motorola 6800 bus
- 8 MHz clock
- ~5000 transistors
- Bus-attached coprocessor architecture
- Higher CPI due to bus interface overhead
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


class AmiS28211Model(BaseProcessorModel):
    """
    AMI S28211 Grey-Box Queueing Model

    Target CPI: 5.0
    Calibration: DSP peripheral with 6800 bus interface overhead

    The S28211 operated as a bus-attached peripheral, which adds
    significant overhead compared to standalone DSPs. Communication
    with the host 6800 CPU through the bus interface increases
    effective CPI for I/O-heavy operations.
    """

    name = "AMI S28211"
    manufacturer = "AMI"
    year = 1979
    clock_mhz = 8.0
    transistor_count = 5000
    data_width = 16
    address_width = 16

    def __init__(self):
        # DSP peripheral: bus interface adds overhead
        # Typical: 0.20*4 + 0.20*3 + 0.15*4 + 0.20*6 + 0.15*8 + 0.10*...
        # With 5 categories:
        # 0.20*4 + 0.25*3 + 0.15*4 + 0.20*6 + 0.20*8
        # = 0.80 + 0.75 + 0.60 + 1.20 + 1.60 = 4.95
        # Close enough: 0.20*4+0.25*3+0.15*4+0.20*6+0.20*8 = 4.95 (1.0% err)
        self.instruction_categories = {
            'mac': InstructionCategory(
                'mac', 4.0, 0,
                "Multiply-accumulate (multi-cycle, no hardware MAC)"
            ),
            'alu': InstructionCategory(
                'alu', 3.0, 0,
                "ALU operations (add, subtract)"
            ),
            'data_move': InstructionCategory(
                'data_move', 4.0, 0,
                "Data move via 6800 bus interface"
            ),
            'control': InstructionCategory(
                'control', 6.0, 0,
                "Control flow operations"
            ),
            'io': InstructionCategory(
                'io', 8.0, 0,
                "I/O through 6800 bus (high overhead)"
            ),
        }

        # Typical: 0.20*4+0.25*3+0.15*4+0.20*6+0.20*8 = 4.95
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'mac': 0.20,
                'alu': 0.25,
                'data_move': 0.15,
                'control': 0.20,
                'io': 0.20,
            }, "Typical DSP peripheral workload"),
            'compute': WorkloadProfile('compute', {
                'mac': 0.35,
                'alu': 0.30,
                'data_move': 0.15,
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
                'data_move': 0.20,
                'control': 0.15,
                'io': 0.45,
            }, "I/O-intensive (heavy bus traffic)"),
            'mixed': WorkloadProfile('mixed', {
                'mac': 0.22,
                'alu': 0.23,
                'data_move': 0.15,
                'control': 0.20,
                'io': 0.20,
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
            'description': 'CPI for typical DSP peripheral workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'mac': 4.0, 'alu': 3.0, 'data_move': 4.0,
            'control': 6.0, 'io': 8.0,
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


def create_model() -> AmiS28211Model:
    return AmiS28211Model()


if __name__ == '__main__':
    model = AmiS28211Model()
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
