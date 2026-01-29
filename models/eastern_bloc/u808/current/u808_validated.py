#!/usr/bin/env python3
"""
VEB U808 Grey-Box Queueing Model
=================================

Architecture: 8-bit microprocessor (1978)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - East German Intel 8008 clone by VEB Mikroelektronik Erfurt
  - First East German microprocessor
  - 8-bit data bus, 14-bit address bus (16KB)
  - Intel 8008 instruction set compatibility
  - Stack on-chip (7-level)
  - 5-11 T-states per instruction (multi-cycle)

Calibrated: 2026-01-29
Target CPI: ~10.0 for typical workloads (same as Intel 8008)
Used in: Early East German industrial controllers, educational systems
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


class U808Model(BaseProcessorModel):
    """
    VEB U808 Grey-Box Queueing Model

    Architecture: 8-bit PMOS microprocessor (1978)
    - Intel 8008 clone by VEB Mikroelektronik Erfurt
    - First East German microprocessor
    - Sequential execution (no pipeline)
    - Same instruction timing as Intel 8008
    - CPI ~10.0 for typical workloads
    """

    # Processor specifications
    name = "U808"
    manufacturer = "VEB Mikroelektronik Erfurt"
    year = 1978
    clock_mhz = 0.5  # 500 kHz typical
    transistor_count = 3500  # Same as 8008
    data_width = 8
    address_width = 14

    def __init__(self):
        # U808 instruction timing identical to Intel 8008
        # VEB's clone maintains full timing compatibility
        #
        # Actual instruction timings (same as 8008):
        #   MOV r,r: 5 T-states (1 cycle = 2 states)
        #   MOV r,M: 8 T-states
        #   ADD r: 5 T-states
        #   ADD M: 8 T-states
        #   MVI r: 8 T-states
        #   LXI: 8 T-states
        #   JMP: 11 T-states
        #   CALL: 11 T-states
        #   RET: 5 T-states
        #   INP/OUT: 8 T-states

        # Instruction categories calibrated to 8008 timing
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 8.0, 0,
                "ALU ops - ADD/SUB register @5T, memory @8T, weighted ~8"),
            'data_transfer': InstructionCategory('data_transfer', 7.0, 0,
                "MOV r,r @5T, MVI @8T, MOV r,M @8T - weighted ~7"),
            'memory': InstructionCategory('memory', 14.0, 0,
                "Memory ops with indirect @8-16T, multi-byte ~14"),
            'io': InstructionCategory('io', 12.0, 0,
                "INP/OUT @8T with setup overhead ~12"),
            'control': InstructionCategory('control', 10.0, 0,
                "JMP @11T, CALL @11T, RET @5T, conditional ~10"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'io': 0.10,
                'control': 0.20,
            }, "Typical U808 workload (industrial control)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
            }, "Compute-intensive"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.15,
                'io': 0.30,
                'control': 0.20,
            }, "I/O-intensive industrial control"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.20,
                'io': 0.15,
                'control': 0.35,
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
        """Run validation tests"""
        tests = []

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 10.0  # Same as Intel 8008
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
