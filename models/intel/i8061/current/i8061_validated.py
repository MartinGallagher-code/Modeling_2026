#!/usr/bin/env python3
"""
Intel 8061 Grey-Box Queueing Model
====================================

Architecture: Ford EEC Engine Controller (1978)
Custom Intel microcontroller designed exclusively for Ford's
Electronic Engine Control (EEC) system.

Features:
  - 8-bit data bus
  - 6 MHz clock
  - ~15,000 transistors (NMOS)
  - Specialized ADC and timer hardware for engine control
  - Lookup table support for fuel maps

Target CPI: 4.5
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


class I8061Model:
    """
    Intel 8061 Grey-Box Queueing Model

    Ford EEC engine controller (1978)
    - 8-bit architecture
    - 6 MHz clock
    - Custom MCU for automotive engine control
    - Integrated ADC, timers, and lookup table hardware
    """

    name = "Intel 8061"
    manufacturer = "Intel"
    year = 1978
    clock_mhz = 6.0
    transistor_count = 15000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "Basic ALU operations - 3 cycles"),
            'adc': InstructionCategory('adc', 8.0, 0, "ADC conversion and read - 8 cycles"),
            'timer': InstructionCategory('timer', 4.0, 0, "Timer operations - 4 cycles"),
            'control': InstructionCategory('control', 5.0, 0, "Branch/call operations - 5 cycles"),
            'lookup': InstructionCategory('lookup', 6.0, 0, "Table lookup for fuel maps - 6 cycles"),
        }

        # Typical: 0.40*3 + 0.10*8 + 0.15*4 + 0.20*5 + 0.15*6 = 1.20+0.80+0.60+1.00+0.90 = 4.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.40,
                'adc': 0.10,
                'timer': 0.15,
                'control': 0.20,
                'lookup': 0.15,
            }, "Typical engine control workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'adc': 0.05,
                'timer': 0.10,
                'control': 0.15,
                'lookup': 0.20,
            }, "Compute-intensive fuel calculation"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'adc': 0.10,
                'timer': 0.10,
                'control': 0.15,
                'lookup': 0.45,
            }, "Heavy table lookup workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.25,
                'adc': 0.10,
                'timer': 0.15,
                'control': 0.40,
                'lookup': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'adc': 0.15,
                'timer': 0.20,
                'control': 0.20,
                'lookup': 0.15,
            }, "Mixed sensor + control workload"),
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
