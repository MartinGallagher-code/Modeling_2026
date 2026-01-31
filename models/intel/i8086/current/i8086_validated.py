#!/usr/bin/env python3
"""
Intel 8086 Grey-Box Queueing Model
==================================

Architecture: Prefetch Queue (1978)
Foundation of x86 architecture.

Features:
  - 16-bit data bus
  - 6-byte prefetch queue
  - BIU/EU parallelism
  - 2-200 cycles per instruction

Target CPI: 4.5 (with prefetch queue benefit)
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
            ipc = 1.0 / cpi if cpi > 0 else 0.0
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

    class BaseProcessorModel:
        def get_corrections(self):
            return getattr(self, 'corrections', {})
        def set_corrections(self, corrections):
            self.corrections = corrections
        def compute_correction_delta(self, workload='typical'):
            profile = self.workload_profiles.get(workload, list(self.workload_profiles.values())[0])
            return sum(self.corrections.get(c, 0) * profile.category_weights.get(c, 0) for c in self.corrections)
        def compute_residuals(self, measured_cpi_dict):
            return {w: self.analyze(w).cpi - m for w, m in measured_cpi_dict.items()}
        def compute_loss(self, measured_cpi_dict):
            residuals = self.compute_residuals(measured_cpi_dict)
            return sum(r**2 for r in residuals.values()) / len(residuals) if residuals else 0
        def get_parameters(self):
            params = {}
            for c, cat in self.instruction_categories.items():
                params[f'cat.{c}.base_cycles'] = cat.base_cycles
            for c, v in self.corrections.items():
                params[f'cor.{c}'] = v
            return params
        def set_parameters(self, params):
            for k, v in params.items():
                if k.startswith('cat.') and k.endswith('.base_cycles'):
                    c = k[4:-12]
                    if c in self.instruction_categories:
                        self.instruction_categories[c].base_cycles = v
                elif k.startswith('cor.'):
                    c = k[4:]
                    self.corrections[c] = v
        def get_parameter_bounds(self):
            bounds = {}
            for c, cat in self.instruction_categories.items():
                bounds[f'cat.{c}.base_cycles'] = (0.1, cat.base_cycles * 5)
            for c in self.corrections:
                bounds[f'cor.{c}'] = (-50, 50)
            return bounds
        def get_parameter_metadata(self):
            return {k: {'type': 'category' if k.startswith('cat.') else 'correction'} for k in self.get_parameters()}
        def get_instruction_categories(self):
            return self.instruction_categories
        def get_workload_profiles(self):
            return self.workload_profiles
        def validate(self):
            return {'tests': [], 'passed': 0, 'total': 0, 'accuracy_percent': None}


class I8086Model(BaseProcessorModel):
    """
    Intel 8086 Grey-Box Queueing Model

    Foundation of x86 (1978)
    - 16-bit architecture
    - 6-byte prefetch queue
    - Effective CPI much lower than raw instruction timing due to prefetch
    """

    name = "Intel 8086"
    manufacturer = "Intel"
    year = 1978
    clock_mhz = 5.0
    transistor_count = 29000
    data_width = 16
    address_width = 20

    def __init__(self):
        # Real effective cycles including bus contention and EA calculation
        # 8086 has 16-bit bus but 4-clock bus cycles; memory operands dominate
        # ADD reg,reg=3 but ADD reg,mem=9+EA(~7)=16; weighted average ~8
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 8, 0, "ADD reg,reg @3, ADD reg,mem @16, weighted ~8"),
            'data_transfer': InstructionCategory('data_transfer', 8, 0, "MOV reg,reg @2, MOV reg,mem @15, weighted ~8"),
            'memory': InstructionCategory('memory', 14, 0, "PUSH/POP @11-17, LDS/LES @16-24, weighted ~14"),
            'control': InstructionCategory('control', 16, 0, "JMP @15, CALL near @19, CALL far @28, weighted ~16"),
            'multiply': InstructionCategory('multiply', 15, 0, "MUL 8b @70-77, MUL 16b @118-133, weighted avg ~15"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.35,
                'memory': 0.20,
                'control': 0.15,
                'multiply': 0.05,}, "Typical x86 workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.42,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.10,
                'multiply': 0.08,}, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.17,
                'data_transfer': 0.20,
                'memory': 0.45,
                'control': 0.15,
                'multiply': 0.03,}, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.40,
                'multiply': 0.02,}, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.26,
                'data_transfer': 0.30,
                'memory': 0.25,
                'control': 0.15,
                'multiply': 0.04,}, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -4.245990,
            'control': 4.714018,
            'data_transfer': 5.163653,
            'memory': 7.662285,
            'multiply': 28.076150
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
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

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck="prefetch_queue",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
