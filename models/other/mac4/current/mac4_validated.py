#!/usr/bin/env python3
"""
Bell Labs MAC-4 Grey-Box Queueing Model
=========================================

Architecture: 8-bit telecommunications MCU (1980s)
- Bell Labs proprietary design for telecom switching
- Optimized for real-time control tasks
- ~5000 transistors, 4 MHz clock
- Used in telephone switching equipment

Target CPI: 5.0
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
class Mac4Model(BaseProcessorModel):
    """Bell Labs MAC-4 telecommunications MCU"""
    name = "Bell Labs MAC-4"
    manufacturer = "Bell Labs / Western Electric"
    year = 1981
    clock_mhz = 4.0
    transistor_count = 5000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            "alu": InstructionCategory("alu", 3, 0, "ALU: ADD, SUB, logical @3 cycles"),
            "data_transfer": InstructionCategory("data_transfer", 4, 0, "Register/memory transfers @4 cycles"),
            "memory": InstructionCategory("memory", 6, 0, "Memory access @6 cycles"),
            "io": InstructionCategory("io", 7.5, 0, "Telecom I/O, line scanning @7.5 cycles"),
            "control": InstructionCategory("control", 5, 0, "Branch, call, interrupt @5 cycles"),
        }
        self.workload_profiles = {
            "typical": WorkloadProfile("typical", {
                "alu": 0.25, "data_transfer": 0.20, "memory": 0.15,
                "io": 0.20, "control": 0.20,
            }, "Typical telecom switching workload"),
            "compute": WorkloadProfile("compute", {
                "alu": 0.40, "data_transfer": 0.25, "memory": 0.15,
                "io": 0.05, "control": 0.15,
            }, "Compute-intensive"),
            "memory": WorkloadProfile("memory", {
                "alu": 0.15, "data_transfer": 0.20, "memory": 0.35,
                "io": 0.15, "control": 0.15,
            }, "Memory-intensive"),
            "control": WorkloadProfile("control", {
                "alu": 0.15, "data_transfer": 0.15, "memory": 0.15,
                "io": 0.25, "control": 0.30,
            }, "Control/IO-intensive (line scanning)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.943062,
            'control': 0.819778,
            'data_transfer': 2.634852,
            'io': -3.618580,
            'memory': -1.353170
        }

    def analyze(self, workload="typical"):
        profile = self.workload_profiles.get(workload, self.workload_profiles["typical"])
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
        return AnalysisResult.from_cpi(self.name, workload, corrected_cpi, self.clock_mhz, bottleneck, contributions, base_cpi=base_cpi, correction_delta=correction_delta)

    def validate(self):
        tests = []
        pc = 0
        result = self.analyze("typical")
        target_cpi = 5.0
        err = abs(result.cpi - target_cpi) / target_cpi * 100
        t = {"name": "CPI accuracy", "expected": target_cpi, "actual": result.cpi,
             "error_percent": err, "passed": err < 5.0}
        tests.append(t)
        if t["passed"]: pc += 1
        for wn, wl in self.workload_profiles.items():
            ws = sum(wl.category_weights.values())
            t = {"name": f"Weight sum ({wn})", "expected": 1.0,
                 "actual": round(ws, 6), "passed": abs(ws - 1.0) < 0.001}
            tests.append(t)
            if t["passed"]: pc += 1
        for wl in self.workload_profiles:
            r = self.analyze(wl)
            t = {"name": f"Valid output ({wl})", "passed": r.cpi > 0 and r.ipc > 0,
                 "actual": f"CPI={r.cpi:.3f}"}
            tests.append(t)
            if t["passed"]: pc += 1
        acc = (pc / len(tests)) * 100 if tests else 0
        return {"tests": tests, "passed": pc, "total": len(tests), "accuracy_percent": acc}

    def get_instruction_categories(self): return self.instruction_categories
    def get_workload_profiles(self): return self.workload_profiles

def create_model(): return Mac4Model()
def run_validation():
    m = Mac4Model()
    r = m.validate()
    print(f"MAC-4 Validation: {r['passed']}/{r['total']} passed ({r['accuracy_percent']:.1f}%)")
    for t in r["tests"]:
        print(f"  [{'PASS' if t['passed'] else 'FAIL'}] {t['name']}")
    return r

if __name__ == "__main__":
    run_validation()
