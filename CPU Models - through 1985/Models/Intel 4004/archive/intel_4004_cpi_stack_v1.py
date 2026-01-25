#!/usr/bin/env python3
"""
Intel 4004 CPI Stack Model - ORIGINAL VERSION (ARCHIVED)

================================================================================
DEPRECATED: This is the original simplified model retained for historical
comparison. For validated, accurate modeling, use:

    from intel_4004_validated import Intel4004Model

See comparison below:

    Metric      | Original  | Validated | Expected
    ------------|-----------|-----------|------------
    CPI (clocks)| ~8.6      | 10.0      | 8-16
    IPC         | ~0.12     | 0.10      | 0.0625-0.125
    IPS         | ~86,000   | 74,074    | 46,250-92,500

The validated model includes:
- Complete 46-instruction timing database
- 1-word vs 2-word instruction distinction
- Machine cycle timing (8 clocks = 10.8 µs)
- BCD addition benchmark validation
- Calculator workload profile
================================================================================

COMPLEMENTARY APPROACH TO QUEUEING THEORY

Decomposes CPI (Cycles Per Instruction) into penalty components:
- Base CPI: Ideal execution from instruction mix
- Memory penalty: Extra cycles for memory operands

Specifications:
- Year: 1971
- Data width: 4-bit
- Clock: 0.74 MHz (740 kHz)
- Pipeline stages: 1

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
Status: ARCHIVED - See intel_4004_validated.py for current version
"""

import warnings

# Issue deprecation warning on import
warnings.warn(
    "intel_4004_cpi_stack_v1.py is deprecated. "
    "Use intel_4004_validated.py for accurate, validated modeling.",
    DeprecationWarning,
    stacklevel=2
)

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Workload:
    """Workload characteristics for CPI analysis."""
    name: str = "typical"
    mix_alu: float = 0.35
    mix_mov: float = 0.25
    mix_branch: float = 0.15
    mix_memory: float = 0.20
    mix_other: float = 0.05
    branch_taken_rate: float = 0.60
    memory_operand_rate: float = 0.40
    
    def validate(self):
        total = self.mix_alu + self.mix_mov + self.mix_branch + self.mix_memory + self.mix_other
        assert abs(total - 1.0) < 0.01, f"Mix sums to {total}, not 1.0"


WORKLOADS = {
    "typical": Workload(),
    "compute": Workload(name="compute", mix_alu=0.50, mix_mov=0.20, mix_branch=0.10, mix_memory=0.15, mix_other=0.05),
    "memory": Workload(name="memory", mix_alu=0.20, mix_mov=0.15, mix_branch=0.10, mix_memory=0.50, mix_other=0.05),
    "control": Workload(name="control", mix_alu=0.25, mix_mov=0.20, mix_branch=0.35, mix_memory=0.15, mix_other=0.05),
}


@dataclass
class CPIStackResult:
    """CPI breakdown result."""
    cpi_base: float = 0.0
    cpi_memory: float = 0.0
    cpi_total: float = 0.0
    ipc: float = 0.0
    mips: float = 0.0
    bottleneck: str = ""
    breakdown: Dict[str, float] = field(default_factory=dict)
    
    def compute_totals(self):
        self.cpi_total = self.cpi_base + self.cpi_memory
        self.ipc = 1.0 / self.cpi_total if self.cpi_total > 0 else 0
        self.mips = 0.74 * self.ipc
        
        if self.cpi_total > 0:
            self.breakdown = {
                'base': 100 * self.cpi_base / self.cpi_total,
                'memory': 100 * self.cpi_memory / self.cpi_total,
            }
            penalties = {k: v for k, v in self.breakdown.items() if k != 'base' and v > 0}
            self.bottleneck = max(penalties, key=penalties.get) if penalties else "none"


class Intel4004CPIStackModel:
    """
    CPI Stack Model for Intel 4004 (ORIGINAL - SIMPLIFIED).
    
    DEPRECATED: Use Intel4004Model from intel_4004_validated.py instead.
    
    This simplified model doesn't properly account for:
    - 1-word vs 2-word instruction distinction
    - Correct machine cycle timing (8 clocks per cycle)
    - The 46-instruction set with specific timings
    """
    
    # Architecture constants
    CLOCK_MHZ = 0.74
    BITS = 4
    
    # SIMPLIFIED instruction timings (clock cycles)
    # Note: Original 4004 uses machine cycles (8 clocks each)
    TIMING_ALU = 8       # Actually correct for 1-word
    TIMING_MOV = 8       # Actually correct for 1-word
    TIMING_BRANCH = 12   # Should be 16 for 2-word jumps
    TIMING_MEMORY = 8    # Actually correct for 1-word
    
    def predict(self, workload: Workload = None) -> CPIStackResult:
        """Predict CPI with full breakdown."""
        workload = workload or WORKLOADS["typical"]
        workload.validate()
        
        result = CPIStackResult()
        
        # Base CPI from instruction mix
        result.cpi_base = (
            workload.mix_alu * self.TIMING_ALU +
            workload.mix_mov * self.TIMING_MOV +
            workload.mix_branch * self.TIMING_BRANCH +
            workload.mix_memory * self.TIMING_MEMORY +
            workload.mix_other * 5
        )
        
        # Memory penalty (minimal for 4004)
        extra_mem = max(0, self.TIMING_MEMORY - self.TIMING_ALU)
        result.cpi_memory = workload.memory_operand_rate * extra_mem * 0.3
        
        result.compute_totals()
        return result
    
    def print_result(self, result: CPIStackResult):
        """Print formatted breakdown."""
        print(f"\n{'='*55}")
        print(f"CPI STACK: Intel 4004 (ORIGINAL - ARCHIVED)")
        print(f"{'='*55}")
        
        components = [
            ('Base (ideal)', 'base', result.cpi_base),
            ('Memory', 'memory', result.cpi_memory),
        ]
        
        print(f"\n{'Component':<14} {'CPI':>7} {'%':>6}  Bar")
        print("-" * 50)
        
        max_pct = max(result.breakdown.values()) if result.breakdown else 1
        for item in components:
            if item and len(item) == 3:
                label, key, cpi = item
                if cpi > 0:
                    pct = result.breakdown.get(key, 0)
                    bar = '█' * int(25 * pct / max_pct) if max_pct > 0 else ''
                    marker = " ←" if key == result.bottleneck and key != 'base' else ""
                    print(f"{label:<14} {cpi:>7.2f} {pct:>5.1f}%  {bar}{marker}")
        
        print("-" * 50)
        print(f"{'TOTAL':<14} {result.cpi_total:>7.2f} {'100.0':>5}%")
        print(f"\nIPC: {result.ipc:.4f}  |  MIPS: {result.mips:.4f}")
        print(f"\n⚠️  WARNING: This is the archived model. Results may be less accurate.")


def main():
    print("\n" + "="*60)
    print("Intel 4004 CPI STACK MODEL - ORIGINAL VERSION (ARCHIVED)")
    print("="*60)
    print("⚠️  DEPRECATED: Use intel_4004_validated.py for accurate results")
    print("="*60)
    
    model = Intel4004CPIStackModel()
    
    for name, workload in WORKLOADS.items():
        result = model.predict(workload)
        model.print_result(result)


if __name__ == "__main__":
    main()
