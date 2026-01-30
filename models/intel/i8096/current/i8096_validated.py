#!/usr/bin/env python3
"""
Intel 8096 Grey-Box Queueing Model
==================================

Architecture: 16-bit Microcontroller (1982)
Dominated automotive applications from 1985-2005.

Features:
  - 16-bit register-based architecture (not accumulator)
  - 232-byte register file with 8 dedicated registers
  - Hardware multiply (16x16->32) and divide (32/16->16)
  - On-chip PWM, A/D converter, high-speed I/O
  - Serial port, timers, watchdog

Target CPI: 4.0 (16-bit MCU register operations)
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class InstructionCategory:
    name: str
    base_cycles: float
    memory_cycles: float = 0
    description: str = ""

    @property
    def total_cycles(self) -> float:
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
    def from_cpi(cls, processor: str, workload: str, cpi: float, clock_mhz: float,
                 bottleneck: str, utilizations: Dict[str, float],
                 base_cpi: float = None, correction_delta: float = 0.0) -> 'AnalysisResult':
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)


class I8096Model:
    """
    Intel 8096 Grey-Box Queueing Model

    16-bit microcontroller (1982) that dominated automotive
    - Register file architecture (not accumulator based)
    - 232 bytes register file, addresses 00h-E7h
    - 8 dedicated registers (R0-R14, word aligned)
    - Hardware multiply/divide for automotive calculations
    - On-chip PWM for motor control, A/D for sensors

    Clock: 8-12 MHz (typically 12 MHz)
    State times: Each state = 3 clock cycles
    Most instructions: 2-6 state times (6-18 clocks)
    """

    name = "Intel 8096"
    manufacturer = "Intel"
    year = 1982
    clock_mhz = 12.0  # Typical automotive clock
    transistor_count = 120000  # CHMOS version
    data_width = 16
    address_width = 16

    def __init__(self):
        # Intel 8096 timing: 1 state time = 3 clock cycles
        # Most register operations: 2-4 state times (6-12 clocks)
        # Memory operations: 3-6 state times (9-18 clocks)
        # Multiply: 6 state times (18 clocks) - 16x16->32
        # Divide: 12 state times (36 clocks) - 32/16->16
        # Peripheral access: 2-4 state times (6-12 clocks)

        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 2.9, 0,
                "ADD/SUB/AND/OR/XOR reg,reg @2-3 clocks (1 state time effective)"
            ),
            'memory': InstructionCategory(
                'memory', 4.5, 0,
                "LD/ST indirect @4-5 clocks average"
            ),
            'multiply': InstructionCategory(
                'multiply', 6.0, 0,
                "MUL 16x16->32 @6 clocks (hardware multiplier)"
            ),
            'divide': InstructionCategory(
                'divide', 12.0, 0,
                "DIV 32/16->16 @12 clocks (hardware divider)"
            ),
            'branch': InstructionCategory(
                'branch', 4.0, 0,
                "JMP/CALL/RET @4 clocks average (short jumps faster)"
            ),
            'peripheral': InstructionCategory(
                'peripheral', 4.0, 0,
                "PWM/ADC/Timer access @4 clocks (SFR access)"
            ),
        }

        # Workload profiles for automotive MCU applications
        self.workload_profiles = {
            'typical': WorkloadProfile(
                'typical',
                {
                    'alu': 0.35,
                    'memory': 0.25,
                    'multiply': 0.05,
                    'divide': 0.02,
                    'branch': 0.18,
                    'peripheral': 0.15,
                },
                "Typical automotive control loop"
            ),
            'compute': WorkloadProfile(
                'compute',
                {
                    'alu': 0.45,
                    'memory': 0.20,
                    'multiply': 0.10,
                    'divide': 0.05,
                    'branch': 0.12,
                    'peripheral': 0.08,
                },
                "Compute-intensive (engine calculations)"
            ),
            'memory': WorkloadProfile(
                'memory',
                {
                    'alu': 0.25,
                    'memory': 0.40,
                    'multiply': 0.03,
                    'divide': 0.02,
                    'branch': 0.15,
                    'peripheral': 0.15,
                },
                "Memory-intensive (data logging)"
            ),
            'control': WorkloadProfile(
                'control',
                {
                    'alu': 0.30,
                    'memory': 0.20,
                    'multiply': 0.03,
                    'divide': 0.02,
                    'branch': 0.30,
                    'peripheral': 0.15,
                },
                "Control-intensive (state machines)"
            ),
            'mixed': WorkloadProfile(
                'mixed',
                {
                    'alu': 0.32,
                    'memory': 0.28,
                    'multiply': 0.05,
                    'divide': 0.03,
                    'branch': 0.17,
                    'peripheral': 0.15,
                },
                "Mixed automotive workload"
            ),
            'fuel_injection': WorkloadProfile(
                'fuel_injection',
                {
                    'alu': 0.30,
                    'memory': 0.20,
                    'multiply': 0.12,
                    'divide': 0.08,
                    'branch': 0.15,
                    'peripheral': 0.15,
                },
                "Fuel injection calculations (heavy math)"
            ),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 1.008645,
            'branch': -1.050855,
            'divide': -6.000000,
            'memory': 0.809417,
            'multiply': -4.999985,
            'peripheral': 0.005701
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze processor performance for given workload.

        Args:
            workload: Name of workload profile to use

        Returns:
            AnalysisResult with CPI, IPC, IPS and utilization data
        """
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0.0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

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
            bottleneck="register_file",
            utilizations={cat: profile.category_weights[cat]
                          for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )

    def get_instruction_timing(self, instruction: str) -> Optional[float]:
        """
        Get cycle timing for a specific instruction.

        Args:
            instruction: Instruction mnemonic (e.g., 'ADD', 'MUL', 'LD')

        Returns:
            Cycle count or None if instruction not found
        """
        # Instruction to category mapping
        timing_map = {
            # ALU operations (register-to-register)
            'ADD': 3, 'ADDC': 3, 'SUB': 3, 'SUBC': 3,
            'AND': 3, 'OR': 3, 'XOR': 3, 'NOT': 3,
            'INC': 2, 'DEC': 2, 'NEG': 3, 'CLR': 2,
            'SHL': 3, 'SHR': 3, 'SHRA': 3,
            'CMP': 3, 'CMPL': 3,
            # Memory operations
            'LD': 4, 'LDB': 4, 'ST': 5, 'STB': 5,
            'PUSH': 5, 'POP': 5,
            # Multiply/Divide (hardware)
            'MUL': 6, 'MULU': 6,
            'DIV': 12, 'DIVU': 12,
            # Branch/Control
            'SJMP': 3, 'LJMP': 4, 'BR': 4,
            'SCALL': 5, 'LCALL': 6, 'RET': 5,
            'JC': 4, 'JNC': 4, 'JE': 4, 'JNE': 4,
            'JGT': 4, 'JLE': 4, 'JGE': 4, 'JLT': 4,
            # Peripheral/Special
            'NOP': 2, 'DI': 2, 'EI': 2,
            'TRAP': 8, 'RST': 8,
        }
        return timing_map.get(instruction.upper())

    def validate(self) -> Dict[str, Any]:
        """
        Validate the model against target specifications.

        Returns:
            Dictionary with validation results including pass/fail status
        """
        target_cpi = 4.0
        result = self.analyze('typical')

        cpi_error = abs(result.cpi - target_cpi) / target_cpi * 100

        validation_result = {
            'processor': self.name,
            'target_cpi': target_cpi,
            'actual_cpi': result.cpi,
            'cpi_error_percent': cpi_error,
            'validation_passed': cpi_error < 5.0,
            'ipc': result.ipc,
            'mips': result.ips / 1e6,
            'clock_mhz': self.clock_mhz,
            'workload_results': {}
        }

        # Test all workloads
        for workload_name in self.workload_profiles:
            wl_result = self.analyze(workload_name)
            validation_result['workload_results'][workload_name] = {
                'cpi': wl_result.cpi,
                'ipc': wl_result.ipc,
                'mips': wl_result.ips / 1e6
            }

        return validation_result


