#!/usr/bin/env python3
"""
WDC65816 Grey-Box Queueing Model
=================================

Architecture: 16-bit CMOS microprocessor (1984)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 16-bit extension of 6502 architecture
  - 8/16-bit switchable accumulator and index registers
  - 24-bit address bus (16 MB address space)
  - 16-bit operations take extra cycles
  - New long addressing modes (24-bit)
  - 2-8 cycles per instruction

Calibrated: 2026-01-28
Target CPI: ~3.8 for typical workloads (slower than 6502 due to 16-bit ops)
Used in: Super Nintendo (SNES), Apple IIGS
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


class Wdc65816Model(BaseProcessorModel):
    """
    WDC65816 Grey-Box Queueing Model

    Architecture: 16-bit CMOS microprocessor (1984)
    - 16-bit extension of 65C02
    - 8/16-bit modes for accumulator and index registers
    - 24-bit addressing for larger memory space
    - CPI ~3.8 for typical workloads (16-bit ops add cycles)
    """

    # Processor specifications
    name = "WDC65816"
    manufacturer = "Western Design Center"
    year = 1984
    clock_mhz = 4.0  # SNES ran at 3.58 MHz (NTSC) / 3.55 MHz (PAL)
    transistor_count = 22000
    data_width = 16  # Switchable 8/16-bit
    address_width = 24

    def __init__(self):
        # 65816 instruction timing
        # 16-bit operations add +1 cycle for the extra byte
        # Long addressing modes (24-bit) add +1 cycle
        # JSL/RTL (long subroutine calls) take 8/6 cycles
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.2, 0,
                "ALU ops - +1 cycle in 16-bit mode"),
            'data_transfer': InstructionCategory('data_transfer', 3.8, 0,
                "LDA/STA - mix of 8/16-bit modes"),
            'memory': InstructionCategory('memory', 4.5, 0,
                "Memory ops including long addressing"),
            'control': InstructionCategory('control', 3.5, 0,
                "Branches + long jumps (JML, JSL)"),
            'stack': InstructionCategory('stack', 4.0, 0,
                "Stack ops - 16-bit push/pull take longer"),
        }

        # Workload profiles for SNES/Apple IIGS typical usage
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.15,
                'memory': 0.30,
                'control': 0.20,
                'stack': 0.10,
            }, "Typical 65816 workload (SNES games)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.12,
                'stack': 0.08,
            }, "Memory-intensive (DMA, graphics)"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.12,
                'memory': 0.20,
                'control': 0.35,
                'stack': 0.15,
            }, "Control-flow intensive"),
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
        """Run validation tests against known 65816 characteristics"""
        tests = []

        # Test 1: CPI within expected range (target 3.8, allow 5% tolerance)
        result = self.analyze('typical')
        expected_cpi = 3.8
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

        # Test 3: All cycle counts are positive and reasonable (1-10 for 65816)
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 1.0 <= cycles <= 10.0,
                'expected': '1-10 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range for 65816 (0.2 - 0.5 typical)
        tests.append({
            'name': 'IPC range',
            'passed': 0.15 <= result.ipc <= 0.6,
            'expected': '0.15-0.6',
            'actual': f'{result.ipc:.3f}'
        })

        # Test 5: 65816 should be slower than 65C02 due to 16-bit overhead (CPI > 3.2)
        tests.append({
            'name': '65816 16-bit overhead',
            'passed': result.cpi > 3.2,
            'expected': 'CPI > 3.2 (16-bit overhead)',
            'actual': f'{result.cpi:.2f}'
        })

        # Test 6: All workloads produce valid results
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
