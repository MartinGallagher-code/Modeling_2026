#!/usr/bin/env python3
"""
Stanford MIPS Grey-Box Queueing Model
======================================

Architecture: 32-bit RISC (1983)
Queueing Model: 5-stage pipeline with delayed branches

Features:
  - Academic RISC processor from Stanford (Hennessy)
  - 5-stage pipeline (IF, ID, EX, MEM, WB)
  - Goal of single-cycle execution
  - 32 general-purpose registers
  - Delayed branches (1 delay slot)
  - Load/store architecture
  - Precursor to MIPS R2000 (1986)

Date: 2026-01-29
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
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi,
                       correction_delta=correction_delta)

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

class StanfordMipsModel(BaseProcessorModel):
    """
    Stanford MIPS Grey-Box Queueing Model

    Architecture: Original MIPS Processor (Stanford, 1983)
    - 5-stage pipeline (IF, ID, EX, MEM, WB)
    - Single-cycle ALU operations (design goal)
    - Load: 1 cycle (pipelined, no stall if scheduled properly)
    - Store: 1 cycle (pipelined)
    - Branch: 1 cycle (with delay slot always filled)
    - 32 general-purpose registers
    - Hardwired control (no microcode)
    - Interlocked pipeline

    Key innovations over Berkeley RISC:
    - 5-stage pipeline vs 2-3 stage
    - Software scheduling of load delay slots
    - More aggressive pipelining
    - Target CPI: ~1.2 (accounting for hazards)
    """

    # Processor specifications
    name = "Stanford MIPS"
    manufacturer = "Stanford University"
    year = 1983
    clock_mhz = 2.0  # 2 MHz (research chip)
    transistor_count = 25000  # Approximate
    data_width = 32
    address_width = 32

    def __init__(self):
        # Stanford MIPS aimed for single-cycle execution
        # Target CPI: ~1.2 (accounting for realistic hazards and memory)
        # Calculation: 0.50*1 + 0.15*1.5 + 0.10*1 + 0.15*1.5 + 0.10*1 = 1.15
        # With some load interlock stalls: ~1.2
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU ops: ADD/SUB/AND/OR/XOR/SLT @1 cycle"),
            'load': InstructionCategory('load', 1.5, 0, "Load: LW/LH/LB @1.5 cycles (load delay slot)"),
            'store': InstructionCategory('store', 1.0, 0, "Store: SW/SH/SB @1 cycle (pipelined)"),
            'branch': InstructionCategory('branch', 1.5, 0, "Branch: BEQ/BNE @1.5 cycles (delay slot)"),
            'jump': InstructionCategory('jump', 1.0, 0, "Jump: J/JAL/JR @1 cycle (delay slot filled)"),
        }

        # Pipeline configuration
        self.pipeline_stages = 5
        self.has_delayed_branch = True
        self.branch_delay_slots = 1
        self.load_delay_slots = 1  # Software-scheduled
        self.general_registers = 32
        self.has_interlocks = True

        # Workload profiles calibrated for CPI ~1.2
        # Stanford MIPS benefits from aggressive pipelining
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.50,      # High ALU percentage (RISC design)
                'load': 0.15,     # Loads with possible stalls
                'store': 0.10,    # Stores (pipelined)
                'branch': 0.15,   # Branches (delay slot)
                'jump': 0.10,     # Jumps/calls
            }, "Typical Stanford MIPS workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.65,
                'load': 0.10,
                'store': 0.05,
                'branch': 0.12,
                'jump': 0.08,
            }, "Compute-intensive (ALU-heavy)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.35,
                'load': 0.25,
                'store': 0.18,
                'branch': 0.12,
                'jump': 0.10,
            }, "Memory-intensive (many loads/stores)"),
            'control': WorkloadProfile('control', {
                'alu': 0.40,
                'load': 0.10,
                'store': 0.05,
                'branch': 0.30,
                'jump': 0.15,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.48,
                'load': 0.17,
                'store': 0.10,
                'branch': 0.15,
                'jump': 0.10,
            }, "Mixed general workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.477069,
            'branch': -0.204650,
            'jump': 0.108140,
            'load': 2.471699,
            'store': -2.623371
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using pipelined execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
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

        ipc = 1.0 / corrected_cpi
        ips = self.clock_mhz * 1e6 * ipc

        # Identify bottleneck
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
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: CPI should be ~1.2 (near single-cycle goal)
        result = self.analyze('typical')
        target_cpi = 1.2
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 1.2",
            "expected": target_cpi,
            "actual": round(result.cpi, 3),
            "error_percent": round(error, 2),
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: CPI should be < 1.5 (RISC single-cycle goal)
        test2 = {
            "name": "Stanford MIPS CPI < 1.5",
            "expected": "< 1.5",
            "actual": round(result.cpi, 3),
            "passed": result.cpi < 1.5
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Comparable to Berkeley RISC II (CPI ~1.2)
        risc2_cpi = 1.2
        difference = abs(result.cpi - risc2_cpi) / risc2_cpi * 100
        test3 = {
            "name": "Comparable to Berkeley RISC II",
            "expected": "within 10% of 1.2",
            "actual": f"CPI={result.cpi:.3f} ({difference:.1f}% difference)",
            "passed": difference < 10.0
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: Much faster than VAX (CPI ~10)
        vax_cpi = 10.0
        speedup = vax_cpi / result.cpi
        test4 = {
            "name": "Speedup vs VAX 11/780",
            "expected": "> 6x",
            "actual": f"{speedup:.1f}x",
            "passed": speedup > 6.0
        }
        tests.append(test4)
        if test4["passed"]: passed += 1

        # Test 5: Workload weight sums
        for wl_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            test = {
                "name": f"Weight sum ({wl_name})",
                "expected": 1.0,
                "actual": round(weight_sum, 3),
                "passed": abs(weight_sum - 1.0) < 0.001
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 6: ALU ops single-cycle
        test6 = {
            "name": "ALU single-cycle",
            "expected": 1.0,
            "actual": self.instruction_categories['alu'].total_cycles,
            "passed": self.instruction_categories['alu'].total_cycles == 1.0
        }
        tests.append(test6)
        if test6["passed"]: passed += 1

        # Test 7: Store single-cycle (pipelined)
        test7 = {
            "name": "Store single-cycle (pipelined)",
            "expected": 1.0,
            "actual": self.instruction_categories['store'].total_cycles,
            "passed": self.instruction_categories['store'].total_cycles == 1.0
        }
        tests.append(test7)
        if test7["passed"]: passed += 1

        # Test 8: 5-stage pipeline
        test8 = {
            "name": "5-stage pipeline",
            "expected": 5,
            "actual": self.pipeline_stages,
            "passed": self.pipeline_stages == 5
        }
        tests.append(test8)
        if test8["passed"]: passed += 1

        # Test 9: 32 registers
        test9 = {
            "name": "32 general-purpose registers",
            "expected": 32,
            "actual": self.general_registers,
            "passed": self.general_registers == 32
        }
        tests.append(test9)
        if test9["passed"]: passed += 1

        accuracy = (passed / len(tests)) * 100 if tests else 0
        return {
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "accuracy_percent": round(accuracy, 1)
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles

    def compare_to_risc(self) -> Dict[str, Any]:
        """Compare Stanford MIPS to Berkeley RISC processors"""
        mips_result = self.analyze('typical')

        return {
            "stanford_mips": {
                "cpi": round(mips_result.cpi, 3),
                "clock_mhz": self.clock_mhz,
                "mips": round(self.clock_mhz / mips_result.cpi, 2),
                "pipeline_stages": self.pipeline_stages,
                "registers": self.general_registers,
                "year": 1983
            },
            "berkeley_risc1": {
                "cpi": 1.3,
                "clock_mhz": 4.0,
                "mips": round(4.0 / 1.3, 2),
                "pipeline_stages": 2,
                "registers": 78,
                "year": 1982
            },
            "berkeley_risc2": {
                "cpi": 1.2,
                "clock_mhz": 3.0,
                "mips": round(3.0 / 1.2, 2),
                "pipeline_stages": 3,
                "registers": 138,
                "year": 1983
            },
            "key_differences": {
                "pipeline": "MIPS: 5-stage (deeper), RISC: 2-3 stage",
                "registers": "MIPS: 32 flat, RISC: register windows",
                "approach": "MIPS: software scheduling, RISC: register windows",
                "descendants": "MIPS -> R2000, RISC -> SPARC"
            }
        }


# Convenience function for quick analysis
def analyze_mips(workload: str = 'typical') -> AnalysisResult:
    """Quick analysis function"""
    model = StanfordMipsModel()
    return model.analyze(workload)


def validate() -> Dict[str, Any]:
    """Run validation and return results"""
    model = StanfordMipsModel()
    return model.validate()


if __name__ == "__main__":
    model = StanfordMipsModel()

    print("=" * 60)
    print("Stanford MIPS Grey-Box Queueing Model")
    print("=" * 60)
    print(f"\nProcessor: {model.name}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"Transistors: {model.transistor_count:,}")
    print(f"Pipeline stages: {model.pipeline_stages}")
    print(f"Registers: {model.general_registers}")

    print("\n" + "-" * 60)
    print("Instruction Categories:")
    print("-" * 60)
    for name, cat in model.instruction_categories.items():
        print(f"  {name:10s}: {cat.total_cycles:.1f} cycles - {cat.description}")

    print("\n" + "-" * 60)
    print("Workload Analysis:")
    print("-" * 60)
    for wl_name in model.workload_profiles:
        result = model.analyze(wl_name)
        print(f"  {wl_name:12s}: CPI={result.cpi:.3f}, IPC={result.ipc:.3f}, "
              f"MIPS={result.ips/1e6:.2f}, bottleneck={result.bottleneck}")

    print("\n" + "-" * 60)
    print("Comparison to Berkeley RISC:")
    print("-" * 60)
    comparison = model.compare_to_risc()
    print(f"  Stanford MIPS: CPI={comparison['stanford_mips']['cpi']}, "
          f"MIPS={comparison['stanford_mips']['mips']}")
    print(f"  Berkeley RISC I: CPI={comparison['berkeley_risc1']['cpi']}, "
          f"MIPS={comparison['berkeley_risc1']['mips']}")
    print(f"  Berkeley RISC II: CPI={comparison['berkeley_risc2']['cpi']}, "
          f"MIPS={comparison['berkeley_risc2']['mips']}")

    print("\n" + "-" * 60)
    print("Validation Results:")
    print("-" * 60)
    validation = model.validate()
    for test in validation["tests"]:
        status = "PASS" if test["passed"] else "FAIL"
        print(f"  [{status}] {test['name']}: expected {test['expected']}, got {test['actual']}")

    print(f"\nOverall: {validation['passed']}/{validation['total']} tests passed "
          f"({validation['accuracy_percent']}%)")
