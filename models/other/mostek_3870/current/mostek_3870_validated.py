#!/usr/bin/env python3
"""
Mostek 3870 Grey-Box Queueing Model
====================================

Architecture: 8-bit microcontroller (1977)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - F8-compatible single-chip microcontroller
  - 8-bit data bus
  - On-chip RAM, ROM, I/O, timer
  - Faster than original F8 multi-chip design
  - 4-20 cycles per instruction

Target CPI: 6.0 (faster than F8's 7.0)
Used in: Consumer electronics, games, embedded control
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

class BaseProcessorModel:
    pass


class Mostek3870Model(BaseProcessorModel):
    """
    Mostek 3870 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microcontroller (1977)
    - F8-compatible single-chip design
    - Faster than original F8 multi-chip
    - 64-byte scratchpad RAM
    - CPI ~6.0 for typical workloads
    """

    # Processor specifications
    name = "Mostek 3870"
    manufacturer = "Mostek"
    year = 1977
    clock_mhz = 4.0  # Up to 4 MHz (faster than F8's 2 MHz)
    transistor_count = 8000  # Estimated
    data_width = 8
    address_width = 16

    def __init__(self):
        # Mostek 3870 instruction timing
        # F8-compatible but faster due to single-chip design
        # Target CPI: 6.0 (vs F8's 7.0)
        # Calibration: 0.40*4.5 + 0.20*6 + 0.18*7 + 0.10*7 + 0.08*8 + 0.04*11 = 5.94 ~ 6.0
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 4.5, 0, "Register-to-register operations"),
            'immediate': InstructionCategory('immediate', 6.0, 0, "Immediate operand instructions"),
            'memory_read': InstructionCategory('memory_read', 7.0, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 7.0, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 8.0, 0, "Branch/jump instructions"),
            'call_return': InstructionCategory('call_return', 11.0, 0, "Subroutine call/return"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.40,
                'immediate': 0.20,
                'memory_read': 0.18,
                'memory_write': 0.10,
                'branch': 0.08,
                'call_return': 0.04,
            }, "Typical embedded workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.50,
                'immediate': 0.25,
                'memory_read': 0.10,
                'memory_write': 0.05,
                'branch': 0.08,
                'call_return': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.15,
                'immediate': 0.10,
                'memory_read': 0.40,
                'memory_write': 0.25,
                'branch': 0.05,
                'call_return': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.20,
                'immediate': 0.10,
                'memory_read': 0.15,
                'memory_write': 0.10,
                'branch': 0.30,
                'call_return': 0.15,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'register_ops': 0.30,
                'immediate': 0.18,
                'memory_read': 0.22,
                'memory_write': 0.12,
                'branch': 0.12,
                'call_return': 0.06,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'branch': -3.530373,
            'call_return': -1.818753,
            'immediate': -1.191236,
            'memory_read': 0.104789,
            'memory_write': -3.039048,
            'register_ops': 2.196175
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        # Identify bottleneck (highest contribution)
        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests against known Mostek 3870 characteristics"""
        tests = []

        # Test 1: CPI within expected range (target 6.0)
        result = self.analyze('typical')
        expected_cpi = 6.0
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
                'passed': 1.0 <= cycles <= 20.0,
                'expected': '1-20 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range
        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 0.5,
            'expected': '0.05-0.5',
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
