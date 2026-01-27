#!/usr/bin/env python3
"""
Intel 80287 Validated Performance Model

FPU coprocessor for 80286

SPECIFICATIONS:
- Year: 1983
- Data Width: 80-bit
- Clock: 8.0 MHz
- Transistors: 45,000
- Technology: NMOS

VALIDATED PERFORMANCE:
- IPS Range: 50,000 - 150,000
- Typical CPI: 100.0

Author: Grey-Box Performance Modeling Research
Validated: January 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
import json


@dataclass
class I80287Specs:
    """Validated Intel 80287 specifications."""
    name: str = "Intel 80287"
    year: int = 1983
    manufacturer: str = "Various"
    data_width: int = 80
    clock_mhz: float = 8.0
    transistors: int = 45000
    technology: str = "NMOS"
    package: str = "40-pin DIP"
    typical_cpi: float = 100.0


@dataclass
class I80287Workload:
    """Workload profile."""
    name: str
    weight_fast: float = 0.3   # Fast instructions
    weight_medium: float = 0.5  # Medium instructions
    weight_slow: float = 0.2   # Slow instructions


@dataclass
class I80287Result:
    """Analysis result."""
    workload: str
    clock_mhz: float
    cpi: float
    ips: float
    mips: float
    bottleneck: str


class I80287Model:
    """
    Validated performance model for Intel 80287.
    
    Uses grey-box queueing methodology with category-based timing.
    """
    
    def __init__(self):
        self.specs = I80287Specs()
        self.workloads = {
            'typical': I80287Workload('typical', 0.3, 0.5, 0.2),
            'compute': I80287Workload('compute', 0.5, 0.4, 0.1),
            'control': I80287Workload('control', 0.2, 0.4, 0.4),
        }
    
    def analyze(self, workload: str = 'typical',
                clock_mhz: float = 8.0) -> I80287Result:
        """Analyze performance for given workload."""
        wl = self.workloads.get(workload, self.workloads['typical'])
        
        # CPI calculation based on instruction mix
        cpi_min, cpi_max = (50, 200)
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
        
        return I80287Result(
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
        ips_min, ips_max = (50000, 150000)
        
        return {
            'ips_range': {
                'expected_min': ips_min,
                'expected_max': ips_max,
                'actual': result.ips,
                'pass': ips_min * 0.8 <= result.ips <= ips_max * 1.2
            },
            'cpi': {
                'expected': 100.0,
                'actual': result.cpi,
                'pass': abs(result.cpi - 100.0) < 100.0 * 0.3
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
    model = I80287Model()
    
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
