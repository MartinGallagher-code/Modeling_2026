#!/usr/bin/env python3
"""
Intel 82730 Grey-Box Queueing Model
======================================

Architecture: Text Coprocessor (1983)
Display controller for text-mode rendering.

Features:
  - 16-bit data bus
  - 5 MHz clock
  - ~25,000 transistors (NMOS)
  - Hardware character rendering
  - Row-based display processing
  - Smooth scrolling and cursor support

Target CPI: 4.0
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

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)


class I82730Model:
    """
    Intel 82730 Grey-Box Queueing Model

    Text coprocessor (1983)
    - 16-bit architecture
    - 5 MHz clock
    - Hardware character rendering and scrolling
    - DMA-based display list processing
    """

    name = "Intel 82730"
    manufacturer = "Intel"
    year = 1983
    clock_mhz = 5.0
    transistor_count = 25000
    data_width = 16
    address_width = 20

    def __init__(self):
        self.instruction_categories = {
            'char_render': InstructionCategory('char_render', 3.0, 0, "Character rendering - 3 cycles"),
            'row_process': InstructionCategory('row_process', 5.0, 0, "Row-based display processing - 5 cycles"),
            'scroll': InstructionCategory('scroll', 6.0, 0, "Smooth scrolling operations - 6 cycles"),
            'cursor': InstructionCategory('cursor', 3.0, 0, "Cursor management - 3 cycles"),
            'dma': InstructionCategory('dma', 4.0, 0, "DMA display list fetch - 4 cycles"),
        }

        # Typical: 0.25*3 + 0.25*5 + 0.10*6 + 0.20*3 + 0.20*4 = 0.75+1.25+0.60+0.60+0.80 = 4.00
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'char_render': 0.25,
                'row_process': 0.25,
                'scroll': 0.10,
                'cursor': 0.20,
                'dma': 0.20,
            }, "Typical text display workload"),
            'compute': WorkloadProfile('compute', {
                'char_render': 0.40,
                'row_process': 0.30,
                'scroll': 0.05,
                'cursor': 0.10,
                'dma': 0.15,
            }, "Heavy character rendering"),
            'memory': WorkloadProfile('memory', {
                'char_render': 0.15,
                'row_process': 0.15,
                'scroll': 0.10,
                'cursor': 0.10,
                'dma': 0.50,
            }, "DMA-intensive display refresh"),
            'control': WorkloadProfile('control', {
                'char_render': 0.15,
                'row_process': 0.15,
                'scroll': 0.35,
                'cursor': 0.25,
                'dma': 0.10,
            }, "Scroll and cursor intensive"),
            'mixed': WorkloadProfile('mixed', {
                'char_render': 0.25,
                'row_process': 0.20,
                'scroll': 0.15,
                'cursor': 0.20,
                'dma': 0.20,
            }, "Mixed text editing workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories}
        )
