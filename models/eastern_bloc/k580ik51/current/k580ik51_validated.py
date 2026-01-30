#!/usr/bin/env python3
"""
K580IK51 Grey-Box Queueing Model
====================================

Architecture: 8-bit microcontroller (1980s)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Soviet 8051-compatible microcontroller
  - 8-bit data bus
  - ~12,000 transistors
  - 6 MHz clock (12 MHz oscillator / 2)
  - 8051 instruction set compatible
  - On-chip RAM, ROM, timers, serial port
  - Bit-addressable operations
  - 1-3 cycles per instruction (machine cycles)

Calibrated: 2026-01-29
Target CPI: ~2.0 for typical workloads
Used in: Soviet industrial control, embedded systems
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

        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)

    class BaseProcessorModel:
        pass


class K580IK51Model(BaseProcessorModel):
    """
    K580IK51 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microcontroller (1980s)
    - Soviet Intel 8051 clone
    - Sequential execution
    - On-chip peripherals (RAM, ROM, timers, serial)
    - Bit-addressable memory
    - CPI ~2.0 for typical workloads (machine cycles)
    """

    # Processor specifications
    name = "K580IK51"
    manufacturer = "Soviet Union"
    year = 1986
    clock_mhz = 6.0  # Machine cycle rate (12 MHz oscillator / 2)
    transistor_count = 12000
    data_width = 8
    address_width = 16

    def __init__(self):
        # K580IK51 instruction timing (8051 compatible)
        #
        # 8051 machine cycles (1 machine cycle = 12 oscillator clocks):
        #   ADD A,Rn: 1 machine cycle
        #   MOV A,Rn: 1 machine cycle
        #   MOV A,@Ri: 1 machine cycle
        #   MOV A,direct: 2 machine cycles
        #   MOVX A,@DPTR: 2 machine cycles
        #   LJMP: 2 machine cycles
        #   LCALL: 2 machine cycles
        #   RET: 2 machine cycles
        #   SETB bit: 1 machine cycle
        #   CLR bit: 1 machine cycle
        #   MUL AB: 4 machine cycles
        #   DIV AB: 4 machine cycles

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0,
                "ALU ops - ADD A,Rn @1, SUBB @1, INC @1, weighted ~1"),
            'data_transfer': InstructionCategory('data_transfer', 2.0, 0,
                "MOV A,Rn @1, MOV A,direct @2, MOV direct,direct @3, weighted ~2"),
            'memory': InstructionCategory('memory', 2.0, 0,
                "MOVX A,@DPTR @2, MOVC A,@A+DPTR @2, external memory ~2"),
            'control': InstructionCategory('control', 2.0, 0,
                "LJMP @2, LCALL @2, RET @2, SJMP @2, DJNZ @2, weighted ~2"),
            'bit_ops': InstructionCategory('bit_ops', 2.0, 0,
                "SETB @1, CLR @1, JB/JNB @2, JBC @2, weighted ~2"),
            'timer': InstructionCategory('timer', 3.0, 0,
                "Timer/serial config, MUL AB @4, DIV AB @4, peripheral access ~3"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.20,
                'bit_ops': 0.15,
                'timer': 0.15,
            }, "Typical K580IK51 workload (embedded control)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.35,
                'data_transfer': 0.25,
                'memory': 0.10,
                'control': 0.15,
                'bit_ops': 0.10,
                'timer': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.10,
                'data_transfer': 0.30,
                'memory': 0.30,
                'control': 0.15,
                'bit_ops': 0.05,
                'timer': 0.10,
            }, "Memory/data-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.10,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.30,
                'bit_ops': 0.20,
                'timer': 0.15,
            }, "Control and bit manipulation intensive"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
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
        """Run validation tests"""
        tests = []

        result = self.analyze('typical')
        expected_cpi = 2.0
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
                'passed': 0.5 <= cycles <= 200.0,
                'expected': '0.5-200 cycles',
                'actual': f'{cycles:.1f}'
            })

        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 1.5,
            'expected': '0.05-1.5',
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
