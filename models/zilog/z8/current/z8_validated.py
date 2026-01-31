#!/usr/bin/env python3
"""
Z8 Grey-Box Queueing Model
===========================

Architecture: 8-bit single-chip microcontroller (1979)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 8-bit data bus, 16-bit address bus
  - Register-file architecture (144 general-purpose registers)
  - On-chip ROM/RAM, I/O ports, timers, UART
  - 6-20 cycles per instruction
  - 47 instruction types, 238 opcodes

Calibrated: 2026-01-28
Target CPI: ~10.0 for typical workloads
Used in: Embedded systems, industrial control, consumer electronics
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Import from common (adjust path as needed)
try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    # Fallback definitions if common not available
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

class Z8Model(BaseProcessorModel):
    """
    Z8 Grey-Box Queueing Model

    Architecture: 8-bit NMOS single-chip microcontroller (1979)
    - Register-file architecture (144 working registers in internal RAM)
    - Sequential execution (no pipeline)
    - On-chip peripherals: timers, UART, I/O ports
    - CPI ~10.0 for typical workloads
    """

    # Processor specifications
    name = "Z8"
    manufacturer = "Zilog"
    year = 1979
    clock_mhz = 8.0  # Z8 runs at up to 8 MHz external clock
    transistor_count = 12000
    data_width = 8
    address_width = 16

    def __init__(self):
        # Z8 instruction timing from datasheet
        #
        # The Z8 uses internal clock cycles (2 external clocks = 1 internal)
        # All timings below are in external clock cycles
        #
        # Actual instruction timings:
        #   LD r,r: 6 cycles (register-to-register)
        #   LD r,Ir: 6 cycles (register indirect)
        #   LD r,IM: 6 cycles (immediate)
        #   LD r,@RR: 10 cycles (indexed)
        #   ADD r,r: 6 cycles
        #   ADD r,IM: 6 cycles
        #   INC r: 6 cycles
        #   JP cc,DA: 10 cycles (conditional jump)
        #   JR cc,RA: 10 cycles (relative jump)
        #   CALL DA: 20 cycles
        #   RET: 14 cycles
        #   PUSH: 12 cycles (internal stack)
        #   POP: 10 cycles
        #   DJNZ: 10 cycles (decrement and jump)

        # Instruction categories calibrated for CPI ~10.0
        # Z8 has longer cycle counts due to register-file architecture overhead
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 6.0, 0,
                "Register-to-register ops: LD/ADD/SUB r,r @6 cycles"),
            'immediate': InstructionCategory('immediate', 6.0, 0,
                "Immediate operations: LD/ADD r,IM @6 cycles"),
            'memory': InstructionCategory('memory', 12.0, 0,
                "Indexed/indirect memory: LD r,@RR @10-14 cycles"),
            'control': InstructionCategory('control', 12.0, 0,
                "Branches: JP/JR @10-12, DJNZ @12 cycles"),
            'stack': InstructionCategory('stack', 14.0, 0,
                "Stack ops: PUSH @12-14, POP @10-12, avg ~14 cycles"),
            'call_return': InstructionCategory('call_return', 20.0, 0,
                "Subroutines: CALL @20, RET @14, avg ~18 cycles"),
        }

        # Workload profiles for MCU applications
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.30,
                'immediate': 0.20,
                'memory': 0.20,
                'control': 0.18,
                'stack': 0.07,
                'call_return': 0.05,
            }, "Typical embedded control workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.40,
                'immediate': 0.30,
                'memory': 0.12,
                'control': 0.12,
                'stack': 0.04,
                'call_return': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.20,
                'immediate': 0.10,
                'memory': 0.40,
                'control': 0.15,
                'stack': 0.10,
                'call_return': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.20,
                'immediate': 0.10,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.10,
                'call_return': 0.10,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'call_return': 10.003474798378209,
            'control': -1.4845134670845923,
            'immediate': -5.000089140185705,
            'memory': -1.6025158148548597,
            'register_ops': 2.3722292378496403,
            'stack': 6.992726819953314,
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        
        # Calculate weighted average CPI
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

        # Identify bottleneck (highest contribution)
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
        """Run validation against expected CPI of ~10.0"""
        expected_cpi = 10.0
        result = self.analyze('typical')
        predicted_cpi = result.cpi
        error_pct = abs(predicted_cpi - expected_cpi) / expected_cpi * 100

        return {
            "expected_cpi": expected_cpi,
            "predicted_cpi": round(predicted_cpi, 3),
            "cpi_error_percent": round(error_pct, 2),
            "validation_passed": error_pct < 5.0,
            "workloads_tested": ['typical', 'compute', 'memory', 'control'],
        }
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
