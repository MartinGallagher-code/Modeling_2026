#!/usr/bin/env python3
"""
K1810VM86 Grey-Box Queueing Model
====================================

Architecture: 16-bit microprocessor (1985)
Queueing Model: Sequential execution with prefetch, cycle-accurate

Features:
  - Soviet Intel 8086 clone
  - 16-bit data bus, 20-bit address bus (1MB)
  - Full 8086 instruction set compatibility
  - 6-byte instruction prefetch queue
  - Segment-based memory model (CS, DS, SS, ES)
  - Hardware multiply/divide
  - 2-200+ cycles per instruction

Calibrated: 2026-01-29
Target CPI: ~6.5 for typical workloads (same as Intel 8086)
Used in: Soviet ES-1841 (IBM PC clone), various Soviet PCs
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


class K1810VM86Model(BaseProcessorModel):
    """
    K1810VM86 Grey-Box Queueing Model

    Architecture: 16-bit NMOS microprocessor (1985)
    - Soviet Intel 8086 clone
    - Sequential execution with 6-byte prefetch queue
    - Same instruction timing as Intel 8086
    - CPI ~6.5 for typical workloads
    """

    # Processor specifications
    name = "K1810VM86"
    manufacturer = "Soviet Union"
    year = 1985
    clock_mhz = 5.0  # 5 MHz typical
    transistor_count = 29000  # Same as 8086
    data_width = 16
    address_width = 20

    def __init__(self):
        # K1810VM86 instruction timing identical to Intel 8086
        #
        # Actual instruction timings (same as 8086):
        #   MOV reg,reg: 2 cycles
        #   MOV reg,imm: 4 cycles
        #   MOV reg,mem: 8+EA cycles
        #   ADD reg,reg: 3 cycles
        #   ADD reg,mem: 9+EA cycles
        #   MUL (16-bit): 118-133 cycles
        #   DIV (16-bit): 144-162 cycles
        #   JMP near: 15 cycles
        #   CALL near: 19 cycles
        #   RET: 8 cycles
        #   PUSH: 11 cycles
        #   POP: 8 cycles
        #   IN/OUT: 8-12 cycles

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 4.0, 0,
                "ALU ops - ADD reg,reg @3, ADD reg,mem @9+EA, INC @2, weighted ~4"),
            'data_transfer': InstructionCategory('data_transfer', 4.0, 0,
                "MOV reg,reg @2, MOV reg,imm @4, MOV reg,mem @8+EA, weighted ~4"),
            'memory': InstructionCategory('memory', 10.0, 0,
                "Memory ops with EA calculation, segment overhead ~10"),
            'io': InstructionCategory('io', 10.0, 0,
                "IN/OUT @8-12 cycles"),
            'control': InstructionCategory('control', 8.0, 0,
                "JMP @15, CALL @19, RET @8, conditional Jcc ~8"),
            'stack': InstructionCategory('stack', 9.0, 0,
                "PUSH @11, POP @8, PUSHF/POPF ~9"),
            'string': InstructionCategory('string', 12.0, 0,
                "REP MOVSW/STOSW/CMPSW with loop overhead ~12"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
                'stack': 0.10,
                'string': 0.05,
            }, "Typical K1810VM86 workload (PC-compatible software)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.12,
                'io': 0.03,
                'control': 0.12,
                'stack': 0.05,
                'string': 0.03,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.30,
                'io': 0.05,
                'control': 0.12,
                'stack': 0.08,
                'string': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.15,
                'memory': 0.10,
                'io': 0.05,
                'control': 0.35,
                'stack': 0.12,
                'string': 0.05,
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
        expected_cpi = 6.5  # Same as Intel 8086
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
