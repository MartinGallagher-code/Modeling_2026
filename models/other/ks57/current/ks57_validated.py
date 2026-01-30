#!/usr/bin/env python3
"""
Samsung KS57 Grey-Box Queueing Model
======================================

Architecture: 4-bit microcontroller (1982)
Queueing Model: Weighted CPI with variable instruction timing

Features:
  - Samsung first 4-bit MCU family
  - NMOS technology, 400 kHz clock
  - On-chip RAM, ROM, I/O
  - Used in Korean consumer electronics (calculators, appliances)
  - ~2500 transistors

Target CPI: 6.0 (typical 4-bit MCU)
Clock: 0.4 MHz

Calibrated: 2026-01-29
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
    base_cpi: float = 0.0
    correction_delta: float = 0.0
    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations, base_cpi=None, correction_delta=0.0):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

class BaseProcessorModel:
    """Base class for processor models"""
    name = ""
    manufacturer = ""
    year = 0
    clock_mhz = 0.0

    def analyze(self, workload='typical'):
        raise NotImplementedError

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
            params[f"cat.{c}.base_cycles"] = cat.base_cycles
        for c, v in self.corrections.items():
            params[f"cor.{c}"] = v
        return params
    def set_parameters(self, params):
        for k, v in params.items():
            if k.startswith("cat.") and k.endswith(".base_cycles"):
                c = k[4:-12]
                if c in self.instruction_categories:
                    self.instruction_categories[c].base_cycles = v
            elif k.startswith("cor."):
                c = k[4:]
                self.corrections[c] = v
    def get_parameter_bounds(self):
        bounds = {}
        for c, cat in self.instruction_categories.items():
            bounds[f"cat.{c}.base_cycles"] = (0.1, cat.base_cycles * 5)
        for c in self.corrections:
            bounds[f"cor.{c}"] = (-50, 50)
        return bounds
    def get_parameter_metadata(self):
        return {k: {"type": "category" if k.startswith("cat.") else "correction"} for k in self.get_parameters()}
    def get_instruction_categories(self):
        return self.instruction_categories
    def get_workload_profiles(self):
        return self.workload_profiles
    def validate(self):
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
class Ks57Model(BaseProcessorModel):
    """Samsung KS57 4-bit MCU Model"""
    name = "Samsung KS57"
    manufacturer = "Samsung"
    year = 1982
    clock_mhz = 0.4  # 400 kHz
    transistor_count = 2500
    data_width = 4
    address_width = 12  # 4K ROM

    def __init__(self):
        # 4-bit MCU instruction timing
        # Target CPI = 6.0
        # Calculation: 0.25*4 + 0.20*5 + 0.20*7 + 0.15*8 + 0.20*6
        # = 1.0 + 1.0 + 1.4 + 1.2 + 1.2 = 5.8
        # Adjust: 0.25*4 + 0.20*5 + 0.20*7 + 0.15*9 + 0.20*6
        # = 1.0 + 1.0 + 1.4 + 1.35 + 1.2 = 5.95 ~ 6.0
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 4, 0,
                "ALU: ADD, SUB, AND, OR operations @4 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 5, 0,
                "Transfer: Register/RAM transfers @5 cycles"),
            'memory': InstructionCategory('memory', 7, 0,
                "Memory: ROM table lookup, indirect @7 cycles"),
            'io': InstructionCategory('io', 9, 0,
                "I/O: Port read/write, display @9 cycles"),
            'control': InstructionCategory('control', 6, 0,
                "Control: Branch, jump, call @6 cycles"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25, 'data_transfer': 0.20, 'memory': 0.20,
                'io': 0.15, 'control': 0.20,
            }, "Typical 4-bit MCU workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45, 'data_transfer': 0.20, 'memory': 0.15,
                'io': 0.05, 'control': 0.15,
            }, "Compute-intensive (arithmetic)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15, 'data_transfer': 0.25, 'memory': 0.30,
                'io': 0.10, 'control': 0.20,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15, 'data_transfer': 0.15, 'memory': 0.15,
                'io': 0.25, 'control': 0.30,
            }, "Control/IO-intensive (appliance control)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 2.458136,
            'control': 1.624969,
            'data_transfer': -2.373993,
            'io': -4.375021,
            'memory': 0.957620
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            contributions[cat_name] = contrib
            base_cpi += contrib
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=corrected_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta)

    def validate(self) -> Dict[str, Any]:
        tests = []
        passed_count = 0
        result = self.analyze('typical')
        target_cpi = 6.0
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {"name": "CPI accuracy (typical)", "expected": target_cpi,
                 "actual": result.cpi, "error_percent": error_pct, "passed": error_pct < 5.0}
        tests.append(test1)
        if test1["passed"]: passed_count += 1
        for wl_name, wl in self.workload_profiles.items():
            weight_sum = sum(wl.category_weights.values())
            test = {"name": f"Weight sum ({wl_name})", "expected": 1.0,
                    "actual": round(weight_sum, 6), "passed": abs(weight_sum - 1.0) < 0.001}
            tests.append(test)
            if test["passed"]: passed_count += 1
        for cat_name, cat in self.instruction_categories.items():
            test = {"name": f"Cycle range ({cat_name})", "expected_range": [4, 9],
                    "actual": cat.total_cycles, "passed": 4 <= cat.total_cycles <= 9}
            tests.append(test)
            if test["passed"]: passed_count += 1
        for wl in self.workload_profiles:
            r = self.analyze(wl)
            test = {"name": f"CPI range ({wl})", "expected_range": [4.0, 9.0],
                    "actual": r.cpi, "passed": 4.0 <= r.cpi <= 9.0}
            tests.append(test)
            if test["passed"]: passed_count += 1
        accuracy = (passed_count / len(tests)) * 100 if tests else 0
        return {"tests": tests, "passed": passed_count, "total": len(tests), "accuracy_percent": accuracy}

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles


def create_model() -> Ks57Model:
    return Ks57Model()

def run_validation():
    model = Ks57Model()
    results = model.validate()
    print(f"Samsung KS57 Validation Results")
    print("=" * 40)
    print(f"Tests passed: {results['passed']}/{results['total']}")
    print(f"Accuracy: {results['accuracy_percent']:.1f}%")
    for test in results['tests']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  [{status}] {test['name']}")
    return results

if __name__ == "__main__":
    run_validation()
