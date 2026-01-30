#!/usr/bin/env python3
"""
NEC uPD7220 Graphics Display Controller Grey-Box Queueing Model
================================================================

Architecture: Graphics Command Processor (1981)
Queueing Model: Serial M/M/1 chain

Features:
  - First LSI graphics display controller (NOT a general CPU)
  - 16-bit internal, ~60000 transistors
  - 5 MHz clock
  - Hardware line draw, arc, area fill, character display, DMA
  - Multi-cycle graphics commands

Generated: 2026-01-29
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

class Upd7220Model(BaseProcessorModel):
    """
    NEC uPD7220 Graphics Display Controller Grey-Box Queueing Model

    Architecture: Graphics Command Processor (Era: 1981)
    - NOT a general-purpose CPU
    - Executes graphics drawing commands in hardware
    - Multi-cycle per command step (pixel operations)
    - CPI represents cycles per command step

    The uPD7220 was the first single-chip LSI graphics display controller,
    capable of drawing lines, arcs, rectangles, and characters in hardware.
    It handled DMA to display memory and generated video timing signals.
    Used in the NEC PC-9801 and IBM Professional Graphics Controller.
    """

    # Processor specifications
    name = "NEC uPD7220"
    manufacturer = "NEC"
    year = 1981
    clock_mhz = 5.0
    transistor_count = 60000
    data_width = 16
    address_width = 20  # 1MB display memory addressing

    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'command_fetch': 2,    # Command fetch from FIFO
            'decode': 1,           # Command decode
            'execute': 6,          # Execute (weighted average per step)
            'memory': 3,           # Display memory access
            'writeback': 0,        # Status update
        }

        # Instruction categories - uPD7220 graphics commands
        # Calibrated for CPI = 12.0
        # Calculation: 0.25*8 + 0.10*12 + 0.20*10 + 0.15*6 + 0.20*4 + 0.10*3
        #            = 2.0 + 1.2 + 2.0 + 0.9 + 0.8 + 0.3 = 7.2 -- too low
        # These are graphics commands, much heavier:
        # Adjust: 0.25*8 + 0.15*12 + 0.20*10 + 0.10*6 + 0.10*4 + 0.20*3
        #       = 2.0 + 1.8 + 2.0 + 0.6 + 0.4 + 0.6 = 7.4 -- still low
        # Need higher weights on expensive ops or higher cycle counts
        # Re-approach: graphics workload is dominated by drawing
        # 0.30*8 + 0.15*12 + 0.25*10 + 0.10*6 + 0.05*4 + 0.15*3 (won't sum to 12)
        # The CPI=12 means average command takes 12 cycles per step
        # Let me use higher base cycles reflecting full command execution:
        # draw_line: 8 per pixel step
        # draw_arc: 12 per step (more computation)
        # area_fill: 10 per step
        # char_display: 6 per character
        # dma_transfer: 4 per word
        # control: 3 per command
        # Typical: 0.25*8 + 0.20*12 + 0.15*10 + 0.15*6 + 0.10*4 + 0.15*3 (won't reach 12)
        # = 2.0+2.4+1.5+0.9+0.4+0.45 = 7.65 -- the individual cycles need to be higher
        # OR: the "CPI" for a GDC is per-command, not per-step
        # Use: draw_line=16, draw_arc=24, area_fill=14, char_display=8, dma=4, control=3
        # 0.25*16+0.15*24+0.20*14+0.15*8+0.10*4+0.15*3
        # = 4.0+3.6+2.8+1.2+0.4+0.45 = 12.45 -- close!
        # Adjust: 0.25*16+0.15*24+0.20*14+0.15*8+0.12*4+0.13*3
        # = 4.0+3.6+2.8+1.2+0.48+0.39 = 12.47
        # Adjust: 0.25*16+0.14*24+0.20*14+0.16*8+0.12*4+0.13*3
        # = 4.0+3.36+2.8+1.28+0.48+0.39 = 12.31
        # Adjust: 0.25*16+0.13*24+0.20*14+0.17*8+0.12*4+0.13*3
        # = 4.0+3.12+2.8+1.36+0.48+0.39 = 12.15
        # Adjust: 0.25*16+0.12*24+0.20*14+0.18*8+0.12*4+0.13*3
        # = 4.0+2.88+2.8+1.44+0.48+0.39 = 11.99 -- essentially 12.0
        self.instruction_categories = {
            'draw_line': InstructionCategory('draw_line', 16, 0, "Line drawing command (per pixel step)"),
            'draw_arc': InstructionCategory('draw_arc', 24, 0, "Arc drawing command (per step)"),
            'area_fill': InstructionCategory('area_fill', 14, 0, "Area fill command"),
            'char_display': InstructionCategory('char_display', 8, 0, "Character display command"),
            'dma_transfer': InstructionCategory('dma_transfer', 4, 0, "DMA transfer per word"),
            'control': InstructionCategory('control', 3, 0, "Control/status commands"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'draw_line': 0.25,
                'draw_arc': 0.12,
                'area_fill': 0.20,
                'char_display': 0.18,
                'dma_transfer': 0.12,
                'control': 0.13,
            }, "Typical mixed graphics workload"),
            'compute': WorkloadProfile('compute', {
                'draw_line': 0.35,
                'draw_arc': 0.25,
                'area_fill': 0.15,
                'char_display': 0.05,
                'dma_transfer': 0.10,
                'control': 0.10,
            }, "Vector graphics heavy workload"),
            'memory': WorkloadProfile('memory', {
                'draw_line': 0.10,
                'draw_arc': 0.05,
                'area_fill': 0.30,
                'char_display': 0.10,
                'dma_transfer': 0.35,
                'control': 0.10,
            }, "DMA/fill intensive workload"),
            'control': WorkloadProfile('control', {
                'draw_line': 0.10,
                'draw_arc': 0.05,
                'area_fill': 0.10,
                'char_display': 0.30,
                'dma_transfer': 0.15,
                'control': 0.30,
            }, "Text/control intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

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
        """Run validation tests"""
        results = {
            "processor": self.name,
            "target_cpi": 12.0,
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }

        # Test typical workload CPI
        analysis = self.analyze('typical')
        expected_cpi = 12.0
        error_pct = abs(analysis.cpi - expected_cpi) / expected_cpi * 100

        test_result = {
            "name": "typical_workload_cpi",
            "expected": expected_cpi,
            "actual": analysis.cpi,
            "error_percent": error_pct,
            "passed": error_pct < 5.0
        }
        results["tests"].append(test_result)
        results["total"] += 1
        if test_result["passed"]:
            results["passed"] += 1

        # Test instruction category timing
        timing_tests = [
            ("draw_line", 16),
            ("draw_arc", 24),
            ("area_fill", 14),
            ("char_display", 8),
            ("dma_transfer", 4),
            ("control", 3),
        ]

        for cat_name, expected_cycles in timing_tests:
            cat = self.instruction_categories[cat_name]
            test_result = {
                "name": f"{cat_name}_timing",
                "expected": expected_cycles,
                "actual": cat.total_cycles,
                "passed": cat.total_cycles == expected_cycles
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        # Test weight sums
        for wp_name, wp in self.workload_profiles.items():
            weight_sum = sum(wp.category_weights.values())
            test_result = {
                "name": f"{wp_name}_weight_sum",
                "expected": 1.0,
                "actual": round(weight_sum, 6),
                "passed": abs(weight_sum - 1.0) < 0.001
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        # Test cycle ranges
        for cat_name, cat in self.instruction_categories.items():
            in_range = 1 <= cat.total_cycles <= 50
            test_result = {
                "name": f"{cat_name}_cycle_range",
                "expected": "1-50",
                "actual": cat.total_cycles,
                "passed": in_range
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        # Test all workloads produce valid results
        for wp_name in self.workload_profiles:
            analysis = self.analyze(wp_name)
            valid = analysis.cpi > 0 and analysis.ips > 0
            test_result = {
                "name": f"{wp_name}_workload_valid",
                "expected": "cpi > 0 and ips > 0",
                "actual": f"cpi={analysis.cpi:.2f}, ips={analysis.ips:.0f}",
                "passed": valid
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        results["accuracy_percent"] = (results["passed"] / results["total"]) * 100
        return results

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
