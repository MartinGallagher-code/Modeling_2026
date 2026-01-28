#!/usr/bin/env python3
"""
WDC65C02 Grey-Box Queueing Model
=================================

Architecture: 8-bit CMOS microprocessor (1983)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - CMOS version of 6502 with bug fixes
  - New instructions (BRA, PHX, PHY, PLX, PLY, STZ, TRB, TSB)
  - Some instructions take fewer cycles than NMOS 6502
  - Higher clock speeds possible (up to 14 MHz)
  - 8-bit data bus, 16-bit address bus
  - 2-7 cycles per instruction

Calibrated: 2026-01-28
Target CPI: ~3.2 for typical workloads (faster than 6502)
Used in: Apple IIc, Apple IIe Enhanced, embedded systems
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

        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)

    class BaseProcessorModel:
        pass


class Wdc65c02Model(BaseProcessorModel):
    """
    WDC65C02 Grey-Box Queueing Model

    Architecture: 8-bit CMOS microprocessor (1983)
    - CMOS 6502 with bug fixes and new instructions
    - Some operations optimized (fewer cycles)
    - BRA (branch always) reduces control flow overhead
    - CPI ~3.2 for typical workloads (faster than 6502's 3.5)
    """

    # Processor specifications
    name = "WDC65C02"
    manufacturer = "Western Design Center"
    year = 1983
    clock_mhz = 4.0  # Up to 14 MHz, 4 MHz typical
    transistor_count = 8000
    data_width = 8
    address_width = 16

    def __init__(self):
        # 65C02 instruction timing - slightly optimized vs 6502
        # Key improvements:
        # - Indexed addressing modes no longer have dummy cycles
        # - Read-modify-write ops on abs,X are 1 cycle faster
        # - New BRA instruction (unconditional branch) = 3 cycles
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.8, 0,
                "ALU ops - slightly faster than 6502"),
            'data_transfer': InstructionCategory('data_transfer', 3.2, 0,
                "LDA/STA - optimized indexed modes"),
            'memory': InstructionCategory('memory', 3.8, 0,
                "Memory ops - faster indexed operations"),
            'control': InstructionCategory('control', 2.8, 0,
                "Branches + BRA instruction"),
            'stack': InstructionCategory('stack', 3.2, 0,
                "Stack ops including PHX/PHY/PLX/PLY"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.15,
                'memory': 0.30,
                'control': 0.20,
                'stack': 0.10,
            }, "Typical 65C02 workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.12,
                'stack': 0.08,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.12,
                'memory': 0.20,
                'control': 0.35,
                'stack': 0.15,
            }, "Control-flow intensive"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
