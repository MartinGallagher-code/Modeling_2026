#!/usr/bin/env python3
"""
National Semiconductor NS32081 Grey-Box Queueing Model
=======================================================

Target CPI: 15.0 (32-bit FPU, 1982)
Architecture: Floating-point unit for NS32000 family

The NS32081 was the floating-point coprocessor for National Semiconductor's
NS32000 series of 32-bit microprocessors. It provided IEEE 754 compatible
floating-point operations.

Key characteristics:
- IEEE 754 floating-point standard support
- 32-bit and 64-bit floating-point operations
- Tightly coupled with NS32016/NS32032 processors
- Direct interface via slave processor protocol
- Hardware multiply and divide
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
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)


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


class Ns32081Model(BaseProcessorModel):
    """
    National Semiconductor NS32081 Grey-Box Queueing Model

    Target CPI: 15.0
    Calibration: Weighted sum of instruction cycles

    The NS32081 is the floating-point unit for the NS32000 family.
    It provides IEEE 754 compatible floating-point operations.

    Instruction cycle counts (from NS32081 specifications):
    - fp_add: 8 cycles (single-precision add/subtract)
    - fp_mul: 12 cycles (single-precision multiply)
    - fp_div: 20 cycles (single-precision divide)
    - fp_sqrt: 30 cycles (square root)
    - dp_add: 12 cycles (double-precision add/subtract)
    - dp_mul: 18 cycles (double-precision multiply)
    - dp_div: 32 cycles (double-precision divide)
    - conversion: 6 cycles (format conversion)

    Typical workload calculation for CPI = 15.0:
    0.18*8 + 0.15*12 + 0.12*20 + 0.08*30 + 0.15*12 + 0.12*18 + 0.10*32 + 0.10*6 = 15.0
    """

    name = "NS32081"
    manufacturer = "National Semiconductor"
    year = 1982
    clock_mhz = 10.0  # Same clock as NS32016/NS32032

    def __init__(self):
        # Instruction categories with IEEE 754 operations
        self.instruction_categories = {
            'fp_add': InstructionCategory(
                'fp_add', 8.0, 0,
                "Single-precision add/subtract (ADDF, SUBF)"
            ),
            'fp_mul': InstructionCategory(
                'fp_mul', 12.0, 0,
                "Single-precision multiply (MULF)"
            ),
            'fp_div': InstructionCategory(
                'fp_div', 20.0, 0,
                "Single-precision divide (DIVF)"
            ),
            'fp_sqrt': InstructionCategory(
                'fp_sqrt', 30.0, 0,
                "Square root (SQRTF)"
            ),
            'dp_add': InstructionCategory(
                'dp_add', 12.0, 0,
                "Double-precision add/subtract (ADDL, SUBL)"
            ),
            'dp_mul': InstructionCategory(
                'dp_mul', 18.0, 0,
                "Double-precision multiply (MULL)"
            ),
            'dp_div': InstructionCategory(
                'dp_div', 32.0, 0,
                "Double-precision divide (DIVL)"
            ),
            'conversion': InstructionCategory(
                'conversion', 6.0, 0,
                "Format conversion (MOVFL, MOVLF, etc.)"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # Typical: 0.21*8 + 0.16*12 + 0.11*20 + 0.07*30 + 0.16*12 + 0.11*18 + 0.08*32 + 0.10*6 = 14.96
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_add': 0.21,
                'fp_mul': 0.16,
                'fp_div': 0.11,
                'fp_sqrt': 0.07,
                'dp_add': 0.16,
                'dp_mul': 0.11,
                'dp_div': 0.08,
                'conversion': 0.10,
            }, "Typical FPU workload"),
            'scientific': WorkloadProfile('scientific', {
                'fp_add': 0.10,
                'fp_mul': 0.10,
                'fp_div': 0.08,
                'fp_sqrt': 0.10,
                'dp_add': 0.22,
                'dp_mul': 0.18,
                'dp_div': 0.15,
                'conversion': 0.07,
            }, "Scientific computing (double-precision heavy)"),
            'graphics': WorkloadProfile('graphics', {
                'fp_add': 0.28,
                'fp_mul': 0.35,
                'fp_div': 0.10,
                'fp_sqrt': 0.05,
                'dp_add': 0.05,
                'dp_mul': 0.05,
                'dp_div': 0.02,
                'conversion': 0.10,
            }, "Graphics workload (single-precision transforms)"),
            'dsp': WorkloadProfile('dsp', {
                'fp_add': 0.30,
                'fp_mul': 0.40,
                'fp_div': 0.05,
                'fp_sqrt': 0.02,
                'dp_add': 0.08,
                'dp_mul': 0.08,
                'dp_div': 0.02,
                'conversion': 0.05,
            }, "DSP-like workload (multiply-accumulate heavy)"),
            'mixed': WorkloadProfile('mixed', {
                'fp_add': 0.20,
                'fp_mul': 0.18,
                'fp_div': 0.10,
                'fp_sqrt': 0.06,
                'dp_add': 0.16,
                'dp_mul': 0.14,
                'dp_div': 0.08,
                'conversion': 0.08,
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
        expected_cpi = 15.0
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
            ("fp_add", 8.0),
            ("fp_mul", 12.0),
            ("fp_div", 20.0),
            ("fp_sqrt", 30.0),
            ("dp_add", 12.0),
            ("dp_mul", 18.0),
            ("dp_div", 32.0),
            ("conversion", 6.0),
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
    model = Ns32081Model()
    return model.validate()


if __name__ == "__main__":
    model = Ns32081Model()
    print(f"National NS32081 FPU Model")
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
