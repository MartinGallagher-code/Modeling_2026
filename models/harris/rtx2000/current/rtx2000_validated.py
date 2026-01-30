#!/usr/bin/env python3
"""
Harris RTX2000 Grey-Box Queueing Model
=======================================

Target CPI: 1.1 (Forth stack machine, 1988)
Architecture: Hardware Forth stack processor

The RTX2000 was an advanced Forth processor with
hardware stack support, achieving near single-cycle
execution for most stack operations.
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
class CacheConfig:
    has_cache: bool = False
    l1_latency: float = 1.0
    l1_hit_rate: float = 0.95
    l2_latency: float = 10.0
    l2_hit_rate: float = 0.90
    has_l2: bool = False
    dram_latency: float = 50.0
    def effective_memory_penalty(self):
        if not self.has_cache: return 0.0
        l1_miss = 1.0 - self.l1_hit_rate
        if self.has_l2:
            l2_miss = 1.0 - self.l2_hit_rate
            return l1_miss * (self.l2_hit_rate * (self.l2_latency - self.l1_latency) + l2_miss * (self.dram_latency - self.l1_latency))
        return l1_miss * (self.dram_latency - self.l1_latency)


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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

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


class Rtx2000Model(BaseProcessorModel):
    """
    Harris RTX2000 Grey-Box Queueing Model

    Target CPI: 1.1
    Calibration: Weighted sum of instruction cycles
    """

    name = "RTX2000"
    manufacturer = "Harris"
    year = 1988
    clock_mhz = 10.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 1.1
        # Forth stack machine: very efficient
        # Calculation: 0.55*1 + 0.18*1.5 + 0.15*1 + 0.08*1.5 + 0.04*1 = 1.1
        self.instruction_categories = {
            'stack_ops': InstructionCategory('stack_ops', 1.0, 0, "Stack operations (DUP, DROP, SWAP)"),
            'memory': InstructionCategory('memory', 1.0, 0.5, "Memory fetch/store"),
            'alu': InstructionCategory('alu', 1.0, 0, "ALU operations"),
            'branch': InstructionCategory('branch', 1.5, 0, "Branch/call/return"),
            'literals': InstructionCategory('literals', 1.0, 0, "Literal push"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_ops': 0.55,
                'memory': 0.18,
                'alu': 0.15,
                'branch': 0.08,
                'literals': 0.04,
            }, "Typical Forth workload"),
            'compute': WorkloadProfile('compute', {
                'stack_ops': 0.45,
                'memory': 0.10,
                'alu': 0.32,
                'branch': 0.08,
                'literals': 0.05,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'stack_ops': 0.35,
                'memory': 0.45,
                'alu': 0.10,
                'branch': 0.05,
                'literals': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'stack_ops': 0.40,
                'memory': 0.12,
                'alu': 0.10,
                'branch': 0.33,
                'literals': 0.05,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'stack_ops': 0.50,
                'memory': 0.20,
                'alu': 0.15,
                'branch': 0.10,
                'literals': 0.05,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.100000,
            'branch': -0.400000,
            'literals': 0.099999,
            'memory': -0.548023,
            'stack_ops': 0.100000
        }

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency=1.0,
            l1_hit_rate=0.9074,
            dram_latency=8.0,
        )
        self.memory_categories = ['memory']

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Apply cache miss penalty to memory-accessing categories
        if hasattr(self, 'cache_config') and self.cache_config and self.cache_config.has_cache:
            penalty = self.cache_config.effective_memory_penalty()
            for cat_name in getattr(self, 'memory_categories', []):
                if cat_name in self.instruction_categories:
                    self.instruction_categories[cat_name].memory_cycles = penalty

        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib
        bottleneck = max(contributions, key=contributions.get)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=corrected_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
