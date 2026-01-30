#!/usr/bin/env python3
"""
TI TMS1000 Grey-Box Queueing Model
==================================

Architecture: 4-bit Microcontroller (1974)
Queueing Model: Fixed-cycle sequential execution

Features:
  - First commercially available single-chip microcontroller
  - 4-bit data path, Harvard architecture
  - All instructions take exactly 6 clock cycles
  - No interrupts, single-level stack
  - LFSR-based program counter

Date: 2026-01-28
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


class Tms1000Model(BaseProcessorModel):
    """
    TI TMS1000 Grey-Box Queueing Model

    Architecture: 4-bit Fixed-Cycle MCU (1974)
    - All instructions execute in exactly 6 clock cycles
    - Harvard architecture (separate program/data memory)
    - 43 instructions in base TMS1000
    - 4-bit data path with BCD arithmetic support
    """

    # Processor specifications
    name = "TMS1000"
    manufacturer = "Texas Instruments"
    year = 1974
    clock_mhz = 0.3  # 300 kHz typical internal clock
    transistor_count = 8000
    data_width = 4
    address_width = 10  # 1KB ROM

    def __init__(self):
        # TMS1000 has FIXED instruction timing - all instructions = 6 cycles
        # This makes the model very simple
        self.fixed_cycles = 6

        # Instruction categories - all same cycle count, but different frequencies
        # CPI is always 6.0 regardless of workload mix
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 6, 0, "ALU: ADD, SUB, comparisons @6 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 6, 0, "Transfer: TAM, TMA, TMY @6 cycles"),
            'memory': InstructionCategory('memory', 6, 0, "Memory: LDP, LDX @6 cycles"),
            'control': InstructionCategory('control', 6, 0, "Control: BR, CALL @6 cycles"),
            'io': InstructionCategory('io', 6, 0, "I/O: TDO, SETR, RSTR @6 cycles"),
        }

        # Workload profiles - don't affect CPI due to fixed timing
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'io': 0.15,
            }, "Typical embedded controller workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.10,
                'io': 0.05,
            }, "Compute-intensive (calculator-like)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.35,
                'memory': 0.30,
                'control': 0.10,
                'io': 0.10,
            }, "Memory/data-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.30,
                'io': 0.20,
            }, "Control-flow and I/O intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using fixed-cycle execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # TMS1000 always has CPI = 6.0 (fixed timing)
        total_cpi = self.fixed_cycles

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        # Calculate category contributions for analysis
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
        bottleneck = max(contributions, key=contributions.get)

        # System identification: apply correction terms
        base_cpi = total_cpi
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

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
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: CPI should be exactly 6.0
        result = self.analyze('typical')
        test1 = {
            "name": "CPI accuracy",
            "expected": 6.0,
            "actual": result.cpi,
            "passed": abs(result.cpi - 6.0) < 0.01
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: IPS at 300 kHz should be ~50,000
        expected_ips = 50000
        test2 = {
            "name": "IPS at 300 kHz",
            "expected": expected_ips,
            "actual": result.ips,
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.01
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: All workloads should give same CPI
        for wl in ['compute', 'memory', 'control']:
            r = self.analyze(wl)
            test = {
                "name": f"CPI consistency ({wl})",
                "expected": 6.0,
                "actual": r.cpi,
                "passed": abs(r.cpi - 6.0) < 0.01
            }
            tests.append(test)
            if test["passed"]: passed += 1

        accuracy = (passed / len(tests)) * 100 if tests else 0
        return {
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "accuracy_percent": accuracy
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
