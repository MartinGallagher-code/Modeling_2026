#!/usr/bin/env python3
"""
KR581IK2 Grey-Box Queueing Model
===================================

Architecture: Data path processor (1983)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Soviet clone of Western Digital MCP-1600 chipset (part 2)
  - Data path component of 2-chip CPU
  - Used together with KR581IK1 (control/microcode)
  - 16-bit ALU and register file
  - PDP-11 compatible addressing modes
  - Used in DEC LSI-11 compatible systems

Calibrated: 2026-01-29
Target CPI: ~8.0 for typical workloads (same as WD MCP-1600)
Used in: Soviet LSI-11 compatible systems, Elektronika-60
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


class KR581IK2Model(BaseProcessorModel):
    """
    KR581IK2 Grey-Box Queueing Model

    Architecture: Data path chip (1983)
    - Soviet clone of WD MCP-1600 chipset (part 2 - data path)
    - Used with KR581IK1 (control/microcode) to form complete CPU
    - 16-bit ALU and register file
    - Same timing as WD MCP-1600
    - CPI ~8.0 for typical workloads
    """

    # Processor specifications
    name = "KR581IK2"
    manufacturer = "Soviet Union"
    year = 1983
    clock_mhz = 2.5  # 2.5 MHz typical
    transistor_count = 6000  # Estimated for data path chip
    data_width = 16
    address_width = 16

    def __init__(self):
        # KR581IK2 instruction timing identical to WD MCP-1600
        # Same timing as KR581IK1 (they form one CPU)
        #
        # Typical instruction timings (PDP-11 ISA via microcode):
        #   MOV Rn,Rn: 3-4 microcode cycles
        #   ADD Rn,Rn: 4-5 microcode cycles
        #   MOV (Rn),Rn: 8-10 cycles (memory access)
        #   JMP addr: 6-8 cycles
        #   JSR addr: 10-12 cycles
        #   RTS: 6-8 cycles
        #   SOB: 5-6 cycles (loop)

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 5.0, 0,
                "ALU ops - ADD/SUB Rn,Rn @4-5, with memory @8-10, weighted ~5"),
            'data_transfer': InstructionCategory('data_transfer', 6.0, 0,
                "MOV Rn,Rn @3-4, MOV (Rn),Rn @8-10, weighted ~6"),
            'memory': InstructionCategory('memory', 10.0, 0,
                "Memory-indirect modes, deferred addressing ~10"),
            'io': InstructionCategory('io', 12.0, 0,
                "I/O via memory-mapped registers ~12"),
            'control': InstructionCategory('control', 8.0, 0,
                "JMP @6-8, JSR @10-12, RTS @6-8, SOB @5-6, weighted ~8"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'io': 0.10,
                'control': 0.20,
            }, "Typical KR581IK2 workload (PDP-11 compatible)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'io': 0.10,
                'control': 0.20,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.15,
                'memory': 0.15,
                'io': 0.12,
                'control': 0.40,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
        expected_cpi = 8.0  # Same as WD MCP-1600
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
