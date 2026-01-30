#!/usr/bin/env python3
"""
MMI 67110 Grey-Box Queueing Model
====================================

Target CPI: 1.8
Architecture: 4-bit Enhanced Bit-Slice Sequencer (1978)

The MMI 67110 was an enhanced microprogram sequencer from Monolithic
Memories Inc., designed to work with bit-slice ALUs to create custom
processors. It provided advanced sequencing capabilities including
subroutine calls, conditional branching, and loop counting.

Key characteristics:
- 4-bit address width
- 10 MHz clock
- ~3,000 transistors
- Bipolar Schottky technology
- Microprogram sequencer (not a CPU)
- Companion to bit-slice ALUs (Am2901, etc.)
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)


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


class Mmi67110Model(BaseProcessorModel):
    """
    MMI 67110 Grey-Box Queueing Model

    Target CPI: 1.8
    Calibration: Enhanced bit-slice sequencer

    The 67110 provided sequencing, branching, subroutine support,
    and loop counting for microprogram-controlled bit-slice systems.
    Simple operations were single-cycle while subroutines required
    additional cycles for stack operations.
    """

    name = "MMI 67110"
    manufacturer = "Monolithic Memories Inc."
    year = 1978
    clock_mhz = 10.0
    data_width = 4
    address_width = 12

    def __init__(self):
        # Typical: 0.20*1 + 0.25*2 + 0.15*3 + 0.25*2 + 0.15*1 = 1.80
        self.instruction_categories = {
            'sequence': InstructionCategory(
                'sequence', 1.0, 0,
                "Sequential address generation (next address)"
            ),
            'branch': InstructionCategory(
                'branch', 2.0, 0,
                "Conditional/unconditional branch"
            ),
            'subroutine': InstructionCategory(
                'subroutine', 3.0, 0,
                "Subroutine call/return (stack operations)"
            ),
            'control': InstructionCategory(
                'control', 2.0, 0,
                "Control register and mode operations"
            ),
            'counter': InstructionCategory(
                'counter', 1.0, 0,
                "Loop counter operations"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'sequence': 0.20,
                'branch': 0.25,
                'subroutine': 0.15,
                'control': 0.25,
                'counter': 0.15,
            }, "Typical microprogram sequencing workload"),
            'compute': WorkloadProfile('compute', {
                'sequence': 0.35,
                'branch': 0.20,
                'subroutine': 0.10,
                'control': 0.15,
                'counter': 0.20,
            }, "Compute-intensive sequencing"),
            'control': WorkloadProfile('control', {
                'sequence': 0.10,
                'branch': 0.35,
                'subroutine': 0.20,
                'control': 0.25,
                'counter': 0.10,
            }, "Control-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'sequence': 0.15,
                'branch': 0.15,
                'subroutine': 0.30,
                'control': 0.25,
                'counter': 0.15,
            }, "Subroutine-heavy workload"),
            'mixed': WorkloadProfile('mixed', {
                'sequence': 0.20,
                'branch': 0.20,
                'subroutine': 0.20,
                'control': 0.20,
                'counter': 0.20,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'branch': -0.704046,
            'control': -0.105205,
            'counter': -0.519064,
            'sequence': 1.493636,
            'subroutine': -0.123699
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
        """Validate the model against expected CPI target."""
        target_cpi = 1.8
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
            'description': 'CPI for typical sequencer workload'
        })
        if test_passed:
            passed += 1

        expected_cycles = {
            'sequence': 1.0, 'branch': 2.0, 'subroutine': 3.0,
            'control': 2.0, 'counter': 1.0,
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


def create_model() -> Mmi67110Model:
    return Mmi67110Model()


if __name__ == '__main__':
    model = Mmi67110Model()
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
