#!/usr/bin/env python3
"""
Intel 8008 CPU Queueing Model (1972)

THE FIRST 8-BIT MICROPROCESSOR

The 8008 was designed for the Datapoint 2200 terminal, but Datapoint
rejected it as too slow. Intel kept it and created the microprocessor
industry. Every x86 processor traces its lineage back to this chip.

Key characteristics:
- 500 kHz clock (slow even then)
- 14-bit address space (16 KB max)
- 7-level on-chip stack (major limitation)
- Multiplexed bus (needs external latches)
- Required ~20 TTL support chips

The 8008's limitations directly motivated the 8080 design (1974),
which fixed most problems and launched the microcomputer revolution.

Historical significance:
- First 8-bit microprocessor
- Ancestor of 8080 → 8086 → x86 → all modern PCs
- Register names (A,B,C,D,E,H,L) survive in x86 (AL,BL,CL,DL)

Author: Grey-Box Performance Modeling Research
Date: January 24, 2026
"""

import json
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class QueueMetrics:
    """Metrics for a single queueing stage."""
    name: str
    arrival_rate: float
    service_time: float
    utilization: float
    queue_length: float
    wait_time: float
    response_time: float

class Intel8008QueueModel:
    """Grey-box queueing model for Intel 8008."""
    
    def __init__(self, config_file: str):
        """Load configuration from JSON file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
        self._compute_service_times()
    
    def _compute_service_times(self):
        """Calculate average service time based on instruction mix."""
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Weighted average in clock states
        self.avg_service_time = (
            mix['register_ops'] * timings['register_to_register'] +
            mix['memory_ops'] * (timings['memory_read'] + timings['memory_write']) / 2 +
            mix['branch_jump'] * timings['jump_unconditional'] +
            mix['io_ops'] * timings['io_operation'] +
            mix['other'] * timings['halt']
        )
        
        # Add multiplexed bus overhead (external latch delays)
        self.bus_overhead = 1.2  # 20% overhead for multiplexed bus
        self.effective_service_time = self.avg_service_time * self.bus_overhead
    
    def _mm1_metrics(self, name: str, arrival_rate: float, 
                     service_time: float) -> QueueMetrics:
        """Calculate M/M/1 queue metrics."""
        utilization = arrival_rate * service_time
        
        if utilization >= 1.0:
            return QueueMetrics(
                name=name,
                arrival_rate=arrival_rate,
                service_time=service_time,
                utilization=1.0,
                queue_length=float('inf'),
                wait_time=float('inf'),
                response_time=float('inf')
            )
        
        queue_length = utilization / (1 - utilization)
        wait_time = service_time / (1 - utilization)
        
        return QueueMetrics(
            name=name,
            arrival_rate=arrival_rate,
            service_time=service_time,
            utilization=utilization,
            queue_length=queue_length,
            wait_time=wait_time,
            response_time=wait_time
        )
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC for given instruction arrival rate.
        
        The 8008 is simple: single execution unit, no pipeline.
        """
        # Single execution stage
        execute = self._mm1_metrics('Execute', arrival_rate, self.effective_service_time)
        
        if execute.utilization >= 1.0:
            return 0.0, [execute]
        
        # CPI is the response time
        cpi = execute.response_time
        ipc = 1.0 / cpi if cpi > 0 else 0.0
        
        return ipc, [execute]
    
    def find_bottleneck(self, arrival_rate: float) -> str:
        """Identify the bottleneck (always execution for 8008)."""
        return "Execute (single-stage, no pipeline)"
    
    def calibrate(self, measured_ipc: float, tolerance: float = 3.0) -> Dict:
        """Calibrate model to match measured IPC."""
        best_rate = 0.035
        best_error = float('inf')
        
        for rate in np.linspace(0.02, 0.06, 100):
            ipc, _ = self.predict_ipc(rate)
            error = abs(ipc - measured_ipc) / measured_ipc * 100
            if error < best_error:
                best_error = error
                best_rate = rate
        
        final_ipc, _ = self.predict_ipc(best_rate)
        
        return {
            'converged': best_error < tolerance,
            'arrival_rate': best_rate,
            'predicted_ipc': final_ipc,
            'error_percent': best_error
        }
    
    def compare_to_successors(self) -> Dict:
        """Compare 8008 to its successors."""
        return {
            '8008': {
                'year': 1972,
                'clock_mhz': 0.5,
                'address_kb': 16,
                'stack': '7 levels (on-chip)',
                'bus': 'Multiplexed (complex)',
                'ipc': 0.04,
                'mips': 0.02
            },
            '8080': {
                'year': 1974,
                'clock_mhz': 2.0,
                'address_kb': 64,
                'stack': 'In RAM (unlimited)',
                'bus': 'Separate (simpler)',
                'ipc': 0.06,
                'mips': 0.12
            },
            '8085': {
                'year': 1976,
                'clock_mhz': 5.0,
                'address_kb': 64,
                'stack': 'In RAM',
                'bus': 'Separate + on-chip clock',
                'ipc': 0.09,
                'mips': 0.45
            },
            'improvement_8008_to_8080': '6× throughput',
            'improvement_8008_to_8085': '22× throughput'
        }
    
    def get_historical_context(self) -> Dict:
        """Return historical context."""
        return {
            'origin': 'Designed for Datapoint 2200 terminal (1969-1971)',
            'rejection': 'Datapoint rejected it as too slow, took cash instead',
            'irony': 'Datapoint could have owned microprocessor rights!',
            'first_computer': 'SCELBI-8H (1974) - first advertised PC',
            'hobby_computer': 'Mark-8 (1974) - Popular Electronics',
            'legacy': 'Register names A,B,C,D,E,H,L survive in modern x86',
            'lineage': '8008 → 8080 → 8086 → 80386 → Pentium → Core i9'
        }

def main():
    """Example usage and demonstration."""
    model = Intel8008QueueModel('intel_8008_model.json')
    
    print("=" * 70)
    print("Intel 8008 (1972) - THE FIRST 8-BIT MICROPROCESSOR")
    print("=" * 70)
    print("Ancestor of all x86 processors")
    print()
    
    # Test different arrival rates
    print("Performance Analysis:")
    print("-" * 50)
    for rate in [0.02, 0.03, 0.04, 0.05]:
        ipc, metrics = model.predict_ipc(rate)
        mips = ipc * model.clock_mhz
        print(f"λ={rate:.3f}: IPC={ipc:.4f}, "
              f"ρ={metrics[0].utilization:.3f}, "
              f"MIPS={mips:.4f}")
    
    print()
    print("Comparison to Successors:")
    print("-" * 50)
    comp = model.compare_to_successors()
    for chip in ['8008', '8080', '8085']:
        c = comp[chip]
        print(f"{chip}: {c['clock_mhz']} MHz, {c['address_kb']}KB, "
              f"IPC={c['ipc']}, MIPS={c['mips']}")
    
    print()
    print(f"8008 → 8080: {comp['improvement_8008_to_8080']}")
    print(f"8008 → 8085: {comp['improvement_8008_to_8085']}")
    
    print()
    print("Historical Note:")
    print("-" * 50)
    ctx = model.get_historical_context()
    print(f"Origin: {ctx['origin']}")
    print(f"Irony: {ctx['irony']}")
    print(f"Legacy: {ctx['legacy']}")

if __name__ == "__main__":
    main()
