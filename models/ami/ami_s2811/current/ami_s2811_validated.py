#!/usr/bin/env python3
"""
AMI S2811 Grey-Box Queueing Model
=====================================

Target CPI: 8.0 (Early Signal Processor, 1978)
Architecture: Signal Processor

The AMI S2811 was an early signal processing chip introduced in 1978,
primarily designed for modem and telecommunications applications.
It featured specialized signal processing capabilities but with
relatively high cycles-per-instruction due to its microcoded
architecture and multi-cycle operations.

Key features:
- 12-bit data width
- Microcoded architecture
- Designed for modem applications
- Multi-cycle instruction execution
- Used in early modems and signal processing equipment
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


class AmiS2811Model(BaseProcessorModel):
    """
    AMI S2811 Grey-Box Queueing Model

    Target CPI: 8.0
    Calibration: Weighted sum of instruction cycles

    The S2811 was AMI's early signal processor designed for modem
    applications. Its microcoded architecture resulted in relatively
    high CPI compared to later DSPs, but it was effective for
    telecommunications signal processing of its era.
    """

    name = "S2811"
    manufacturer = "AMI"
    year = 1978
    clock_mhz = 4.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 8.0
        # Early signal processor with microcoded multi-cycle operations
        # Calculation: 0.30*6 + 0.25*8 + 0.25*10 + 0.20*8 = 1.8 + 2.0 + 2.5 + 1.6 = 7.9 ~ 8.0
        self.instruction_categories = {
            'multiply': InstructionCategory(
                'multiply', 6.0, 0,
                "Multiply operations - core signal processing"
            ),
            'alu': InstructionCategory(
                'alu', 8.0, 0,
                "ALU operations (add, subtract, logic)"
            ),
            'memory': InstructionCategory(
                'memory', 6.0, 4.0,
                "Memory load/store operations"
            ),
            'control': InstructionCategory(
                'control', 8.0, 0,
                "Control and branch operations"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # Typical modem/signal processing workload
        # Target CPI calculation for 'typical':
        # 0.30*6 + 0.25*8 + 0.25*10 + 0.20*8 = 1.8 + 2.0 + 2.5 + 1.6 = 7.9
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'multiply': 0.30,
                'alu': 0.25,
                'memory': 0.25,
                'control': 0.20,
            }, "Typical modem signal processing workload"),
            'compute': WorkloadProfile('compute', {
                'multiply': 0.45,
                'alu': 0.30,
                'memory': 0.15,
                'control': 0.10,
            }, "Compute-intensive signal processing"),
            'memory': WorkloadProfile('memory', {
                'multiply': 0.20,
                'alu': 0.20,
                'memory': 0.45,
                'control': 0.15,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'multiply': 0.20,
                'alu': 0.20,
                'memory': 0.20,
                'control': 0.40,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'multiply': 0.28,
                'alu': 0.27,
                'memory': 0.27,
                'control': 0.18,
            }, "Mixed signal processing workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze performance for a given workload profile.

        Args:
            workload: Name of the workload profile to use

        Returns:
            AnalysisResult with CPI, IPC, and performance metrics
        """
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
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        """
        Validate the model against expected performance targets.

        Returns:
            Dictionary containing validation results
        """
        target_cpi = 8.0
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
            'description': 'CPI for typical modem signal processing workload'
        })
        if test_passed:
            passed += 1

        # Test instruction category cycles
        expected_cycles = {
            'multiply': 6.0,
            'alu': 8.0,
            'memory': 10.0,
            'control': 8.0,
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
            # CPI should be between 6.0 and 10.0 for this architecture
            wl_passed = 6.0 <= wl_result.cpi <= 10.0
            tests.append({
                'name': f'{wl_name}_cpi_range',
                'expected': '6.0-10.0',
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
            'data_width_bits': 12,
            'architecture': 'Signal Processor',
            'technology': 'NMOS',
            'features': [
                'Microcoded architecture',
                'Hardware multiplier',
                '12-bit data path',
                'Signal processing instructions',
                'Modem support circuitry'
            ],
            'applications': [
                'Modem signal processing',
                'Telecommunications',
                'Filter implementations',
                'Early DSP applications'
            ]
        }


# Module-level convenience function
def create_model() -> AmiS2811Model:
    """Create and return a new S2811 model instance."""
    return AmiS2811Model()


if __name__ == '__main__':
    # Self-test when run directly
    model = AmiS2811Model()

    print(f"AMI {model.name} Processor Model")
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
