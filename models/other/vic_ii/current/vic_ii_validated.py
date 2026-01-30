#!/usr/bin/env python3
"""
Commodore VIC-II (6567) Grey-Box Queueing Model
=================================================

Architecture: 12-bit Video Interface Controller (1982)
Queueing Model: Sequential execution

Features:
  - Commodore 64 video chip
  - Character and bitmap graphics modes
  - 8 hardware sprites with multicolor support
  - Hardware smooth scrolling
  - Raster interrupt generation
  - DMA cycle stealing from CPU bus
  - 16 fixed colors

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

class VicIiModel(BaseProcessorModel):
    """Commodore VIC-II (6567/6569) - C64 Video Interface Controller"""

    name = "Commodore VIC-II (6567)"
    manufacturer = "MOS Technology/Commodore"
    year = 1982
    clock_mhz = 8.0
    transistor_count = 16000
    data_width = 12
    address_width = 14

    def __init__(self):
        self.instruction_categories = {
            'char_gen': InstructionCategory('char_gen', 3.0, 0, "Character generation @3c"),
            'sprite': InstructionCategory('sprite', 5.0, 0, "Sprite processing @5c"),
            'scroll': InstructionCategory('scroll', 4.0, 0, "Smooth scroll @4c"),
            'raster': InstructionCategory('raster', 3.0, 0, "Raster/sync @3c"),
            'dma': InstructionCategory('dma', 6.0, 0, "DMA cycle steal @6c"),
            'color': InstructionCategory('color', 3.0, 0, "Color lookup @3c"),
        }
        # Target CPI = 4.0
        # 3*w1 + 5*w2 + 4*w3 + 3*w4 + 6*w5 + 3*w6 = 4.0
        # Try: char_gen=0.20, sprite=0.20, scroll=0.15, raster=0.15, dma=0.15, color=0.15
        # Check: 0.60+1.00+0.60+0.45+0.90+0.45 = 4.00 exact!
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'char_gen': 0.20,
                'sprite': 0.20,
                'scroll': 0.15,
                'raster': 0.15,
                'dma': 0.15,
                'color': 0.15,
            }, "Typical C64 game rendering"),
            'compute': WorkloadProfile('compute', {
                'char_gen': 0.15,
                'sprite': 0.30,
                'scroll': 0.15,
                'raster': 0.10,
                'dma': 0.15,
                'color': 0.15,
            }, "Sprite-heavy game scene"),
            'memory': WorkloadProfile('memory', {
                'char_gen': 0.15,
                'sprite': 0.10,
                'scroll': 0.10,
                'raster': 0.15,
                'dma': 0.35,
                'color': 0.15,
            }, "DMA-heavy memory workload"),
            'control': WorkloadProfile('control', {
                'char_gen': 0.15,
                'sprite': 0.15,
                'scroll': 0.20,
                'raster': 0.20,
                'dma': 0.10,
                'color': 0.20,
            }, "Raster/scroll-heavy control workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'char_gen': 0.316739,
            'color': 1.097961,
            'dma': -1.164866,
            'raster': 2.189551,
            'scroll': 1.117507,
            'sprite': -2.746855
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
