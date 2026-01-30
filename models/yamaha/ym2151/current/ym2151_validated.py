#!/usr/bin/env python3
"""
Yamaha YM2151 OPM Grey-Box Queueing Model
=============================================

Architecture: 8-bit FM Synthesis (1983)
Queueing Model: Sequential execution

Features:
  - 8 channels, 4 operators per channel (32 total operators)
  - 4-operator FM synthesis with 8 algorithms
  - Hardware LFO with 4 waveforms
  - Stereo output (L/R panning per channel)
  - Used in arcade games (Sega, Capcom, Konami)

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi,
                       correction_delta=correction_delta)

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

class Ym2151Model(BaseProcessorModel):
    """Yamaha YM2151 OPM - 4-operator FM synthesis chip"""

    name = "Yamaha YM2151 OPM"
    manufacturer = "Yamaha"
    year = 1983
    clock_mhz = 3.58
    transistor_count = 20000
    data_width = 8
    address_width = 8

    def __init__(self):
        self.instruction_categories = {
            'operator': InstructionCategory('operator', 6, 0, "FM operator computation @6 cycles"),
            'envelope': InstructionCategory('envelope', 4, 0, "ADSR envelope generation @4 cycles"),
            'lfo': InstructionCategory('lfo', 3, 0, "Low-frequency oscillator @3 cycles"),
            'output': InstructionCategory('output', 5, 0, "DAC output and stereo mixing @5 cycles"),
            'register': InstructionCategory('register', 2, 0, "Register write @2 cycles"),
        }
        # Target typical CPI: 4.5
        # Weights: operator=0.30, envelope=0.20, lfo=0.15, output=0.25, register=0.10
        # Verify: 0.30*6 + 0.20*4 + 0.15*3 + 0.25*5 + 0.10*2 = 1.8+0.8+0.45+1.25+0.2 = 4.5
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'operator': 0.300,
                'envelope': 0.200,
                'lfo': 0.150,
                'output': 0.250,
                'register': 0.100,
            }, "Typical FM synthesis - balanced operator and output"),
            'compute': WorkloadProfile('compute', {
                'operator': 0.400,
                'envelope': 0.200,
                'lfo': 0.150,
                'output': 0.200,
                'register': 0.050,
            }, "Compute-intensive - heavy FM operator processing"),
            'memory': WorkloadProfile('memory', {
                'operator': 0.200,
                'envelope': 0.150,
                'lfo': 0.100,
                'output': 0.300,
                'register': 0.250,
            }, "Memory-intensive - frequent register access"),
            'control': WorkloadProfile('control', {
                'operator': 0.250,
                'envelope': 0.300,
                'lfo': 0.200,
                'output': 0.150,
                'register': 0.100,
            }, "Control-flow intensive - envelope and LFO heavy"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'envelope': 3.530644,
            'lfo': -1.102631,
            'operator': -2.882666,
            'output': -0.329339,
            'register': 4.064006
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
