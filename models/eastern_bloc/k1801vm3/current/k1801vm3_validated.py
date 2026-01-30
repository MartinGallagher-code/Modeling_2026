#!/usr/bin/env python3
"""
K1801VM3 Grey-Box Queueing Model
====================================

Architecture: 16-bit microprocessor (1985)
Queueing Model: Pipelined execution, cycle-accurate

Features:
  - Final Soviet PDP-11 compatible microprocessor
  - 16-bit data bus
  - ~40,000 transistors
  - 10 MHz clock
  - Pipelined execution
  - PDP-11 instruction set with FP support
  - 2-8 cycles per instruction

Calibrated: 2026-01-29
Target CPI: ~3.2 for typical workloads
Used in: Advanced DVK systems, Elektronika-85
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


class K1801VM3Model(BaseProcessorModel):
    """
    K1801VM3 Grey-Box Queueing Model

    Architecture: 16-bit NMOS microprocessor (1985)
    - Final Soviet PDP-11 compatible
    - Pipelined execution for improved throughput
    - Floating point support
    - CPI ~3.2 for typical workloads
    """

    # Processor specifications
    name = "K1801VM3"
    manufacturer = "Soviet Union"
    year = 1985
    clock_mhz = 10.0
    transistor_count = 40000
    data_width = 16
    address_width = 16

    def __init__(self):
        # K1801VM3 instruction timing (pipelined PDP-11 compatible)
        #
        # Pipeline improvements over VM2:
        #   MOV Rn,Rn: 1 cycle
        #   ADD Rn,Rn: 2 cycles
        #   ADD Rn,(Rn): 3 cycles
        #   JMP: 2-3 cycles
        #   JSR: 4-5 cycles
        #   RTS: 3 cycles
        #   Memory indirect: 4-6 cycles
        #   FADD: 6-10 cycles

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0,
                "ALU ops - ADD Rn,Rn @2, INC @1, CMP @2, weighted ~2"),
            'data_transfer': InstructionCategory('data_transfer', 2.0, 0,
                "MOV Rn,Rn @1, MOV Rn,(Rn) @2, MOV Rn,imm @2, weighted ~2"),
            'memory': InstructionCategory('memory', 5.0, 0,
                "Memory indirect modes, deferred addressing ~5"),
            'control': InstructionCategory('control', 3.0, 0,
                "JMP @2-3, JSR @4-5, RTS @3, Bcc @2, weighted ~3"),
            'float': InstructionCategory('float', 8.0, 0,
                "FADD @6-10, FMUL @8-12, floating point ops ~8"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.10,
                'control': 0.30,
                'float': 0.10,
            }, "Typical K1801VM3 workload (advanced PDP-11 software)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.30,
                'data_transfer': 0.20,
                'memory': 0.10,
                'control': 0.15,
                'float': 0.25,
            }, "Compute-intensive with floating point"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'control': 0.20,
                'float': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.50,
                'float': 0.10,
            }, "Control-flow intensive"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using pipelined execution model"""
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
        expected_cpi = 3.2
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
