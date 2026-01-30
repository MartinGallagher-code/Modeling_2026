#!/usr/bin/env python3
"""
M68000 Grey-Box Queueing Model
===============================

Architecture: 16/32-bit microprocessor (1979)
Queueing Model: Microcoded execution, cycle-accurate

Features:
  - 32-bit internal, 16-bit external data bus
  - 24-bit address bus (16 MB)
  - 8 data registers, 8 address registers
  - Microcoded instruction execution
  - 4-158 cycles per instruction

Calibrated: 2026-01-28
Target CPI: ~6.5 for typical workloads
Used in: Macintosh, Amiga, Atari ST, arcade games
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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

    class BaseProcessorModel:
        pass


class M68000Model(BaseProcessorModel):
    """
    M68000 Grey-Box Queueing Model

    Architecture: 16/32-bit NMOS microprocessor (1979)
    - Microcoded execution (not pipelined)
    - CISC with orthogonal addressing modes
    - CPI ~6.5 for typical workloads
    """

    # Processor specifications
    name = "M68000"
    manufacturer = "Motorola"
    year = 1979
    clock_mhz = 8.0
    transistor_count = 68000
    data_width = 16
    address_width = 24

    def __init__(self):
        # M68000 instruction timing from datasheet
        # MOVE.L Dn,Dn @4, MOVE.L mem,Dn @12
        # ADD.L Dn,Dn @8, ADD mem,Dn @8
        # JMP @8, JSR @16, RTS @16, BRA @10
        # MULU @70, DIVU @140
        self.instruction_categories = {
            'alu_reg': InstructionCategory('alu_reg', 4.0, 0,
                "ADD/SUB Dn,Dn @4 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 4.0, 0,
                "MOVE Dn,Dn @4 cycles"),
            'memory': InstructionCategory('memory', 8.0, 0,
                "MOVE mem,Dn @8, MOVE Dn,mem @8"),
            'control': InstructionCategory('control', 8.0, 0,
                "JMP @8, BRA @10, weighted"),
            'multiply': InstructionCategory('multiply', 70.0, 0,
                "MULU/MULS @70"),
            'divide': InstructionCategory('divide', 140.0, 0,
                "DIVU/DIVS @140"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu_reg': 0.29,
                'data_transfer': 0.33,
                'memory': 0.22,
                'control': 0.15,
                'multiply': 0.005,
                'divide': 0.005,
            }, "Typical M68000 workload"),
            'compute': WorkloadProfile('compute', {
                'alu_reg': 0.44,
                'data_transfer': 0.27,
                'memory': 0.18,
                'control': 0.10,
                'multiply': 0.005,
                'divide': 0.005,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu_reg': 0.18,
                'data_transfer': 0.22,
                'memory': 0.45,
                'control': 0.14,
                'multiply': 0.005,
                'divide': 0.005,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu_reg': 0.20,
                'data_transfer': 0.22,
                'memory': 0.15,
                'control': 0.42,
                'multiply': 0.005,
                'divide': 0.005,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu_reg': -2.780197,
            'control': 2.115021,
            'data_transfer': 3.277875,
            'divide': -53.893587,
            'memory': -0.661327,
            'multiply': -26.946971
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using microcoded execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        # Apply correction terms from system identification
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
        """Run validation tests"""
        tests = []

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 6.5  # M68000 target CPI
        cpi_error = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': 'CPI accuracy',
            'passed': cpi_error < 5.0,
            'expected': f'{expected_cpi} +/- 5%',
            'actual': f'{result.cpi:.2f} ({cpi_error:.1f}% error)'
        })

        # Test 2: Workload weights sum to 1.0
        for profile_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            tests.append({
                'name': f'Weights sum ({profile_name})',
                'passed': 0.99 <= weight_sum <= 1.01,
                'expected': '1.0',
                'actual': f'{weight_sum:.2f}'
            })

        # Test 3: All cycle counts are positive and reasonable
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 0.5 <= cycles <= 200.0,
                'expected': '0.5-200 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range
        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 1.5,
            'expected': '0.05-1.5',
            'actual': f'{result.ipc:.3f}'
        })

        # Test 5: All workloads produce valid results
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
