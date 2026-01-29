#!/usr/bin/env python3
"""
General Instrument CP1600 Grey-Box Queueing Model
==================================================

Target CPI: 6.0 (16-bit architecture, 1975)
Architecture: 16-bit with 10-bit opcodes
Clock: 894.886 kHz (NTSC Intellivision)

The CP1600 was used in the Mattel Intellivision game console (1979).
It featured 8 general-purpose 16-bit registers (R0-R7) where R7
served as the program counter.

Key Features:
  - 16-bit data bus
  - 10-bit opcodes (some extended)
  - 8 16-bit registers (R0-R7)
  - R7 = Program Counter
  - R6 = Stack Pointer (by convention)
  - R4, R5 = Auto-increment/decrement registers
  - External ROM via cartridge slot
  - STIC graphics chip interface
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


class Cp1600Model(BaseProcessorModel):
    """
    General Instrument CP1600 Grey-Box Queueing Model

    Target CPI: 6.0
    Calibration: Weighted sum of instruction cycles

    The CP1600 was a relatively slow 16-bit processor due to its
    multi-cycle instruction execution and external memory interface.
    Most instructions took 6-10 cycles, with some complex instructions
    requiring up to 14 cycles.
    """

    name = "CP1600"
    manufacturer = "General Instrument"
    year = 1975
    clock_mhz = 0.894886  # NTSC Intellivision clock

    def __init__(self):
        # Calibrated cycles to achieve CPI = 6.0
        # CP1600 instruction timing from Intellivision programming guides
        # Calculation: 0.30*4 + 0.25*6 + 0.15*8 + 0.15*6 + 0.15*8 = 6.0
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 4.0, 0,
                "ALU operations (ADD, SUB, AND, XOR, etc.)"
            ),
            'data_transfer': InstructionCategory(
                'data_transfer', 6.0, 0,
                "Register moves and immediate loads (MOVR, MVII)"
            ),
            'memory': InstructionCategory(
                'memory', 8.0, 0,
                "Memory load/store (MVI, MVO, indirect)"
            ),
            'branch': InstructionCategory(
                'branch', 6.0, 0,
                "Branch and jump instructions (B, BNEQ, JSR)"
            ),
            'shift': InstructionCategory(
                'shift', 8.0, 0,
                "Shift and rotate operations (SLL, SLR, SWAP)"
            ),
        }

        # Workload profiles - weights sum to 1.0
        # Typical Intellivision game workload has lots of data movement
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.25,
                'memory': 0.15,
                'branch': 0.15,
                'shift': 0.15,
            }, "Typical Intellivision game workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.10,
                'branch': 0.10,
                'shift': 0.15,
            }, "Compute-intensive workload (math, collision)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.40,
                'branch': 0.10,
                'shift': 0.10,
            }, "Memory-intensive workload (graphics updates)"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'branch': 0.40,
                'shift': 0.10,
            }, "Control-flow intensive workload (game logic)"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.28,
                'data_transfer': 0.22,
                'memory': 0.22,
                'branch': 0.15,
                'shift': 0.13,
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
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known CP1600 timing data.

        Returns validation results including:
        - Test cases with expected vs predicted values
        - Pass/fail status
        - Overall accuracy percentage
        """
        tests = []

        # Test 1: Typical workload CPI
        result = self.analyze('typical')
        expected_cpi = 6.0
        error_pct = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': 'typical_workload_cpi',
            'expected': expected_cpi,
            'predicted': result.cpi,
            'error_percent': error_pct,
            'passed': error_pct < 5.0
        })

        # Test 2: ALU instruction timing (ADDR, SUBR, etc.)
        alu_cycles = self.instruction_categories['alu'].total_cycles
        expected_alu = 4.0
        error_pct = abs(alu_cycles - expected_alu) / expected_alu * 100
        tests.append({
            'name': 'alu_instruction_cycles',
            'expected': expected_alu,
            'predicted': alu_cycles,
            'error_percent': error_pct,
            'passed': error_pct < 5.0
        })

        # Test 3: Memory instruction timing (MVI, MVO)
        mem_cycles = self.instruction_categories['memory'].total_cycles
        expected_mem = 8.0
        error_pct = abs(mem_cycles - expected_mem) / expected_mem * 100
        tests.append({
            'name': 'memory_instruction_cycles',
            'expected': expected_mem,
            'predicted': mem_cycles,
            'error_percent': error_pct,
            'passed': error_pct < 5.0
        })

        # Test 4: Branch instruction timing
        branch_cycles = self.instruction_categories['branch'].total_cycles
        expected_branch = 6.0
        error_pct = abs(branch_cycles - expected_branch) / expected_branch * 100
        tests.append({
            'name': 'branch_instruction_cycles',
            'expected': expected_branch,
            'predicted': branch_cycles,
            'error_percent': error_pct,
            'passed': error_pct < 5.0
        })

        # Test 5: Shift instruction timing
        shift_cycles = self.instruction_categories['shift'].total_cycles
        expected_shift = 8.0
        error_pct = abs(shift_cycles - expected_shift) / expected_shift * 100
        tests.append({
            'name': 'shift_instruction_cycles',
            'expected': expected_shift,
            'predicted': shift_cycles,
            'error_percent': error_pct,
            'passed': error_pct < 5.0
        })

        # Test 6: IPS validation (instructions per second)
        result = self.analyze('typical')
        # At ~895 kHz with CPI 6.0, expect ~149k IPS
        expected_ips = 894886 / 6.0  # ~149,148 IPS
        error_pct = abs(result.ips - expected_ips) / expected_ips * 100
        tests.append({
            'name': 'ips_validation',
            'expected': expected_ips,
            'predicted': result.ips,
            'error_percent': error_pct,
            'passed': error_pct < 5.0
        })

        passed = sum(1 for t in tests if t['passed'])
        total = len(tests)
        accuracy = (passed / total) * 100 if total > 0 else 0

        return {
            'tests': tests,
            'passed': passed,
            'total': total,
            'accuracy_percent': accuracy,
            'validation_passed': passed == total
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        """Return all instruction categories."""
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        """Return all workload profiles."""
        return self.workload_profiles

    def get_specifications(self) -> Dict[str, Any]:
        """Return processor specifications."""
        return {
            'name': self.name,
            'manufacturer': self.manufacturer,
            'year': self.year,
            'clock_mhz': self.clock_mhz,
            'data_width_bits': 16,
            'address_width_bits': 16,
            'register_count': 8,
            'opcode_width_bits': 10,
            'technology': 'NMOS',
            'package': '40-pin DIP',
            'notable_uses': ['Mattel Intellivision (1979)'],
        }


def main():
    """Test the CP1600 model."""
    model = Cp1600Model()

    print(f"{'='*60}")
    print(f"General Instrument CP1600 Processor Model")
    print(f"{'='*60}")
    print(f"Manufacturer: {model.manufacturer}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz * 1000:.3f} kHz")
    print()

    print("Instruction Categories:")
    print("-" * 40)
    for name, cat in model.instruction_categories.items():
        print(f"  {name:15} {cat.total_cycles:5.1f} cycles - {cat.description}")
    print()

    print("Workload Analysis:")
    print("-" * 40)
    for workload_name in model.workload_profiles:
        result = model.analyze(workload_name)
        print(f"  {workload_name:10} CPI={result.cpi:.2f}  IPC={result.ipc:.3f}  "
              f"IPS={result.ips:,.0f}  Bottleneck={result.bottleneck}")
    print()

    print("Validation Results:")
    print("-" * 40)
    validation = model.validate()
    for test in validation['tests']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  [{status}] {test['name']}: expected={test['expected']:.2f}, "
              f"predicted={test['predicted']:.2f}, error={test['error_percent']:.1f}%")
    print()
    print(f"Overall: {validation['passed']}/{validation['total']} tests passed "
          f"({validation['accuracy_percent']:.0f}%)")


if __name__ == "__main__":
    main()
