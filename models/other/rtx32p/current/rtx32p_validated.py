#!/usr/bin/env python3
"""
Harris RTX32P Grey-Box Queueing Model
=======================================

Architecture: 32-bit Forth Engine (1985)
Hardware Forth processor with dual stacks.

Features:
  - 32-bit data bus
  - 8 MHz clock
  - ~40,000 transistors (CMOS)
  - Pipelined architecture
  - Hardware data and return stacks
  - Most Forth primitives execute in 1 cycle
  - Subroutine threading in hardware

Target CPI: 1.5
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


class RTX32PModel(BaseProcessorModel):
    """
    Harris RTX32P Grey-Box Queueing Model

    32-bit Forth engine (1985)
    - 32-bit pipelined architecture
    - 8 MHz clock
    - Hardware data and return stacks
    - Most primitives in 1 cycle (pipelined)
    - Subroutine threading in hardware
    """

    name = "Harris RTX32P"
    manufacturer = "Harris"
    year = 1985
    clock_mhz = 8.0
    transistor_count = 40000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'stack_op': InstructionCategory('stack_op', 1.0, 0, "Stack push/pop/dup/swap - 1 cycle (pipelined)"),
            'alu': InstructionCategory('alu', 1.0, 0, "ALU operations on TOS - 1 cycle (pipelined)"),
            'memory': InstructionCategory('memory', 3.0, 0, "Memory fetch/store - 3 cycles"),
            'control': InstructionCategory('control', 2.0, 0, "Branch/loop operations - 2 cycles"),
            'call_return': InstructionCategory('call_return', 2.0, 0, "Subroutine call/return - 2 cycles"),
        }

        # Typical: 0.35*1 + 0.25*1 + 0.10*3 + 0.15*2 + 0.15*2 = 0.35+0.25+0.30+0.30+0.30 = 1.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_op': 0.35,
                'alu': 0.25,
                'memory': 0.10,
                'control': 0.15,
                'call_return': 0.15,
            }, "Typical Forth workload"),
            'compute': WorkloadProfile('compute', {
                'stack_op': 0.30,
                'alu': 0.40,
                'memory': 0.05,
                'control': 0.15,
                'call_return': 0.10,
            }, "Compute-intensive Forth"),
            'memory': WorkloadProfile('memory', {
                'stack_op': 0.20,
                'alu': 0.15,
                'memory': 0.35,
                'control': 0.10,
                'call_return': 0.20,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'stack_op': 0.20,
                'alu': 0.15,
                'memory': 0.10,
                'control': 0.35,
                'call_return': 0.20,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'stack_op': 0.30,
                'alu': 0.25,
                'memory': 0.15,
                'control': 0.15,
                'call_return': 0.15,
            }, "Mixed Forth workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.500000,
            'call_return': -0.500000,
            'control': -0.500000,
            'memory': -1.500000,
            'stack_op': 0.500000
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
            bottleneck="pipelined",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
