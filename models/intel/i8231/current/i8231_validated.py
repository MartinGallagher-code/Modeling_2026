#!/usr/bin/env python3
"""
Intel 8231 Grey-Box Queueing Model
=====================================

Architecture: 8-bit (1977)
Queueing Model: Sequential execution

Features:
  - Fixed+floating-point
  - 32-bit via 8-bit bus

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


class I8231Model(BaseProcessorModel):
    """Intel 8231 - Arithmetic Processing Unit, simpler than 8087"""

    name = "Intel 8231"
    manufacturer = "Intel"
    year = 1977
    clock_mhz = 2.0
    transistor_count = 8000
    data_width = 8
    address_width = 8

    def __init__(self):
        self.instruction_categories = {
            'fp_add': InstructionCategory('fp_add', 30.0, 0, "FP add @25-35c"),
            'fp_mul': InstructionCategory('fp_mul', 45.0, 0, "FP mul @40-50c"),
            'fp_div': InstructionCategory('fp_div', 65.0, 0, "FP div @55-75c"),
            'fixed_point': InstructionCategory('fixed_point', 25.0, 0, "Fixed-point @20-30c"),
            'data_transfer': InstructionCategory('data_transfer', 15.0, 0, "Bus transfer @10-20c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_add': 0.18,
                'fp_mul': 0.485,
                'fp_div': 0.126,
                'fixed_point': 0.128,
                'data_transfer': 0.081,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'fp_add': 0.28,
                'fp_mul': 0.46,
                'fp_div': 0.101,
                'fixed_point': 0.103,
                'data_transfer': 0.056,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'fp_add': 0.155,
                'fp_mul': 0.46,
                'fp_div': 0.101,
                'fixed_point': 0.103,
                'data_transfer': 0.181,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'fp_add': 0.155,
                'fp_mul': 0.46,
                'fp_div': 0.101,
                'fixed_point': 0.228,
                'data_transfer': 0.056,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'data_transfer': 1.773538,
            'fixed_point': 12.493538,
            'fp_add': 8.733538,
            'fp_div': -30.651804,
            'fp_mul': 1.478889
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        bottleneck = max(contributions, key=contributions.get)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
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
