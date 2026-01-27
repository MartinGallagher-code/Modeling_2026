#!/usr/bin/env python3
"""
Motorola 6803 CPI Stack Model

COMPLEMENTARY APPROACH TO QUEUEING THEORY

Decomposes CPI (Cycles Per Instruction) into penalty components:
- Base CPI: Ideal execution from instruction mix


- Memory penalty: Extra cycles for memory operands



Specifications:
- Year: 1983
- Data width: 8-bit
- Clock: 1.0 MHz
- Pipeline stages: 1



Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

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
        self.mips = 1.0 * self.ipc
        
        if self.cpi_total > 0:
            self.breakdown = {
                'base': 100 * self.cpi_base / self.cpi_total,
                
                
                'memory': 100 * self.cpi_memory / self.cpi_total,
                
                
            }
            penalties = {k: v for k, v in self.breakdown.items() if k != 'base' and v > 0}
            self.bottleneck = max(penalties, key=penalties.get) if penalties else "none"


class Motorola6803CPIStackModel:
    """
    CPI Stack Model for Motorola 6803.
    
    Decomposes execution time into penalty components.
    """
    
    # Architecture constants
    CLOCK_MHZ = 1.0
    BITS = 8
    
    
    
    
    # Instruction timings (cycles)
    TIMING_ALU = 2
    TIMING_MOV = 3
    TIMING_BRANCH = 4
    TIMING_MEMORY = 4
    
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
        
        
        
        
        
        
        
        
        # Memory penalty
        extra_mem = max(0, self.TIMING_MEMORY - self.TIMING_ALU)
        result.cpi_memory = workload.memory_operand_rate * extra_mem * 0.3
        
        
        
        
        
        
        
        
        result.compute_totals()
        return result
    
    def print_result(self, result: CPIStackResult):
        """Print formatted breakdown."""
        print(f"\n{'='*55}")
        print(f"CPI STACK: Motorola 6803")
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
        print(f"\nIPC: {result.ipc:.4f}  |  MIPS: {result.mips:.3f}")


def main():
    model = Motorola6803CPIStackModel()
    
    print("\n" + "="*55)
    print("Motorola 6803 CPI STACK MODEL")
    print("="*55)
    
    for name, workload in WORKLOADS.items():
        result = model.predict(workload)
        model.print_result(result)


if __name__ == "__main__":
    main()
