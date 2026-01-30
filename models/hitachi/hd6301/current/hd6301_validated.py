#!/usr/bin/env python3
"""
Hitachi HD6301 Grey-Box Queueing Model
=======================================

Architecture: 8-bit microcontroller (1983)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Enhanced 6801 with improved performance
  - 8-bit data bus, 16-bit address bus
  - On-chip RAM, ROM, timer, serial I/O
  - Faster instruction execution than 6801
  - 2-10 cycles per instruction

Calibrated: 2026-01-29
Target CPI: ~3.5 for typical workloads (faster than 6801)
Used in: Embedded systems, automotive, industrial controllers
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


class HD6301Model(BaseProcessorModel):
    """
    Hitachi HD6301 Grey-Box Queueing Model

    Architecture: 8-bit CMOS microcontroller (1983)
    - Enhanced 6801 with faster execution
    - On-chip RAM, ROM, timer, serial I/O
    - CPI ~3.5 for typical workloads (faster than 6801's 3.8)
    """

    # Processor specifications
    name = "HD6301"
    manufacturer = "Hitachi"
    year = 1983
    clock_mhz = 1.0  # Internal clock (external may be 4x)
    transistor_count = 40000
    data_width = 8
    address_width = 16

    def __init__(self):
        # HD6301 timing - optimized vs 6801
        # Hitachi improved the microcode for faster execution
        # Most instructions 1 cycle faster than 6801
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.4, 0,
                "ALU ops - ADDA imm @2, INCA @1, optimized"),
            'data_transfer': InstructionCategory('data_transfer', 2.6, 0,
                "LDAA imm @2, register moves"),
            'memory': InstructionCategory('memory', 3.8, 0,
                "LDAA dir @3, LDAA ext @4, STAA @4"),
            'control': InstructionCategory('control', 3.8, 0,
                "JMP @3, BEQ @3, weighted avg"),
            'stack': InstructionCategory('stack', 4.5, 0,
                "PSHA/PULA @3-4"),
            'call_return': InstructionCategory('call_return', 7.5, 0,
                "JSR @8, RTS @5, weighted"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.25,
                'control': 0.15,
                'stack': 0.05,
                'call_return': 0.05,
            }, "Typical HD6301 workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.10,
                'stack': 0.03,
                'call_return': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.45,
                'control': 0.12,
                'stack': 0.08,
                'call_return': 0.05,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.10,
                'call_return': 0.10,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.200654,
            'call_return': 0.773106,
            'control': -0.316850,
            'data_transfer': 1.434445,
            'memory': -0.107626,
            'stack': 2.146624
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
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
        """Run validation tests"""
        tests = []

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 3.5  # HD6301 target CPI
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
