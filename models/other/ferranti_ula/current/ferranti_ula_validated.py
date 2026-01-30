#!/usr/bin/env python3
"""
Ferranti ULA Grey-Box Queueing Model
=======================================

Architecture: 8-bit (1981)
Queueing Model: Sequential execution

Features:
  - ZX Spectrum
  - Bus contention
  - Video gen

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


class FerrantiUlaModel(BaseProcessorModel):
    """Ferranti ULA - ZX Spectrum ULA for memory/IO/video"""

    name = "Ferranti ULA"
    manufacturer = "Ferranti"
    year = 1981
    clock_mhz = 3.5
    transistor_count = 5000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'memory_ctrl': InstructionCategory('memory_ctrl', 4.0, 0, "Bus arb @3-5c"),
            'video_gen': InstructionCategory('video_gen', 5.0, 0, "Video @4-6c"),
            'io_decode': InstructionCategory('io_decode', 5.0, 0, "I/O decode @4-6c"),
            'contention': InstructionCategory('contention', 6.0, 0, "Contention @5-8c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'memory_ctrl': 0.2,
                'video_gen': 0.3,
                'io_decode': 0.3,
                'contention': 0.2,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'memory_ctrl': 0.3,
                'video_gen': 0.267,
                'io_decode': 0.267,
                'contention': 0.166,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'memory_ctrl': 0.3,
                'video_gen': 0.267,
                'io_decode': 0.267,
                'contention': 0.166,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'memory_ctrl': 0.167,
                'video_gen': 0.267,
                'io_decode': 0.267,
                'contention': 0.299,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'contention': 0.022613,
            'io_decode': -0.083145,
            'memory_ctrl': 0.022613,
            'video_gen': -0.083145
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
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
