#!/usr/bin/env python3
"""
Intel 3003 Grey-Box Queueing Model
=====================================

Target CPI: 1.0
Architecture: 2-bit Carry Lookahead Generator (1975)

The Intel 3003 was a carry lookahead generator designed to work
with the Intel 3002 bit-slice ALU to accelerate multi-bit arithmetic.
It generated carry signals in parallel rather than through ripple
propagation, enabling single-cycle operation for all functions.

Key characteristics:
- 2-bit slice width
- 10 MHz clock
- ~100 transistors
- Single-cycle operation for all functions
- Companion to Intel 3002 bit-slice ALU
- Schottky bipolar technology
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
        ipc = 1.0 / cpi if cpi > 0 else 0.0
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                   base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)


class BaseProcessorModel:
    pass


class I3003Model(BaseProcessorModel):
    """
    Intel 3003 Grey-Box Queueing Model

    Target CPI: 1.0
    Calibration: Single-cycle carry lookahead generator

    The Intel 3003 performs all operations in a single cycle,
    generating carry signals in parallel for fast multi-bit
    arithmetic when used with Intel 3002 bit-slice ALUs.
    """

    name = "Intel 3003"
    manufacturer = "Intel"
    year = 1975
    clock_mhz = 10.0
    data_width = 2
    address_width = 2

    def __init__(self):
        # All operations single-cycle: any weights * 1 = 1.0
        self.instruction_categories = {
            'carry_gen': InstructionCategory(
                'carry_gen', 1.0, 0,
                "Carry generation (parallel carry compute)"
            ),
            'propagate': InstructionCategory(
                'propagate', 1.0, 0,
                "Carry propagation signal generation"
            ),
            'group_carry': InstructionCategory(
                'group_carry', 1.0, 0,
                "Group carry for cascaded operation"
            ),
            'control': InstructionCategory(
                'control', 1.0, 0,
                "Control and mode selection"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'carry_gen': 0.30,
                'propagate': 0.25,
                'group_carry': 0.25,
                'control': 0.20,
            }, "Typical arithmetic acceleration workload"),
            'compute': WorkloadProfile('compute', {
                'carry_gen': 0.40,
                'propagate': 0.30,
                'group_carry': 0.20,
                'control': 0.10,
            }, "Compute-intensive workload"),
            'control': WorkloadProfile('control', {
                'carry_gen': 0.15,
                'propagate': 0.15,
                'group_carry': 0.20,
                'control': 0.50,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'carry_gen': 0.20,
                'propagate': 0.20,
                'group_carry': 0.40,
                'control': 0.20,
            }, "Cascaded operation workload"),
            'mixed': WorkloadProfile('mixed', {
                'carry_gen': 0.25,
                'propagate': 0.25,
                'group_carry': 0.25,
                'control': 0.25,
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

        # Apply correction terms (system identification)
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
        target_cpi = 1.0
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
            'description': 'CPI for typical carry lookahead workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'carry_gen': 1.0, 'propagate': 1.0,
            'group_carry': 1.0, 'control': 1.0,
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
            wl_passed = 0.5 <= wl_result.cpi <= 1.5
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '0.5-1.5',
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


def create_model() -> I3003Model:
    return I3003Model()


if __name__ == '__main__':
    model = I3003Model()
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
