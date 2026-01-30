#!/usr/bin/env python3
"""
GI AY-3-8910 PSG Grey-Box Queueing Model
============================================

Architecture: 8-bit Programmable Sound Generator (1978)
Queueing Model: Sequential execution

Features:
  - 3 square wave tone generators
  - 1 noise generator (pseudo-random)
  - 1 shared envelope generator
  - 3-channel mixer with per-channel tone/noise enable
  - 2 general-purpose 8-bit I/O ports
  - Used in MSX, ZX Spectrum 128, Atari ST, Vectrex, many arcade games

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

class Ay38910Model(BaseProcessorModel):
    """GI AY-3-8910 PSG - Programmable Sound Generator"""

    name = "GI AY-3-8910 PSG"
    manufacturer = "General Instrument"
    year = 1978
    clock_mhz = 1.79
    transistor_count = 5000
    data_width = 8
    address_width = 4

    def __init__(self):
        self.instruction_categories = {
            'tone_gen': InstructionCategory('tone_gen', 3, 0, "Tone generator (square wave) @3 cycles"),
            'noise_gen': InstructionCategory('noise_gen', 4, 0, "Noise generator (LFSR) @4 cycles"),
            'envelope': InstructionCategory('envelope', 5, 0, "Envelope generator (shared) @5 cycles"),
            'mixer': InstructionCategory('mixer', 3, 0, "Channel mixer @3 cycles"),
            'io_port': InstructionCategory('io_port', 4, 0, "I/O port access @4 cycles"),
        }
        # Target typical CPI: 3.5
        # Weights: tone_gen=0.2857, noise_gen=0.1786, envelope=0.0714, mixer=0.2857, io_port=0.1786
        # Verify: 0.2857*3 + 0.1786*4 + 0.0714*5 + 0.2857*3 + 0.1786*4
        #       = 0.8571+0.7143+0.3571+0.8571+0.7143 = 3.5
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'tone_gen': 0.286,
                'noise_gen': 0.179,
                'envelope': 0.071,
                'mixer': 0.286,
                'io_port': 0.178,
            }, "Typical PSG operation - tone generation dominant"),
            'compute': WorkloadProfile('compute', {
                'tone_gen': 0.300,
                'noise_gen': 0.250,
                'envelope': 0.150,
                'mixer': 0.200,
                'io_port': 0.100,
            }, "Compute-intensive - heavy tone and noise generation"),
            'memory': WorkloadProfile('memory', {
                'tone_gen': 0.200,
                'noise_gen': 0.150,
                'envelope': 0.100,
                'mixer': 0.200,
                'io_port': 0.350,
            }, "Memory-intensive - frequent I/O port access"),
            'control': WorkloadProfile('control', {
                'tone_gen': 0.200,
                'noise_gen': 0.150,
                'envelope': 0.300,
                'mixer': 0.200,
                'io_port': 0.150,
            }, "Control-flow intensive - envelope-heavy operation"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'envelope': -0.059401,
            'io_port': 0.007225,
            'mixer': 0.060062,
            'noise_gen': 0.006889,
            'tone_gen': 0.060062
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
