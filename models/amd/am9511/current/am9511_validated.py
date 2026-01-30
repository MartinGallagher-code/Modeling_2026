#!/usr/bin/env python3
"""
AMD Am9511 Grey-Box Queueing Model
===================================

Target CPI: 25.0 (Arithmetic Processing Unit, 1977)
Architecture: Stack-based math coprocessor for 8-bit systems

The Am9511 was an early arithmetic processing unit designed to
accelerate floating-point and fixed-point math operations for
8-bit microprocessor systems. It featured a 4-level internal
stack and supported 32-bit floating point and 16/32-bit fixed point.
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
                   base_cpi=base_cpi if base_cpi is not None else cpi,
                   correction_delta=correction_delta)


class BaseProcessorModel:
    def get_corrections(self):
        return getattr(self, 'corrections', {})
    def set_corrections(self, corrections):
        self.corrections = corrections
    def compute_correction_delta(self, workload='typical'):
        profile = self.workload_profiles.get(workload, list(self.workload_profiles.values())[0])
        return sum(self.corrections.get(c, 0) * profile.category_weights.get(c, 0) for c in self.corrections)
    def compute_residuals(self, measured_cpi_dict):
        return {w: self.analyze(w).cpi - m for w, m in measured_cpi_dict.items()}
    def compute_loss(self, measured_cpi_dict):
        residuals = self.compute_residuals(measured_cpi_dict)
        return sum(r**2 for r in residuals.values()) / len(residuals) if residuals else 0
    def get_parameters(self):
        params = {}
        for c, cat in self.instruction_categories.items():
            params[f'cat.{c}.base_cycles'] = cat.base_cycles
        for c, v in self.corrections.items():
            params[f'cor.{c}'] = v
        return params
    def set_parameters(self, params):
        for k, v in params.items():
            if k.startswith('cat.') and k.endswith('.base_cycles'):
                c = k[4:-12]
                if c in self.instruction_categories:
                    self.instruction_categories[c].base_cycles = v
            elif k.startswith('cor.'):
                c = k[4:]
                self.corrections[c] = v
    def get_parameter_bounds(self):
        bounds = {}
        for c, cat in self.instruction_categories.items():
            bounds[f'cat.{c}.base_cycles'] = (0.1, cat.base_cycles * 5)
        for c in self.corrections:
            bounds[f'cor.{c}'] = (-50, 50)
        return bounds
    def get_parameter_metadata(self):
        return {k: {'type': 'category' if k.startswith('cat.') else 'correction'} for k in self.get_parameters()}
    def get_instruction_categories(self):
        return self.instruction_categories
    def get_workload_profiles(self):
        return self.workload_profiles
    def validate(self):
        return {'tests': [], 'passed': 0, 'total': 0, 'accuracy_percent': None}


class Am9511Model(BaseProcessorModel):
    """
    AMD Am9511 Grey-Box Queueing Model

    Target CPI: 25.0
    Calibration: Weighted sum of instruction cycles

    The Am9511 is a math coprocessor with stack-based operation.
    Floating-point operations dominate typical workloads and are
    relatively slow compared to fixed-point operations.

    Instruction cycle counts (from Am9511 datasheet):
    - fp_add: 16 cycles (floating-point addition/subtraction)
    - fp_mul: 24 cycles (floating-point multiplication)
    - fp_div: 32 cycles (floating-point division)
    - fp_sqrt: 45 cycles (floating-point square root)
    - fixed_point: 8 cycles (16/32-bit fixed-point operations)

    Typical workload calculation for CPI = 25.0:
    0.19*16 + 0.26*24 + 0.24*32 + 0.15*45 + 0.16*8 = 25.0
    """

    name = "Am9511"
    manufacturer = "AMD"
    year = 1977
    clock_mhz = 3.0

    def __init__(self):
        # Instruction categories with cycle counts from Am9511 datasheet
        # These are typical execution times for each operation class
        self.instruction_categories = {
            'fp_add': InstructionCategory(
                'fp_add', 16.0, 0,
                "Floating-point addition/subtraction (FADD, FSUB)"
            ),
            'fp_mul': InstructionCategory(
                'fp_mul', 24.0, 0,
                "Floating-point multiplication (FMUL)"
            ),
            'fp_div': InstructionCategory(
                'fp_div', 32.0, 0,
                "Floating-point division (FDIV)"
            ),
            'fp_sqrt': InstructionCategory(
                'fp_sqrt', 45.0, 0,
                "Floating-point square root (SQRT)"
            ),
            'fixed_point': InstructionCategory(
                'fixed_point', 8.0, 0,
                "16/32-bit fixed-point operations (ADD, SUB, MUL, DIV)"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # Typical workload: 0.19*16 + 0.26*24 + 0.24*32 + 0.15*45 + 0.16*8 = 25.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_add': 0.19,
                'fp_mul': 0.26,
                'fp_div': 0.24,
                'fp_sqrt': 0.15,
                'fixed_point': 0.16,
            }, "Typical math coprocessor workload"),
            'scientific': WorkloadProfile('scientific', {
                'fp_add': 0.20,
                'fp_mul': 0.25,
                'fp_div': 0.25,
                'fp_sqrt': 0.20,
                'fixed_point': 0.10,
            }, "Scientific computing with heavy sqrt/div"),
            'graphics': WorkloadProfile('graphics', {
                'fp_add': 0.30,
                'fp_mul': 0.40,
                'fp_div': 0.10,
                'fp_sqrt': 0.05,
                'fixed_point': 0.15,
            }, "Graphics workload (transforms, projections)"),
            'fixed_heavy': WorkloadProfile('fixed_heavy', {
                'fp_add': 0.10,
                'fp_mul': 0.15,
                'fp_div': 0.10,
                'fp_sqrt': 0.05,
                'fixed_point': 0.60,
            }, "Fixed-point heavy workload"),
            'mixed': WorkloadProfile('mixed', {
                'fp_add': 0.22,
                'fp_mul': 0.28,
                'fp_div': 0.18,
                'fp_sqrt': 0.12,
                'fixed_point': 0.20,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'fixed_point': 5.000000,
            'fp_add': 8.000000,
            'fp_div': -16.000000,
            'fp_mul': 12.000000,
            'fp_sqrt': -10.563218
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

        # Apply correction terms (system identification)
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
        """
        Validate the model against expected CPI target.

        Returns validation results including:
        - Expected vs predicted CPI
        - Error percentage
        - Pass/fail status (passes if error < 5%)
        """
        expected_cpi = 25.0
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
            ("fp_add", 16.0),
            ("fp_mul", 24.0),
            ("fp_div", 32.0),
            ("fp_sqrt", 45.0),
            ("fixed_point", 8.0),
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
    model = Am9511Model()
    return model.validate()


if __name__ == "__main__":
    model = Am9511Model()
    print(f"AMD Am9511 Arithmetic Processing Unit Model")
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
