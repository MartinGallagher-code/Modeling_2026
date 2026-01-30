#!/usr/bin/env python3
"""
Ensoniq OTTO (ES5505) Grey-Box Queueing Model
=============================================

Architecture: 32-voice wavetable, Gravis Ultrasound / Taito F3
Year: 1991, Clock: 16.0 MHz

Target CPI: 2.2
"""

from dataclasses import dataclass
from typing import Dict, Any

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


class EnsoniqOttoModel:
    """
    Ensoniq OTTO (ES5505) Grey-Box Queueing Model

    32-voice wavetable, Gravis Ultrasound / Taito F3 (1991)
    - 32 voices
    - Wavetable synthesis
    - 16-bit output
    """

    name = "Ensoniq OTTO (ES5505)"
    manufacturer = "Ensoniq"
    year = 1991
    clock_mhz = 16.0
    transistor_count = 250000
    data_width = 16
    address_width = 21

    def __init__(self):
        self.instruction_categories = {
            'oscillator': InstructionCategory('oscillator', 2.0, 0, "Waveform generation"),
            'envelope': InstructionCategory('envelope', 2.0, 0, "Envelope/modulation"),
            'register': InstructionCategory('register', 1.0, 0, "Register write"),
            'memory': InstructionCategory('memory', 2.0, 0, "Sample memory access"),
            'control': InstructionCategory('control', 3.0, 0, "Sequencing/control"),
            'mixing': InstructionCategory('mixing', 2.0, 0, "Channel mixing"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'oscillator': 0.3,
                'envelope': 0.2,
                'register': 0.1,
                'memory': 0.15,
                'control': 0.1,
                'mixing': 0.15,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'oscillator': 0.4,
                'envelope': 0.25,
                'register': 0.05,
                'memory': 0.1,
                'control': 0.05,
                'mixing': 0.15,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'oscillator': 0.2,
                'envelope': 0.15,
                'register': 0.1,
                'memory': 0.3,
                'control': 0.1,
                'mixing': 0.15,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'oscillator': 0.2,
                'envelope': 0.15,
                'register': 0.15,
                'memory': 0.15,
                'control': 0.25,
                'mixing': 0.1,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'oscillator': 0.25,
                'envelope': 0.2,
                'register': 0.1,
                'memory': 0.2,
                'control': 0.1,
                'mixing': 0.15,
            }, "Mixed workload"),
        }

        self.corrections = {
            'oscillator': 0.200000,
            'envelope': 0.200000,
            'register': 0.200000,
            'memory': 0.200000,
            'control': 0.200000,
            'mixing': 0.200000,
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
            bottleneck="sample_fetch",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
