#!/usr/bin/env python3
"""
MOS 8502 Grey-Box Queueing Model
===================================

Architecture: 8-bit (1985)
Queueing Model: Sequential execution

Features:
  - 2MHz 6502
  - C128
  - Dual-speed

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

    class BaseProcessorModel:
        pass


class Mos8502Model(BaseProcessorModel):
    """MOS 8502 - C128 CPU, 2MHz 6502 variant"""

    name = "MOS 8502"
    manufacturer = "MOS Technology"
    year = 1985
    clock_mhz = 2.0
    transistor_count = 7500
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.5, 0, "6502 ALU @2-3c"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Transfers @2-4c"),
            'memory': InstructionCategory('memory', 4.5, 0, "Addressing @4-6c"),
            'control': InstructionCategory('control', 4.5, 0, "Branch/jump @2-7c"),
            'stack': InstructionCategory('stack', 5.0, 0, "Push/pull @3-7c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.21,
                'data_transfer': 0.247,
                'memory': 0.191,
                'control': 0.191,
                'stack': 0.161,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.31,
                'data_transfer': 0.222,
                'memory': 0.166,
                'control': 0.166,
                'stack': 0.136,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.185,
                'data_transfer': 0.347,
                'memory': 0.166,
                'control': 0.166,
                'stack': 0.136,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.185,
                'data_transfer': 0.222,
                'memory': 0.166,
                'control': 0.291,
                'stack': 0.136,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.374744,
            'control': 0.273256,
            'data_transfer': 1.381256,
            'memory': -0.863826,
            'stack': -0.929661
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        # Apply correction terms from system identification
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            self.name, workload, corrected_cpi, self.clock_mhz, bottleneck, contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self):
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
