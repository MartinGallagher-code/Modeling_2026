#!/usr/bin/env python3
"""
DEC MicroVAX 78032 Grey-Box Queueing Model
============================================

Target CPI: 5.5 (32-bit CISC, 1984)
Architecture: First single-chip VAX implementation
Clock: 5 MHz, ~125,000 transistors

The MicroVAX 78032 was DEC's first single-chip VAX processor,
capable of running the full VMS operating system. It implemented
a subset of the VAX instruction set with microcoded execution.
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


class MicroVAX78032Model(BaseProcessorModel):
    """
    DEC MicroVAX 78032 Grey-Box Queueing Model

    Target CPI: 5.5
    Calibration: Weighted sum of instruction cycles
    """

    name = "MicroVAX 78032"
    manufacturer = "DEC"
    year = 1984
    clock_mhz = 5.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 5.5
        # First single-chip VAX, microcoded CISC, full VMS support
        # Typical: 0.365*2 + 0.200*6 + 0.200*4 + 0.100*10 + 0.050*15 + 0.085*12
        #        = 0.73 + 1.20 + 0.80 + 1.00 + 0.75 + 1.02 = 5.50
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0, "ALU register operations"),
            'memory': InstructionCategory('memory', 3.0, 3.0, "Memory load/store"),
            'control': InstructionCategory('control', 4.0, 0, "Branch and jump"),
            'string': InstructionCategory('string', 10.0, 0, "String manipulation"),
            'decimal': InstructionCategory('decimal', 15.0, 0, "Decimal arithmetic"),
            'float': InstructionCategory('float', 12.0, 0, "Floating-point operations"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.365,
                'memory': 0.200,
                'control': 0.200,
                'string': 0.100,
                'decimal': 0.050,
                'float': 0.085,
            }, "Typical VMS workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'memory': 0.12,
                'control': 0.10,
                'string': 0.05,
                'decimal': 0.08,
                'float': 0.25,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'memory': 0.40,
                'control': 0.12,
                'string': 0.15,
                'decimal': 0.05,
                'float': 0.08,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.25,
                'memory': 0.15,
                'control': 0.35,
                'string': 0.10,
                'decimal': 0.05,
                'float': 0.10,
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
    model = MicroVAX78032Model()
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
    model = MicroVAX78032Model()
    print(f"=== {model.name} ({model.year}) ===")
    print(f"Clock: {model.clock_mhz} MHz")
    print()
    for workload in ['typical', 'compute', 'memory', 'control']:
        result = model.analyze(workload)
        print(f"{workload:10s}: CPI={result.cpi:.3f}  IPC={result.ipc:.3f}  "
              f"IPS={result.ips:,.0f}  Bottleneck={result.bottleneck}")
