#!/usr/bin/env python3
"""
Z80 Grey-Box Queueing Model
============================

Architecture: 8-bit microprocessor (1976)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 8-bit data bus, 16-bit address bus
  - Enhanced 8080 instruction set + extensions
  - Block transfer/search instructions (LDIR, CPIR, etc.)
  - Two register sets (main + alternate)
  - IX/IY index registers
  - 4-23 cycles per instruction

Calibrated: 2026-01-28
Target CPI: ~5.5 for typical workloads
Used in: ZX Spectrum, MSX, TRS-80, Amstrad CPC, Game Boy (modified)
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

class Z80Model(BaseProcessorModel):
    """
    Z80 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microprocessor (1976)
    - Sequential execution (no pipeline)
    - Enhanced 8080 compatible
    - Block instructions for memory/string operations
    - CPI ~5.5 for typical workloads
    """

    # Processor specifications
    name = "Z80"
    manufacturer = "Zilog"
    year = 1976
    clock_mhz = 2.5  # Original Z80 (Z80A=4MHz, Z80B=6MHz)
    transistor_count = 8500
    data_width = 8
    address_width = 16

    def __init__(self):
        # Z80 instruction timing from datasheet (T-states)
        #
        # Actual instruction timings:
        #   LD r,r: 4 cycles
        #   LD r,n: 7 cycles
        #   LD r,(HL): 7 cycles
        #   LD (HL),r: 7 cycles
        #   LD A,(nn): 13 cycles
        #   ADD A,r: 4 cycles
        #   ADD A,n: 7 cycles
        #   ADD HL,rr: 11 cycles
        #   INC r: 4 cycles
        #   JP nn: 10 cycles
        #   JR e: 12/7 cycles (taken/not taken)
        #   CALL nn: 17 cycles
        #   RET: 10 cycles
        #   PUSH: 11 cycles
        #   POP: 10 cycles
        #   LDIR: 21/16 cycles (BC!=0/BC=0)

        # Instruction categories calibrated to validation instruction_mix
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 4.0, 0,
                "ALU ops - ADD/SUB/INC/DEC register @4, immediate @7"),
            'data_transfer': InstructionCategory('data_transfer', 4.0, 0,
                "LD r,r @4, LD r,n @7 - weighted for register-heavy code"),
            'memory': InstructionCategory('memory', 5.8, 0,
                "LD r,(HL) @7, LD (HL),r @7 - (HL) most common"),
            'control': InstructionCategory('control', 5.5, 0,
                "JP @10, JR @9.5 avg, CALL/RET less frequent"),
            'stack': InstructionCategory('stack', 10.0, 0,
                "PUSH @11, POP @10"),
            'block': InstructionCategory('block', 12.0, 0,
                "LDIR/LDDR @21/16, weighted for typical use"),
        }

        # Workload profiles from validation JSON instruction_mix
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.10,
                'block': 0.05,
            }, "Typical Z80 workload (games, system software)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.12,
                'stack': 0.05,
                'block': 0.03,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'control': 0.12,
                'stack': 0.08,
                'block': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.12,
                'block': 0.05,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.304196,
            'block': 2.628901,
            'control': 3.043924,
            'data_transfer': 1.251871,
            'memory': 3.416820,
            'stack': -3.488146
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        # Apply correction terms (system identification)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        ipc = 1.0 / corrected_cpi if corrected_cpi > 0 else 0.0
        ips = self.clock_mhz * 1e6 * ipc

        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
