#!/usr/bin/env python3
"""
WISC CPU/16 Grey-Box Queueing Model
=====================================

Architecture: 16-bit Writable Instruction Set Computer (1986)
Queueing Model: Sequential execution, stack-based

Features:
  - Writable Instruction Set Computer (WISC)
  - TTL discrete logic construction
  - 16-bit data path, 4 MHz clock
  - Fully RAM-based microcode (writable control store)
  - Stack-oriented architecture
  - User can redefine instruction set at runtime
  - Phil Koopman's research architecture

Calibrated: 2026-01-29
Target CPI: ~2.5 (stack ops are fast on stack machines)
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    from dataclasses import dataclass

    @dataclass
    class InstructionCategory:
        name: str
        base_cycles: float
        memory_cycles: float = 0
        description: str = ""
        @property
        def total_cycles(self): return self.base_cycles + self.memory_cycles

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi,
                       correction_delta=correction_delta)

    class BaseProcessorModel:
        pass


class WISC16Model(BaseProcessorModel):
    """
    WISC CPU/16 Grey-Box Queueing Model

    Architecture: 16-bit Writable Instruction Set Computer (1986)
    - Stack-oriented architecture
    - TTL discrete logic (board-level implementation)
    - RAM-based writable microcode store
    - User-definable instruction set
    - CPI ~2.5 (stack ops inherently efficient)

    Research machine by Phil Koopman exploring writable
    instruction sets and stack machine architectures.
    """

    name = "WISC CPU/16"
    manufacturer = "Phil Koopman (Carnegie Mellon)"
    year = 1986
    clock_mhz = 4.0
    transistor_count = 0  # TTL discrete, not monolithic
    data_width = 16
    address_width = 16

    def __init__(self):
        # WISC CPU/16 instruction timing
        # Stack machines have efficient stack operations
        # Microcode execution from RAM adds slight overhead
        #
        # Operations:
        #   Stack ops (push, pop, dup, swap): ~2 cycles
        #   ALU (add, sub, and, or): ~2 cycles
        #   Memory (load, store): ~3 cycles
        #   Control (branch, call, return): ~3 cycles
        #   Microcode (custom microcode execution): ~2.5 cycles

        self.instruction_categories = {
            'stack_ops': InstructionCategory('stack_ops', 2.0, 0,
                "Stack operations: push/pop/dup/swap @2 cycles"),
            'alu': InstructionCategory('alu', 2.0, 0,
                "ALU operations: add/sub/and/or @2 cycles"),
            'memory': InstructionCategory('memory', 3.0, 0,
                "Memory load/store @3 cycles"),
            'control': InstructionCategory('control', 3.0, 0,
                "Branch/call/return @3 cycles"),
            'microcode': InstructionCategory('microcode', 2.5, 0,
                "Custom microcode instruction execution @2.5 cycles"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_ops': 0.30,
                'alu': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'microcode': 0.10,
            }, "Typical Forth-like stack machine workload"),
            'compute': WorkloadProfile('compute', {
                'stack_ops': 0.25,
                'alu': 0.40,
                'memory': 0.15,
                'control': 0.10,
                'microcode': 0.10,
            }, "Compute-intensive (arithmetic)"),
            'stack_heavy': WorkloadProfile('stack_heavy', {
                'stack_ops': 0.45,
                'alu': 0.15,
                'memory': 0.15,
                'control': 0.15,
                'microcode': 0.10,
            }, "Stack-intensive (deep nesting, shuffling)"),
            'custom_isa': WorkloadProfile('custom_isa', {
                'stack_ops': 0.20,
                'alu': 0.15,
                'memory': 0.15,
                'control': 0.10,
                'microcode': 0.40,
            }, "Heavy use of custom microcode instructions"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.314697,
            'control': 0.516934,
            'memory': 0.433836,
            'microcode': -0.823861,
            'stack_ops': 0.665984
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential stack machine execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        ipc = 1.0 / corrected_cpi
        ips = self.clock_mhz * 1e6 * ipc

        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
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
        """Run validation tests against known WISC CPU/16 characteristics"""
        tests = []

        result = self.analyze('typical')
        expected_cpi = 2.5
        cpi_error = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': 'CPI accuracy',
            'passed': cpi_error < 5.0,
            'expected': f'{expected_cpi} +/- 5%',
            'actual': f'{result.cpi:.2f} ({cpi_error:.1f}% error)'
        })

        for profile_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            tests.append({
                'name': f'Weights sum ({profile_name})',
                'passed': 0.99 <= weight_sum <= 1.01,
                'expected': '1.0',
                'actual': f'{weight_sum:.2f}'
            })

        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 1.0 <= cycles <= 10.0,
                'expected': '1-10 cycles',
                'actual': f'{cycles:.1f}'
            })

        tests.append({
            'name': 'IPC range',
            'passed': 0.2 <= result.ipc <= 0.8,
            'expected': '0.2-0.8',
            'actual': f'{result.ipc:.3f}'
        })

        for workload in self.workload_profiles.keys():
            try:
                r = self.analyze(workload)
                valid = r.cpi > 0 and r.ipc > 0 and r.ips > 0
                tests.append({
                    'name': f'Workload analysis ({workload})',
                    'passed': valid,
                    'expected': 'Valid CPI/IPC/IPS',
                    'actual': f'CPI={r.cpi:.2f}' if valid else 'Invalid'
                })
            except Exception as e:
                tests.append({
                    'name': f'Workload analysis ({workload})',
                    'passed': False,
                    'expected': 'No error',
                    'actual': str(e)
                })

        tests.append({
            'name': 'Clock speed',
            'passed': abs(self.clock_mhz - 4.0) < 0.1,
            'expected': '4.0 MHz',
            'actual': f'{self.clock_mhz} MHz'
        })

        passed = sum(1 for t in tests if t['passed'])
        return {
            'tests': tests,
            'passed': passed,
            'total': len(tests),
            'accuracy_percent': 100.0 - cpi_error
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles


if __name__ == '__main__':
    model = WISC16Model()

    print(f"=== {model.name} Performance Model ===")
    print(f"Manufacturer: {model.manufacturer}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print()

    for workload in model.workload_profiles:
        result = model.analyze(workload)
        print(f"{workload:16} - CPI: {result.cpi:.2f}, IPC: {result.ipc:.3f}, "
              f"IPS: {result.ips/1e6:.3f}M, Bottleneck: {result.bottleneck}")

    print()

    validation = model.validate()
    print(f"=== Validation Results ===")
    print(f"Passed: {validation['passed']}/{validation['total']}")
    print(f"Accuracy: {validation['accuracy_percent']:.1f}%")
    print()

    for test in validation['tests']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  [{status}] {test['name']}: {test['actual']} (expected: {test['expected']})")
