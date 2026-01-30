#!/usr/bin/env python3
"""
Apollo DN300 PRISM Grey-Box Queueing Model
============================================

Target CPI: 4.5 (32-bit, 68000-derived workstation, 1983)
Architecture: 68000-derived workstation processor
Clock: 10 MHz, ~100,000 transistors

The Apollo DN300 used a 68000-derived processor for high-performance
graphics workstations, featuring pipelined execution with dedicated
graphics processing capabilities.
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
    def total_cycles(self):
        return self.base_cycles + self.memory_cycles


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
    pass


class ApolloDN300Model(BaseProcessorModel):
    """
    Apollo DN300 PRISM Grey-Box Queueing Model

    Target CPI: 4.5
    Calibration: Weighted sum of instruction cycles
    """

    name = "Apollo DN300 PRISM"
    manufacturer = "Apollo Computer"
    year = 1983
    clock_mhz = 10.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 4.5
        # 68000-derived workstation with graphics support
        # Typical: 0.350*2 + 0.2533*5 + 0.200*4 + 0.080*10 + 0.1167*8
        #        = 0.700 + 1.267 + 0.800 + 0.800 + 0.933 = 4.500
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0, "ALU register operations"),
            'memory': InstructionCategory('memory', 2.0, 3.0, "Memory load/store"),
            'control': InstructionCategory('control', 4.0, 0, "Branch and jump"),
            'float': InstructionCategory('float', 10.0, 0, "Floating-point operations"),
            'graphics': InstructionCategory('graphics', 8.0, 0, "Graphics operations"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.350,
                'memory': 0.2533,
                'control': 0.200,
                'float': 0.080,
                'graphics': 0.1167,
            }, "Typical workstation workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.35,
                'memory': 0.15,
                'control': 0.12,
                'float': 0.28,
                'graphics': 0.10,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'memory': 0.40,
                'control': 0.15,
                'float': 0.10,
                'graphics': 0.15,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.25,
                'memory': 0.15,
                'control': 0.35,
                'float': 0.10,
                'graphics': 0.15,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
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


def validate():
    model = ApolloDN300Model()
    results = {}
    for workload in ['typical', 'compute', 'memory', 'control']:
        result = model.analyze(workload)
        results[workload] = {
            'cpi': result.cpi,
            'ipc': result.ipc,
            'ips': result.ips,
            'bottleneck': result.bottleneck,
        }
    return results


if __name__ == '__main__':
    model = ApolloDN300Model()
    print(f"=== {model.name} ({model.year}) ===")
    print(f"Clock: {model.clock_mhz} MHz")
    print()
    for workload in ['typical', 'compute', 'memory', 'control']:
        result = model.analyze(workload)
        print(f"{workload:10s}: CPI={result.cpi:.3f}  IPC={result.ipc:.3f}  "
              f"IPS={result.ips:,.0f}  Bottleneck={result.bottleneck}")
