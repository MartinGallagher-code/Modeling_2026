#!/usr/bin/env python3
"""
Intel i82596 Grey-Box Queueing Model
====================================

Architecture: 32-bit Ethernet coprocessor, TCP offload
Year: 1987, Clock: 16.0 MHz

Target CPI: 3.0
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


class I82596Model:
    """
    Intel i82596 Grey-Box Queueing Model

    32-bit Ethernet coprocessor, TCP offload (1987)
    - 32-bit LAN coprocessor
    - TCP offload
    - DMA engine
    """

    name = "Intel i82596"
    manufacturer = "Intel"
    year = 1987
    clock_mhz = 16.0
    transistor_count = 120000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'packet': InstructionCategory('packet', 4.0, 0, "Packet processing"),
            'dma': InstructionCategory('dma', 3.0, 0, "DMA transfer"),
            'register': InstructionCategory('register', 1.0, 0, "Register access"),
            'memory': InstructionCategory('memory', 3.0, 0, "Buffer memory"),
            'control': InstructionCategory('control', 3.0, 0, "Flow control"),
            'protocol': InstructionCategory('protocol', 4.0, 0, "Protocol engine"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'packet': 0.3,
                'dma': 0.2,
                'register': 0.1,
                'memory': 0.2,
                'control': 0.1,
                'protocol': 0.1,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'packet': 0.4,
                'dma': 0.15,
                'register': 0.05,
                'memory': 0.15,
                'control': 0.1,
                'protocol': 0.15,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'packet': 0.2,
                'dma': 0.25,
                'register': 0.1,
                'memory': 0.3,
                'control': 0.05,
                'protocol': 0.1,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'packet': 0.25,
                'dma': 0.15,
                'register': 0.1,
                'memory': 0.15,
                'control': 0.25,
                'protocol': 0.1,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'packet': 0.25,
                'dma': 0.2,
                'register': 0.1,
                'memory': 0.2,
                'control': 0.1,
                'protocol': 0.15,
            }, "Mixed workload"),
        }

        self.corrections = {
            'packet': -0.200000,
            'dma': -0.200000,
            'register': -0.200000,
            'memory': -0.200000,
            'control': -0.200000,
            'protocol': -0.200000,
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
            bottleneck="packet_processing",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
