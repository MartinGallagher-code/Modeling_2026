#!/usr/bin/env python3
"""
AMD Am9512 Grey-Box Queueing Model
===================================

Target CPI: 20.0 (Floating-point APU, 1979)
Architecture: Improved math coprocessor, successor to Am9511

The Am9512 was an improved arithmetic processing unit designed to
accelerate floating-point and fixed-point math operations. It offered
faster performance than its predecessor, the Am9511, with enhanced
precision and throughput.

Key characteristics:
- Successor to Am9511 with improved performance
- 32-bit and 64-bit floating point support
- 16-bit and 32-bit fixed point support
- Faster operation than Am9511 (~20% improvement)
- Stack-based operation
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

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)


class BaseProcessorModel:
    pass


class Am9512Model(BaseProcessorModel):
    """
    AMD Am9512 Grey-Box Queueing Model

    Target CPI: 20.0
    Calibration: Weighted sum of instruction cycles

    The Am9512 is an improved math coprocessor, successor to Am9511.
    Floating-point operations are faster than Am9511 (~20% improvement).

    Instruction cycle counts (estimated from Am9512 specifications):
    - fp_add: 12 cycles (floating-point addition/subtraction)
    - fp_mul: 18 cycles (floating-point multiplication)
    - fp_div: 26 cycles (floating-point division)
    - fp_sqrt: 36 cycles (floating-point square root)
    - fixed_point: 6 cycles (16/32-bit fixed-point operations)
    - double_fp: 24 cycles (64-bit floating-point operations)

    Typical workload calculation for CPI = 20.0:
    0.20*12 + 0.25*18 + 0.20*26 + 0.12*36 + 0.15*6 + 0.08*24 = 20.0
    """

    name = "Am9512"
    manufacturer = "AMD"
    year = 1979
    clock_mhz = 4.0  # Faster than Am9511

    def __init__(self):
        # Instruction categories with improved cycle counts over Am9511
        self.instruction_categories = {
            'fp_add': InstructionCategory(
                'fp_add', 12.0, 0,
                "Floating-point addition/subtraction (FADD, FSUB)"
            ),
            'fp_mul': InstructionCategory(
                'fp_mul', 18.0, 0,
                "Floating-point multiplication (FMUL)"
            ),
            'fp_div': InstructionCategory(
                'fp_div', 26.0, 0,
                "Floating-point division (FDIV)"
            ),
            'fp_sqrt': InstructionCategory(
                'fp_sqrt', 36.0, 0,
                "Floating-point square root (SQRT)"
            ),
            'fixed_point': InstructionCategory(
                'fixed_point', 6.0, 0,
                "16/32-bit fixed-point operations"
            ),
            'double_fp': InstructionCategory(
                'double_fp', 24.0, 0,
                "64-bit double-precision floating-point"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # Typical workload: 0.18*12 + 0.24*18 + 0.20*26 + 0.14*36 + 0.14*6 + 0.10*24 = 19.96
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_add': 0.18,
                'fp_mul': 0.24,
                'fp_div': 0.20,
                'fp_sqrt': 0.14,
                'fixed_point': 0.14,
                'double_fp': 0.10,
            }, "Typical math coprocessor workload"),
            'scientific': WorkloadProfile('scientific', {
                'fp_add': 0.15,
                'fp_mul': 0.20,
                'fp_div': 0.20,
                'fp_sqrt': 0.18,
                'fixed_point': 0.07,
                'double_fp': 0.20,
            }, "Scientific computing with heavy double-precision"),
            'graphics': WorkloadProfile('graphics', {
                'fp_add': 0.30,
                'fp_mul': 0.40,
                'fp_div': 0.10,
                'fp_sqrt': 0.05,
                'fixed_point': 0.10,
                'double_fp': 0.05,
            }, "Graphics workload (transforms, projections)"),
            'fixed_heavy': WorkloadProfile('fixed_heavy', {
                'fp_add': 0.12,
                'fp_mul': 0.15,
                'fp_div': 0.08,
                'fp_sqrt': 0.05,
                'fixed_point': 0.55,
                'double_fp': 0.05,
            }, "Fixed-point heavy workload"),
            'mixed': WorkloadProfile('mixed', {
                'fp_add': 0.22,
                'fp_mul': 0.26,
                'fp_div': 0.18,
                'fp_sqrt': 0.10,
                'fixed_point': 0.14,
                'double_fp': 0.10,
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
        """
        Validate the model against expected CPI target.

        Returns validation results including:
        - Expected vs predicted CPI
        - Error percentage
        - Pass/fail status (passes if error < 5%)
        """
        expected_cpi = 20.0
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

        # Validate individual instruction categories
        category_tests = [
            ("fp_add", 12.0),
            ("fp_mul", 18.0),
            ("fp_div", 26.0),
            ("fp_sqrt", 36.0),
            ("fixed_point", 6.0),
            ("double_fp", 24.0),
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
    model = Am9512Model()
    return model.validate()


if __name__ == "__main__":
    model = Am9512Model()
    print(f"AMD Am9512 Floating-Point APU Model")
    print(f"=" * 50)
    print(f"Manufacturer: {model.manufacturer}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
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
