#!/usr/bin/env python3
"""
Texas Instruments SN74S481 Grey-Box Queueing Model
====================================================

Target CPI: 1.0 (per micro-op)
Architecture: 4-bit slice ALU (1976)

The TI SN74S481 was Texas Instruments' bit-slice ALU offering.
It provides a 4-bit arithmetic logic unit with look-ahead carry
capability for high-speed operation.

Key characteristics:
- 4-bit slice ALU
- Schottky TTL technology
- Single-cycle operations
- Look-ahead carry for cascading
- Compatible with 74S182 carry look-ahead generator
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


class Sn74s481Model(BaseProcessorModel):
    """
    Texas Instruments SN74S481 Grey-Box Queueing Model

    Target CPI: 1.0 (microinstruction level)
    Calibration: All ALU operations complete in single cycle

    The SN74S481 is a 4-bit slice ALU. Like other bit-slice
    processors, all operations complete in a single clock cycle.
    """

    name = "TI SN74S481"
    manufacturer = "Texas Instruments"
    year = 1976
    clock_mhz = 8.0  # Typical clock frequency (Schottky TTL)
    transistor_count = 180  # Approximate
    data_width = 4  # 4-bit slice
    address_width = 4

    def __init__(self):
        # Bit-slice: all operations are single-cycle
        self.instruction_categories = {
            'arithmetic': InstructionCategory(
                'arithmetic', 1.0, 0,
                "Arithmetic operations (ADD, SUB, INCR, DECR)"
            ),
            'logic': InstructionCategory(
                'logic', 1.0, 0,
                "Logic operations (AND, OR, XOR, NOT, NAND, NOR)"
            ),
            'compare': InstructionCategory(
                'compare', 1.0, 0,
                "Compare operations"
            ),
            'pass': InstructionCategory(
                'pass', 1.0, 0,
                "Pass through (A, B, zero, ones)"
            ),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'arithmetic': 0.45,
                'logic': 0.30,
                'compare': 0.10,
                'pass': 0.15,
            }, "Typical ALU workload"),
            'compute': WorkloadProfile('compute', {
                'arithmetic': 0.60,
                'logic': 0.25,
                'compare': 0.05,
                'pass': 0.10,
            }, "Compute-intensive workload"),
            'logic_heavy': WorkloadProfile('logic_heavy', {
                'arithmetic': 0.25,
                'logic': 0.55,
                'compare': 0.10,
                'pass': 0.10,
            }, "Logic-heavy workload"),
            'control': WorkloadProfile('control', {
                'arithmetic': 0.30,
                'logic': 0.25,
                'compare': 0.25,
                'pass': 0.20,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'arithmetic': 0.40,
                'logic': 0.35,
                'compare': 0.10,
                'pass': 0.15,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
        # System identification: apply correction terms
        base_cpi = total_cpi
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
            ("arithmetic", 1.0),
            ("logic", 1.0),
            ("compare", 1.0),
            ("pass", 1.0),
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
    model = Sn74s481Model()
    return model.validate()


if __name__ == "__main__":
    model = Sn74s481Model()
    print(f"TI SN74S481 Bit-Slice ALU Model")
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
