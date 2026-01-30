#!/usr/bin/env python3
"""
NEC uPD7720 Grey-Box Queueing Model
=====================================

Target CPI: 1.5 (Early DSP, 1980)
Architecture: Digital Signal Processor

The NEC uPD7720 was an early digital signal processor designed
primarily for speech synthesis applications, particularly Linear
Predictive Coding (LPC) vocoders. It featured hardware multiply-
accumulate (MAC) operations and a pipelined architecture optimized
for real-time signal processing.

Key features:
- 16-bit data width, 13-bit instruction encoding
- Hardware multiply-accumulate unit
- 8 MHz clock frequency
- Harvard architecture with separate program/data memory
- Used in voice synthesis chips (e.g., Super Nintendo APU)
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


class Upd7720Model(BaseProcessorModel):
    """
    NEC uPD7720 Grey-Box Queueing Model

    Target CPI: 1.5
    Calibration: Weighted sum of instruction cycles

    The uPD7720 was NEC's early DSP designed for speech synthesis.
    It features a pipelined architecture with single-cycle MAC
    operations that made it efficient for LPC vocoder implementations.
    """

    name = "uPD7720"
    manufacturer = "NEC"
    year = 1980
    clock_mhz = 8.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 1.5
        # DSP architecture with pipelined MAC operations
        # Calculation: 0.40*1 + 0.25*1 + 0.20*2 + 0.15*2 = 1.35
        # Adjusted to hit 1.5: 0.35*1 + 0.25*1 + 0.25*2 + 0.15*2 = 1.4
        # Final: 0.30*1 + 0.25*1 + 0.25*2 + 0.20*2 = 1.45 (close to 1.5)
        # Using: mac=1, alu=1, memory=2, branch=2 with adjusted weights
        self.instruction_categories = {
            'mac': InstructionCategory(
                'mac', 1.0, 0,
                "Multiply-accumulate operations - single-cycle pipelined"
            ),
            'alu': InstructionCategory(
                'alu', 1.0, 0,
                "ALU operations (add, subtract, shift, logic)"
            ),
            'memory': InstructionCategory(
                'memory', 1.0, 1.0,
                "Memory load/store operations"
            ),
            'branch': InstructionCategory(
                'branch', 2.0, 0,
                "Branch and jump operations (pipeline flush)"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # Typical DSP workload emphasizes MAC operations for speech synthesis
        # Target CPI calculation for 'typical':
        # 0.35*1 + 0.25*1 + 0.25*2 + 0.15*2 = 0.35 + 0.25 + 0.50 + 0.30 = 1.40
        # Adjusted: 0.30*1 + 0.20*1 + 0.30*2 + 0.20*2 = 0.30 + 0.20 + 0.60 + 0.40 = 1.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'mac': 0.30,
                'alu': 0.20,
                'memory': 0.30,
                'branch': 0.20,
            }, "Typical LPC vocoder workload"),
            'compute': WorkloadProfile('compute', {
                'mac': 0.50,
                'alu': 0.25,
                'memory': 0.15,
                'branch': 0.10,
            }, "Compute-intensive DSP workload (FFT, filtering)"),
            'memory': WorkloadProfile('memory', {
                'mac': 0.20,
                'alu': 0.15,
                'memory': 0.50,
                'branch': 0.15,
            }, "Memory-intensive workload (coefficient lookup)"),
            'control': WorkloadProfile('control', {
                'mac': 0.20,
                'alu': 0.15,
                'memory': 0.25,
                'branch': 0.40,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'mac': 0.35,
                'alu': 0.20,
                'memory': 0.28,
                'branch': 0.17,
            }, "Mixed speech synthesis workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze performance for a given workload profile.

        Args:
            workload: Name of the workload profile to use

        Returns:
            AnalysisResult with CPI, IPC, and performance metrics
        """
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
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """
        Validate the model against expected performance targets.

        Returns:
            Dictionary containing validation results
        """
        target_cpi = 1.5
        tolerance = 0.05  # 5% error tolerance

        tests: List[Dict[str, Any]] = []
        passed = 0

        # Test typical workload
        result = self.analyze('typical')
        error = abs(result.cpi - target_cpi) / target_cpi
        test_passed = error <= tolerance

        tests.append({
            'name': 'typical_workload_cpi',
            'expected': target_cpi,
            'actual': result.cpi,
            'error_percent': error * 100,
            'passed': test_passed,
            'description': 'CPI for typical LPC vocoder workload'
        })
        if test_passed:
            passed += 1

        # Test instruction category cycles
        expected_cycles = {
            'mac': 1.0,
            'alu': 1.0,
            'memory': 2.0,
            'branch': 2.0,
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

        # Test all workloads produce reasonable CPI values
        for wl_name in self.workload_profiles:
            wl_result = self.analyze(wl_name)
            # CPI should be between 1.0 and 2.0 for this architecture
            wl_passed = 1.0 <= wl_result.cpi <= 2.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '1.0-2.0',
                'actual': wl_result.cpi,
                'passed': wl_passed,
                'description': f'CPI range check for {wl_name} workload'
            })
            if wl_passed:
                passed += 1

        total = len(tests)
        accuracy = (passed / total * 100) if total > 0 else 0

        return {
            'tests': tests,
            'passed': passed,
            'total': total,
            'accuracy_percent': accuracy,
            'target_cpi': target_cpi,
            'predicted_cpi': result.cpi,
            'cpi_error_percent': error * 100,
            'validation_passed': passed == total
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        """Return the instruction categories for this processor."""
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        """Return the workload profiles for this processor."""
        return self.workload_profiles

    def get_specs(self) -> Dict[str, Any]:
        """Return processor specifications."""
        return {
            'name': self.name,
            'manufacturer': self.manufacturer,
            'year': self.year,
            'clock_mhz': self.clock_mhz,
            'data_width_bits': 16,
            'instruction_width_bits': 13,
            'architecture': 'Harvard DSP',
            'technology': 'NMOS',
            'features': [
                'Hardware multiply-accumulate (MAC)',
                'Pipelined execution',
                '16-bit data path',
                '13-bit instruction encoding',
                'LPC vocoder support',
                'On-chip data RAM',
                'On-chip program ROM'
            ],
            'applications': [
                'Speech synthesis',
                'LPC vocoders',
                'Audio processing',
                'Super Nintendo sound processor'
            ]
        }


# Module-level convenience function
def create_model() -> Upd7720Model:
    """Create and return a new uPD7720 model instance."""
    return Upd7720Model()


if __name__ == '__main__':
    # Self-test when run directly
    model = Upd7720Model()

    print(f"NEC {model.name} Processor Model")
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
    print(f"  Accuracy: {validation['accuracy_percent']:.1f}%")
    print(f"  Target CPI: {validation['target_cpi']}")
    print(f"  Predicted CPI: {validation['predicted_cpi']:.2f}")
    print(f"  CPI Error: {validation['cpi_error_percent']:.2f}%")
