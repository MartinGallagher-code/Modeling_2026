#!/usr/bin/env python3
"""
HP PA-RISC 7100 Grey-Box Queueing Model
========================================

Target CPI: 1.2 (superscalar RISC, 1992)
Architecture: Superscalar RISC with 2-way issue

The PA-RISC 7100 was a high-performance RISC processor with
superscalar execution, achieving near-single-cycle throughput
for most instructions.
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

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


class HpPaRiscModel(BaseProcessorModel):
    """
    HP PA-RISC 7100 Grey-Box Queueing Model

    Target CPI: 1.2
    Calibration: Weighted sum of instruction cycles
    """

    name = "HP_PA_RISC"
    manufacturer = "HP"
    year = 1992
    clock_mhz = 100.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 0.91 (superscalar, IPC ~1.1)
        # RISC: most instructions single-cycle, dual-issue helps
        # Calculation: 0.45*0.7 + 0.20*1.1 + 0.10*0.8 + 0.15*0.9 + 0.05*1.5 + 0.02*2.5 + 0.02*0.8 + 0.01*3.0 = 0.91
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 0.70, 0, "ALU operations (dual-issue)"),
            'load': InstructionCategory('load', 1.10, 0, "Load from cache"),
            'store': InstructionCategory('store', 0.80, 0, "Store to cache"),
            'branch': InstructionCategory('branch', 0.90, 0, "Branch with prediction"),
            'multiply': InstructionCategory('multiply', 1.50, 0, "Integer multiply"),
            'divide': InstructionCategory('divide', 2.50, 0, "Integer divide"),
            'fp_ops': InstructionCategory('fp_ops', 0.80, 0, "FP operations"),
            'fp_complex': InstructionCategory('fp_complex', 3.00, 0, "FP divide/sqrt"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.45,
                'load': 0.20,
                'store': 0.10,
                'branch': 0.15,
                'multiply': 0.05,
                'divide': 0.02,
                'fp_ops': 0.02,
                'fp_complex': 0.01,
            }, "Typical RISC workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.55,
                'load': 0.10,
                'store': 0.05,
                'branch': 0.12,
                'multiply': 0.10,
                'divide': 0.03,
                'fp_ops': 0.03,
                'fp_complex': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.25,
                'load': 0.35,
                'store': 0.20,
                'branch': 0.12,
                'multiply': 0.03,
                'divide': 0.01,
                'fp_ops': 0.03,
                'fp_complex': 0.01,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.30,
                'load': 0.15,
                'store': 0.08,
                'branch': 0.35,
                'multiply': 0.04,
                'divide': 0.02,
                'fp_ops': 0.04,
                'fp_complex': 0.02,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.40,
                'load': 0.22,
                'store': 0.12,
                'branch': 0.15,
                'multiply': 0.05,
                'divide': 0.02,
                'fp_ops': 0.03,
                'fp_complex': 0.01,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.435762783399857,
            'branch': -0.2032009478237062,
            'divide': 4.999964827213707,
            'fp_complex': -1.3697286996719584,
            'fp_ops': -1.3160263767185678,
            'load': 3.033101877520287,
            'multiply': -0.7791404688919025,
            'store': -4.9999995690619246,
        }

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency=1.0,
            l1_hit_rate=0.9514,
            has_l2=True,
            l2_latency=8.0,
            l2_hit_rate=0.9138,
            dram_latency=12.0,
        )
        self.memory_categories = ['load', 'store']

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
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)
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
