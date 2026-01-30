#!/usr/bin/env python3
"""
Intel 3001/3002 Grey-Box Queueing Model
========================================

Target CPI: 1.0 (per micro-op)
Architecture: 2-bit slice processor (1974)

The Intel 3001/3002 was Intel's entry into the bit-slice market.
The 3002 is a 2-bit ALU slice, while the 3001 is the microprogram
control unit. Multiple 3002 slices are cascaded for wider data paths.

Key characteristics:
- 2-bit slice (vs AMD's 4-bit Am2901)
- Schottky bipolar technology
- Single-cycle microinstructions
- 11 general-purpose registers per slice
"""

from dataclasses import dataclass
from typing import Dict, Any


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


class I3002Model(BaseProcessorModel):
    """
    Intel 3001/3002 Grey-Box Queueing Model

    Target CPI: 1.0 (microinstruction level)
    Calibration: All microinstructions execute in single cycle

    The 3002 is a 2-bit slice ALU component. Like other bit-slice
    processors, all microinstructions complete in a single clock cycle.
    """

    name = "Intel 3002"
    manufacturer = "Intel"
    year = 1974
    clock_mhz = 5.0  # Typical clock frequency
    transistor_count = 125  # Approximate per slice
    data_width = 2  # 2-bit slice
    address_width = 2

    def __init__(self):
        # Bit-slice: all operations are single-cycle microinstructions
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 1.0, 0,
                "ALU operations (ADD, SUB, AND, OR, XOR, etc.)"
            ),
            'shift': InstructionCategory(
                'shift', 1.0, 0,
                "Shift operations (left/right)"
            ),
            'pass': InstructionCategory(
                'pass', 1.0, 0,
                "Pass through (data routing)"
            ),
            'load': InstructionCategory(
                'load', 1.0, 0,
                "Load register operations"
            ),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.55,
                'shift': 0.20,
                'pass': 0.15,
                'load': 0.10,
            }, "Typical microcode workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.70,
                'shift': 0.15,
                'pass': 0.10,
                'load': 0.05,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.35,
                'shift': 0.10,
                'pass': 0.40,
                'load': 0.15,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.45,
                'shift': 0.15,
                'pass': 0.25,
                'load': 0.15,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.50,
                'shift': 0.20,
                'pass': 0.20,
                'load': 0.10,
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
        """
        Validate the model against expected CPI target.

        Returns validation results including:
        - Expected vs predicted CPI
        - Error percentage
        - Pass/fail status (passes if error < 5%)
        """
        expected_cpi = 1.0
        result = self.analyze('typical')
        predicted_cpi = result.cpi
        error_pct = abs(predicted_cpi - expected_cpi) / expected_cpi * 100

        tests = [
            {
                "name": "CPI accuracy",
                "expected": expected_cpi,
                "predicted": predicted_cpi,
                "error_percent": error_pct,
                "passed": error_pct < 5.0
            }
        ]

        # Validate individual instruction categories (all should be 1 cycle)
        category_tests = [
            ("alu", 1.0),
            ("shift", 1.0),
            ("pass", 1.0),
            ("load", 1.0),
        ]
        for cat_name, expected_cycles in category_tests:
            actual = self.instruction_categories[cat_name].total_cycles
            cat_error = abs(actual - expected_cycles) / expected_cycles * 100
            tests.append({
                "name": f"{cat_name} cycles",
                "expected": expected_cycles,
                "predicted": actual,
                "error_percent": cat_error,
                "passed": cat_error < 5.0
            })

        passed = sum(1 for t in tests if t["passed"])
        total = len(tests)

        return {
            "processor": self.name,
            "target_cpi": expected_cpi,
            "predicted_cpi": predicted_cpi,
            "cpi_error_percent": error_pct,
            "tests": tests,
            "passed": passed,
            "total": total,
            "accuracy_percent": (passed / total) * 100 if total > 0 else None,
            "validation_passed": error_pct < 5.0
        }

    def get_instruction_categories(self):
        """Return instruction categories dictionary."""
        return self.instruction_categories

    def get_workload_profiles(self):
        """Return workload profiles dictionary."""
        return self.workload_profiles


def validate():
    """Module-level validation function."""
    model = I3002Model()
    return model.validate()


if __name__ == "__main__":
    model = I3002Model()
    print(f"Intel 3001/3002 Bit-Slice Processor Model")
    print(f"=" * 50)
    print(f"Manufacturer: {model.manufacturer}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"Data Width: {model.data_width}-bit slice")
    print()
    print("Instruction Categories:")
    for name, cat in model.instruction_categories.items():
        print(f"  {name}: {cat.total_cycles} cycles - {cat.description}")
    print()
    print("Workload Analysis:")
    for workload in model.workload_profiles:
        result = model.analyze(workload)
        print(f"  {workload}: CPI={result.cpi:.2f}, IPC={result.ipc:.4f}, "
              f"IPS={result.ips:.0f}, bottleneck={result.bottleneck}")
    print()
    print("Validation:")
    validation = model.validate()
    print(f"  Target CPI: {validation['target_cpi']}")
    print(f"  Predicted CPI: {validation['predicted_cpi']:.2f}")
    print(f"  Error: {validation['cpi_error_percent']:.2f}%")
    print(f"  Passed: {validation['passed']}/{validation['total']} tests")
    print(f"  Validation: {'PASSED' if validation['validation_passed'] else 'FAILED'}")
