#!/usr/bin/env python3
"""
DEC J-11 Grey-Box Queueing Model
===================================

Architecture: 16-bit (1983)
Queueing Model: Sequential execution

Features:
  - Fastest PDP-11
  - Pipelined
  - 175K transistors

Date: 2026-01-29
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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

    class BaseProcessorModel:
        pass


class DecJ11Model(BaseProcessorModel):
    """DEC J-11 - Fastest PDP-11 chip for PDP-11/73 and 11/84"""

    name = "DEC J-11"
    manufacturer = "DEC"
    year = 1983
    clock_mhz = 15.0
    transistor_count = 175000
    data_width = 16
    address_width = 22

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "Pipelined ALU @2-4c"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Reg MOV @2-4c"),
            'memory': InstructionCategory('memory', 5.0, 0, "Memory @4-7c"),
            'control': InstructionCategory('control', 5.0, 0, "Branch/JSR @3-8c"),
            'stack': InstructionCategory('stack', 5.5, 0, "Stack @4-7c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.262,
                'data_transfer': 0.261,
                'memory': 0.167,
                'control': 0.167,
                'stack': 0.143,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.362,
                'data_transfer': 0.236,
                'memory': 0.142,
                'control': 0.142,
                'stack': 0.118,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.237,
                'data_transfer': 0.361,
                'memory': 0.142,
                'control': 0.142,
                'stack': 0.118,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.237,
                'data_transfer': 0.236,
                'memory': 0.142,
                'control': 0.267,
                'stack': 0.118,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -4.761346,
            'control': 2.806755,
            'data_transfer': 5.000000,
            'memory': 1.239684,
            'stack': -5.000000
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            self.name, workload, corrected_cpi, self.clock_mhz, bottleneck, contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self):
        target_cpi = 4.0
        result = self.analyze("typical")
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        passed = error_pct < 5.0
        return {
            "tests": [{
                "name": "typical_cpi",
                "target": target_cpi,
                "actual": round(result.cpi, 3),
                "error_pct": round(error_pct, 2),
                "passed": passed
            }],
            "passed": 1 if passed else 0,
            "total": 1,
            "accuracy_percent": round(100 - error_pct, 2)
        }

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
