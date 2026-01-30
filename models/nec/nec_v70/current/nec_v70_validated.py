#!/usr/bin/env python3
"""
NEC V70 Grey-Box Queueing Model
=================================

Architecture: 32-bit microprocessor (1987)
- NEC V60 variant with higher clock speed
- Same proprietary ISA as V60
- ~400,000 transistors, 20 MHz
- Used in NEC workstations

Target CPI: 2.8 (slightly improved over V60s 3.0)
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

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
class NecV70Model(BaseProcessorModel):
    """NEC V70 32-bit processor model"""
    name = "NEC V70"
    manufacturer = "NEC"
    year = 1987
    clock_mhz = 20.0
    transistor_count = 400000
    data_width = 32
    address_width = 32

    def __init__(self):
        # Similar to V60 but slightly improved pipeline
        # Target CPI = 2.8
        # 0.30*2 + 0.25*2 + 0.20*3.5 + 0.15*3 + 0.05*7 + 0.05*5.5
        # = 0.60 + 0.50 + 0.70 + 0.45 + 0.35 + 0.275 = 2.825
        self.instruction_categories = {
            "alu": InstructionCategory("alu", 2, 0, "ALU operations - 32-bit"),
            "data_transfer": InstructionCategory("data_transfer", 2, 0, "Data transfer (MOV)"),
            "memory": InstructionCategory("memory", 3.5, 0, "Memory operations (load/store)"),
            "control": InstructionCategory("control", 3, 0, "Control flow (BR, Bcc, JSR)"),
            "float": InstructionCategory("float", 7, 0, "Floating point (FADD, FMUL)"),
            "string": InstructionCategory("string", 5.5, 0, "String manipulation"),
        }
        self.workload_profiles = {
            "typical": WorkloadProfile("typical", {
                "alu": 0.30, "data_transfer": 0.25, "memory": 0.20,
                "control": 0.15, "float": 0.05, "string": 0.05,
            }, "Typical 32-bit workstation workload"),
            "compute": WorkloadProfile("compute", {
                "alu": 0.45, "data_transfer": 0.20, "memory": 0.15,
                "control": 0.10, "float": 0.05, "string": 0.05,
            }, "Compute-intensive"),
            "memory": WorkloadProfile("memory", {
                "alu": 0.15, "data_transfer": 0.15, "memory": 0.35,
                "control": 0.10, "float": 0.05, "string": 0.20,
            }, "Memory-intensive"),
            "control": WorkloadProfile("control", {
                "alu": 0.20, "data_transfer": 0.15, "memory": 0.15,
                "control": 0.35, "float": 0.05, "string": 0.10,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.041939,
            'control': -0.078889,
            'data_transfer': -0.050928,
            'float': -0.085745,
            'memory': -0.021391,
            'string': -0.085745
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
        return AnalysisResult.from_cpi(self.name, workload, corrected_cpi, self.clock_mhz, bottleneck, contributions,
            base_cpi=base_cpi, correction_delta=correction_delta)

    def validate(self):
        tests = []
        passed_count = 0
        result = self.analyze("typical")
        target_cpi = 2.8
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {"name": "CPI accuracy", "expected": target_cpi, "actual": result.cpi,
                 "error_percent": error_pct, "passed": error_pct < 5.0}
        tests.append(test1)
        if test1["passed"]: passed_count += 1
        for wl_name, wl in self.workload_profiles.items():
            ws = sum(wl.category_weights.values())
            t = {"name": f"Weight sum ({wl_name})", "expected": 1.0,
                 "actual": round(ws, 6), "passed": abs(ws - 1.0) < 0.001}
            tests.append(t)
            if t["passed"]: passed_count += 1
        for wl in self.workload_profiles:
            r = self.analyze(wl)
            t = {"name": f"Valid output ({wl})", "passed": r.cpi > 0 and r.ipc > 0 and r.ips > 0,
                 "actual": f"CPI={r.cpi:.3f}"}
            tests.append(t)
            if t["passed"]: passed_count += 1
        acc = (passed_count / len(tests)) * 100 if tests else 0
        return {"tests": tests, "passed": passed_count, "total": len(tests), "accuracy_percent": acc}

    def get_instruction_categories(self): return self.instruction_categories
    def get_workload_profiles(self): return self.workload_profiles

def create_model(): return NecV70Model()
def run_validation():
    m = NecV70Model()
    r = m.validate()
    p = r["passed"]
    t = r["total"]
    a = r["accuracy_percent"]
    print("NEC V70 Validation: %d/%d passed (%.1f%%)" % (p, t, a))
    for test in r["tests"]:
        status = "PASS" if test["passed"] else "FAIL"
        print("  [%s] %s" % (status, test["name"]))
    return r

if __name__ == "__main__":
    run_validation()
