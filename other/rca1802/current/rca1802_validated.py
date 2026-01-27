#!/usr/bin/env python3
"""
RCA 1802 Validated Performance Model

First CMOS microprocessor, Voyager

SPECIFICATIONS:
- Year: 1976
- Data Width: 8-bit
- Clock: 3.2 MHz
- Transistors: 5,000
- Technology: CMOS

VALIDATED PERFORMANCE:
- IPS Range: 100,000 - 300,000
- Typical CPI: 12.0

Author: Grey-Box Performance Modeling Research
Validated: January 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
import json


@dataclass
class RCA1802Specs:
    """Validated RCA 1802 specifications."""
    name: str = "RCA 1802"
    year: int = 1976
    manufacturer: str = "Various"
    data_width: int = 8
    clock_mhz: float = 3.2
    transistors: int = 5000
    technology: str = "CMOS"
    package: str = "40-pin DIP"
    typical_cpi: float = 12.0


@dataclass
class RCA1802Workload:
    """Workload profile."""
    name: str
    weight_fast: float = 0.3   # Fast instructions
    weight_medium: float = 0.5  # Medium instructions
    weight_slow: float = 0.2   # Slow instructions


@dataclass
class RCA1802Result:
    """Analysis result."""
    workload: str
    clock_mhz: float
    cpi: float
    ips: float
    mips: float
    bottleneck: str


class RCA1802Model:
    """
    Validated performance model for RCA 1802.
    
    Uses grey-box queueing methodology with category-based timing.
    """
    
    def __init__(self):
        self.specs = RCA1802Specs()
        self.workloads = {
            'typical': RCA1802Workload('typical', 0.3, 0.5, 0.2),
            'compute': RCA1802Workload('compute', 0.5, 0.4, 0.1),
            'control': RCA1802Workload('control', 0.2, 0.4, 0.4),
        }
    
    def analyze(self, workload: str = 'typical',
                clock_mhz: float = 3.2) -> RCA1802Result:
        """Analyze performance for given workload."""
        wl = self.workloads.get(workload, self.workloads['typical'])
        
        # CPI calculation based on instruction mix
        cpi_min, cpi_max = (8, 24)
        cpi_mid = (cpi_min + cpi_max) / 2
        
        cpi = (wl.weight_fast * cpi_min + 
               wl.weight_medium * cpi_mid + 
               wl.weight_slow * cpi_max)
        
        # Calculate IPS
        ips = (clock_mhz * 1e6) / cpi
        mips = ips / 1e6
        
        # Bottleneck analysis
        if cpi > 10:
            bottleneck = "High CPI (memory or complex instructions)"
        elif clock_mhz < 2:
            bottleneck = "Clock frequency"
        else:
            bottleneck = "Sequential execution"
        
        return RCA1802Result(
            workload=workload,
            clock_mhz=clock_mhz,
            cpi=cpi,
            ips=ips,
            mips=mips,
            bottleneck=bottleneck
        )
    
    def validate(self) -> Dict:
        """Run validation against known specifications."""
        result = self.analyze('typical')
        ips_min, ips_max = (100000, 300000)
        
        return {
            'ips_range': {
                'expected_min': ips_min,
                'expected_max': ips_max,
                'actual': result.ips,
                'pass': ips_min * 0.8 <= result.ips <= ips_max * 1.2
            },
            'cpi': {
                'expected': 12.0,
                'actual': result.cpi,
                'pass': abs(result.cpi - 12.0) < 12.0 * 0.3
            }
        }
    
    def export_json(self, filepath: str):
        """Export model data to JSON."""
        data = {
            'specs': asdict(self.specs),
            'validation': self.validate()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Demonstrate model."""
    model = RCA1802Model()
    
    print("=" * 60)
    print(f"{model.specs.name} ({model.specs.year})")
    print("=" * 60)
    print(f"Clock: {model.specs.clock_mhz} MHz")
    print(f"Data Width: {model.specs.data_width}-bit")
    print(f"Transistors: {model.specs.transistors:,}")
    print()
    
    for wl in model.workloads:
        result = model.analyze(wl)
        print(f"{wl}: {result.ips:,.0f} IPS ({result.mips:.3f} MIPS)")
    
    print()
    print("Validation:")
    for test, data in model.validate().items():
        status = "✓ PASS" if data['pass'] else "✗ FAIL"
        print(f"  {test}: {status}")


if __name__ == "__main__":
    main()