def validate() -> Dict[str, Any]:
    """
    Module-level validation function.

    Returns:
        Validation results dictionary
    """
    model = I8096Model()
    return model.validate()


def main():
    """Run model and display results."""
    model = I8096Model()

    print(f"{'=' * 60}")
    print(f"{model.name} Grey-Box Performance Model")
    print(f"{'=' * 60}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"Data Width: {model.data_width}-bit")
    print(f"Transistors: {model.transistor_count:,}")
    print()

    print("Instruction Categories:")
    print("-" * 40)
    for name, cat in model.instruction_categories.items():
        print(f"  {name:12s}: {cat.total_cycles:5.1f} cycles - {cat.description}")
    print()

    print("Workload Analysis:")
    print("-" * 60)
    for workload_name in model.workload_profiles:
        result = model.analyze(workload_name)
        print(f"  {workload_name:16s}: CPI={result.cpi:.2f}, "
              f"IPC={result.ipc:.3f}, MIPS={result.ips / 1e6:.2f}")
    print()

    print("Validation:")
    print("-" * 40)
    validation = model.validate()
    print(f"  Target CPI: {validation['target_cpi']:.1f}")
    print(f"  Actual CPI: {validation['actual_cpi']:.2f}")
    print(f"  Error: {validation['cpi_error_percent']:.2f}%")
    print(f"  Status: {'PASSED' if validation['validation_passed'] else 'FAILED'}")


if __name__ == '__main__':
    main()
