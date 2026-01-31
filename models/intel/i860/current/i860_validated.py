#!/usr/bin/env python3
"""
I860 Grey-Box Queueing Model
=============================

Architecture: VLIW-Hybrid Superscalar (1989)
Queueing Model: Dual-issue pipeline with pipelined FP

Features:
  - Dual instruction mode (issue int AND fp simultaneously)
  - 3 branch delay slots (no interlocks)
  - Pipelined floating-point units (80 MFLOPS peak)
  - 4KB I-cache, 8KB D-cache
  - 64-bit data path
  - "Cray on a chip" - supercomputer performance when hand-tuned

Calibrated: 2026-01-28
Target CPI: ~1.2 for typical workloads
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Import from common (adjust path as needed)
try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult, CacheConfig
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

class I860Model(BaseProcessorModel):
    """
    I860 Grey-Box Queueing Model

    Architecture: VLIW-Hybrid Superscalar (1989)
    - Dual instruction mode: issue integer AND float simultaneously
    - 5-stage pipeline with 3 branch delay slots
    - 4KB I-cache, 8KB D-cache
    - Pipelined FP units (80 MFLOPS peak, ~20 MFLOPS typical)
    - No hardware interlocks - compiler/programmer handles hazards
    """

    # Processor specifications
    name = "I860"
    manufacturer = "Intel"
    year = 1989
    clock_mhz = 40.0  # Standard clock (up to 50 MHz)
    transistor_count = 1000000
    data_width = 64
    address_width = 32

    def __init__(self):
        # Pipeline configuration
        self.pipeline_depth = 5

        # Dual-issue capability (VLIW-hybrid)
        self.dual_issue = True  # Can issue int + fp simultaneously
        self.dual_issue_efficiency = 0.55  # Realistic utilization (hard to schedule)

        # Cache configuration - i860 had effective caches for its era
        self.icache_size_kb = 4
        self.icache_hit_rate = 0.975  # Good hit rate for scientific loops
        self.dcache_size_kb = 8  # 8KB D-cache per spec
        self.dcache_hit_rate = 0.94  # Scientific workloads have good locality
        self.memory_latency = 6  # ~150ns at 40 MHz, reasonable for 1989

        # Branch handling - i860 has 3 delay slots
        self.has_delayed_branch = True
        self.branch_delay_slots = 3
        self.delay_slot_fill_rate = 0.8  # Hand-tuned code fills slots well

        # Instruction categories - i860 specific timings
        # FP operations are pipelined: latency vs throughput
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1, 0, "ALU operations (single-cycle)"),
            'load': InstructionCategory('load', 1, 1, "Load from memory"),
            'store': InstructionCategory('store', 1, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 1, 0, "Branch (3 delay slots)"),
            'multiply': InstructionCategory('multiply', 3, 0, "Integer multiply (pipelined)"),
            'divide': InstructionCategory('divide', 8, 0, "Integer divide"),
            'fp_single': InstructionCategory('fp_single', 1, 0, "FP single (pipelined, 1/cycle throughput)"),
            'fp_double': InstructionCategory('fp_double', 1, 0, "FP double (pipelined, 1/cycle throughput)"),
        }

        # Workload profiles - i860 was used for FP-heavy scientific/graphics work
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30, 'load': 0.18, 'store': 0.10,
                'branch': 0.12, 'multiply': 0.05, 'divide': 0.01,
                'fp_single': 0.15, 'fp_double': 0.09,
            }, "Typical i860 workload (scientific/graphics)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.20, 'load': 0.10, 'store': 0.05,
                'branch': 0.08, 'multiply': 0.07, 'divide': 0.02,
                'fp_single': 0.28, 'fp_double': 0.20,
            }, "FP compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20, 'load': 0.35, 'store': 0.20,
                'branch': 0.12, 'multiply': 0.03, 'divide': 0.01,
                'fp_single': 0.05, 'fp_double': 0.04,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.35, 'load': 0.15, 'store': 0.10,
                'branch': 0.28, 'multiply': 0.03, 'divide': 0.01,
                'fp_single': 0.05, 'fp_double': 0.03,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.28, 'load': 0.18, 'store': 0.12,
                'branch': 0.14, 'multiply': 0.05, 'divide': 0.01,
                'fp_single': 0.12, 'fp_double': 0.10,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.28599824602750484,
            'branch': -0.7612968125987817,
            'divide': 1.0170408857715774,
            'fp_double': -0.4484960689208486,
            'fp_single': -0.11534204934631394,
            'load': -0.010878971382604805,
            'multiply': 0.3031380261015099,
            'store': -0.17146998036186986,
        }

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency=1.0,
            l1_hit_rate=0.9300,
            has_l2=True,
            l2_latency=8.0,
            l2_hit_rate=0.9990,
            dram_latency=8.0,
        )
        self.memory_categories = ['load', 'store']

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using i860 VLIW-hybrid dual-issue model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Apply cache miss penalty to memory-accessing categories
        if hasattr(self, 'cache_config') and self.cache_config and self.cache_config.has_cache:
            penalty = self.cache_config.effective_memory_penalty()
            for cat_name in getattr(self, 'memory_categories', []):
                if cat_name in self.instruction_categories:
                    self.instruction_categories[cat_name].memory_cycles = penalty


        # Base CPI starts at 1.0 for single-issue
        base_cpi = 1.0

        # Dual-issue benefit: int and fp can execute simultaneously
        # Calculate FP fraction of workload
        fp_fraction = (profile.category_weights.get('fp_single', 0) +
                       profile.category_weights.get('fp_double', 0))
        int_fraction = 1.0 - fp_fraction

        # When dual-issue is utilized, effective CPI improves
        # The benefit depends on how well int/fp instructions can be paired
        if self.dual_issue:
            # Overlap factor: how much FP work runs in parallel with int
            overlap = min(fp_fraction, int_fraction) * self.dual_issue_efficiency
            base_cpi = base_cpi - overlap  # Reduce CPI due to parallelism

        # I-cache miss penalty
        icache_miss_cpi = (1 - self.icache_hit_rate) * self.memory_latency

        # D-cache miss penalty
        load_weight = profile.category_weights.get('load', 0.18)
        store_weight = profile.category_weights.get('store', 0.10)
        mem_fraction = load_weight + store_weight
        dcache_miss_cpi = mem_fraction * (1 - self.dcache_hit_rate) * self.memory_latency

        # Branch penalty with delayed branches
        branch_weight = profile.category_weights.get('branch', 0.12)
        taken_rate = 0.6  # Fraction of branches taken

        # i860 has 3 delay slots - penalty only for unfilled slots
        unfilled_slots = self.branch_delay_slots * (1 - self.delay_slot_fill_rate)
        branch_cpi = branch_weight * taken_rate * unfilled_slots

        # Multi-cycle instructions (pipelined, so throughput is key)
        # Multiply: 3-cycle latency but fully pipelined (1/cycle throughput)
        mult_weight = profile.category_weights.get('multiply', 0)
        mult_cpi = mult_weight * 0.5  # Minimal overhead due to full pipelining

        # Divide: not pipelined, but rare in optimized i860 code
        div_weight = profile.category_weights.get('divide', 0)
        div_cpi = div_weight * (self.instruction_categories['divide'].base_cycles - 1)

        # FP operations: fully pipelined at 1/cycle throughput
        # No additional CPI penalty for sustained FP work (already in base)

        base_cpi_total = base_cpi + icache_miss_cpi + dcache_miss_cpi + branch_cpi + mult_cpi + div_cpi

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi_total + correction_delta

        # Bottleneck analysis
        penalties = {
            'icache': icache_miss_cpi,
            'dcache': dcache_miss_cpi,
            'branch': branch_cpi,
            'multiply': mult_cpi,
            'divide': div_cpi
        }
        bottleneck = max(penalties, key=penalties.get) if max(penalties.values()) > 0.05 else 'balanced'

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=penalties,
            base_cpi=base_cpi_total,
            correction_delta=correction_delta
        )
    
    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
