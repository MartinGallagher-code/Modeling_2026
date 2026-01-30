#!/usr/bin/env python3
"""
Signetics 8X300 Grey-Box Queueing Model
=====================================

Target CPI: 1.0 (Bipolar Signal Processor, 1976)
Architecture: Bipolar High-Speed Processor

The Signetics 8X300 was a revolutionary bipolar processor introduced
in 1976, designed for high-speed I/O and signal processing applications.
Its bipolar technology enabled single-cycle instruction execution,
making it one of the fastest processors of its era.

Key features:
- 8-bit data width
- Bipolar (TTL/Schottky) technology for maximum speed
- Single-cycle instruction execution
- 250ns instruction cycle time at 4 MHz
- Used in high-speed I/O controllers and signal processing
- Harvard-like architecture with separate I/O bus
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
    pass


class Signetics8X300Model(BaseProcessorModel):
    """
    Signetics 8X300 Grey-Box Queueing Model

    Target CPI: 1.0
    Calibration: Single-cycle execution for all instructions

    The 8X300 was a groundbreaking bipolar processor that achieved
    single-cycle execution through its high-speed bipolar technology.
    Every instruction executes in exactly one clock cycle (250ns at 4 MHz).
    """

    name = "8X300"
    manufacturer = "Signetics"
    year = 1976
    clock_mhz = 4.0  # 250ns cycle time

    def __init__(self):
        # Calibrated cycles to achieve CPI = 1.0
        # All instructions execute in exactly 1 cycle due to bipolar technology
        # This is the key architectural feature of the 8X300
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 1.0, 0,
                "ALU operations - single cycle"
            ),
            'move': InstructionCategory(
                'move', 1.0, 0,
                "Move/transfer operations - single cycle"
            ),
            'io': InstructionCategory(
                'io', 1.0, 0,
                "I/O operations - single cycle via IV bus"
            ),
            'branch': InstructionCategory(
                'branch', 1.0, 0,
                "Branch operations - single cycle"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # All categories execute in 1 cycle, so CPI is always 1.0
        # Typical high-speed I/O controller workload
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'move': 0.35,
                'io': 0.25,
                'branch': 0.10,
            }, "Typical I/O controller workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.55,
                'move': 0.25,
                'io': 0.10,
                'branch': 0.10,
            }, "Compute-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.15,
                'move': 0.25,
                'io': 0.50,
                'branch': 0.10,
            }, "I/O-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'move': 0.30,
                'io': 0.20,
                'branch': 0.30,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.28,
                'move': 0.32,
                'io': 0.25,
                'branch': 0.15,
            }, "Mixed signal processing workload"),
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

        bottleneck = max(contributions, key=contributions.get)

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

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
        target_cpi = 1.0
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
            'description': 'CPI for typical I/O controller workload'
        })
        if test_passed:
            passed += 1

        # Test instruction category cycles - all should be 1.0
        expected_cycles = {
            'alu': 1.0,
            'move': 1.0,
            'io': 1.0,
            'branch': 1.0,
        }

        for cat_name, expected in expected_cycles.items():
            actual = self.instruction_categories[cat_name].total_cycles
            cat_passed = actual == expected
            tests.append({
                'name': f'{cat_name}_cycles',
                'expected': expected,
                'actual': actual,
                'passed': cat_passed,
                'description': f'Cycle count for {cat_name} instructions (should be 1)'
            })
            if cat_passed:
                passed += 1

        # Test all workloads produce CPI = 1.0 (since all instructions are 1 cycle)
        for wl_name in self.workload_profiles:
            wl_result = self.analyze(wl_name)
            # CPI should be exactly 1.0 for this architecture
            wl_passed = abs(wl_result.cpi - 1.0) < 0.001
            tests.append({
                'name': f'{wl_name}_cpi_exact',
                'expected': 1.0,
                'actual': wl_result.cpi,
                'passed': wl_passed,
                'description': f'CPI should be 1.0 for {wl_name} workload'
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
            'data_width_bits': 8,
            'instruction_width_bits': 16,
            'architecture': 'Bipolar High-Speed',
            'technology': 'Bipolar (Schottky TTL)',
            'cycle_time_ns': 250,
            'features': [
                'Single-cycle instruction execution',
                'Bipolar high-speed technology',
                '8-bit data path',
                '16-bit instruction word',
                'Separate I/O bus (IV bus)',
                'Fast-in/fast-out architecture',
                '8 general-purpose registers'
            ],
            'applications': [
                'High-speed I/O controllers',
                'Disk drive controllers',
                'Communication controllers',
                'Signal processing',
                'Industrial automation'
            ]
        }


# Module-level convenience function
def create_model() -> Signetics8X300Model:
    """Create and return a new 8X300 model instance."""
    return Signetics8X300Model()


if __name__ == '__main__':
    # Self-test when run directly
    model = Signetics8X300Model()

    print(f"Signetics {model.name} Processor Model")
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
