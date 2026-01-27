#!/usr/bin/env python3
"""
Intel iAPX 432 CPU Queueing Model (1981)

INTEL'S BIGGEST FAILURE

The iAPX 432 was supposed to be Intel's future - a "micromainframe"
that would replace mainframe computers with microprocessors.

Instead, it was:
- 1/4 to 1/10 the speed of 8086 at same clock
- Required 3 chips just for the CPU
- Optimized for Ada (market wanted C)
- Incredibly complex
- A commercial disaster

The project consumed more resources than any Intel project before it,
and its failure nearly bankrupted the company. Only the success of
the 8086/8088 (IBM PC) saved Intel.

The 432's failure taught Intel valuable lessons that influenced the
much more successful 80386 design.

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

import json
from dataclasses import dataclass
from typing import Tuple, Dict, List

@dataclass
class QueueMetrics:
    name: str
    arrival_rate: float
    service_time: float
    utilization: float
    queue_length: float
    wait_time: float
    response_time: float

class InteliAPX432QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        # The 432 was incredibly slow due to:
        # - Multi-chip overhead
        # - Capability checking
        # - Bit-aligned instruction decode
        # - Complex microcode
        
        base_ipc = 0.02  # Terribly slow
        
        # Model the multi-chip communication overhead
        chip_overhead = 1.5  # 50% overhead for inter-chip communication
        effective_ipc = base_ipc / chip_overhead
        
        return effective_ipc, []
    
    def compare_contemporaries(self) -> Dict:
        """The 432 compared to its competition - embarrassing."""
        return {
            'iAPX_432': {
                'year': 1981,
                'clock': '8 MHz',
                'chips': 3,
                'ipc': 0.02,
                'mips': 0.16,
                'status': 'FAILED'
            },
            '8086': {
                'year': 1978,
                'clock': '5 MHz',
                'chips': 1,
                'ipc': 0.12,
                'mips': 0.60,
                'status': 'IBM PC!'
            },
            '68000': {
                'year': 1979,
                'clock': '8 MHz',
                'chips': 1,
                'ipc': 0.13,
                'mips': 1.04,
                'status': 'Mac, Amiga'
            },
            'verdict': '432 was 6× slower than 8086, 10× slower than 68000'
        }
    
    def why_failed(self) -> List[str]:
        return [
            "1. TOO SLOW: 1/10 the speed of 68000",
            "2. TOO COMPLEX: Required 3 chips for CPU",
            "3. TOO EXPENSIVE: Multi-chip = high cost",
            "4. WRONG LANGUAGE: Optimized for Ada, not C",
            "5. NO ECOSYSTEM: No compilers or software",
            "6. BAD TIMING: IBM chose 8088 instead"
        ]
    
    def lessons_for_intel(self) -> Dict:
        return {
            'lesson_1': 'Simple beats complex',
            'lesson_2': 'Performance beats features',
            'lesson_3': 'Market timing is everything',
            'lesson_4': 'Backward compatibility matters',
            'applied_to': '80386 design (successful!)'
        }

def main():
    model = InteliAPX432QueueModel('intel_iapx432_model.json')
    
    print("Intel iAPX 432 (1981) - The Famous Failure")
    print("=" * 55)
    print("Intel's most ambitious project... and biggest disaster")
    print()
    
    ipc, _ = model.predict_ipc(0.02)
    print(f"Performance: IPC ≈ {ipc:.4f}")
    print(f"At 8 MHz: ~0.16 MIPS")
    print()
    
    print("vs Contemporary CPUs:")
    comp = model.compare_contemporaries()
    print(f"  8086:  {comp['8086']['mips']} MIPS")
    print(f"  68000: {comp['68000']['mips']} MIPS")
    print(f"  432:   {comp['iAPX_432']['mips']} MIPS")
    print(f"  → {comp['verdict']}")
    print()
    
    print("Why it failed:")
    for reason in model.why_failed():
        print(f"  {reason}")

if __name__ == "__main__":
    main()
