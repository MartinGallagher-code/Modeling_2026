# Modeling_2026: Grey-Box Queueing Performance Models

**63 Pre-1986 Microprocessor Performance Models**

## Overview

This project implements grey-box queueing theory performance models for historical microprocessors from 1971-1987. Each model uses **category-based timing** with M/M/1 queueing analysis to predict Instructions Per Second (IPS), Cycles Per Instruction (CPI), and identify performance bottlenecks.

## Methodology

### Category-Based Timing (NOT Instruction Encyclopedias)

Each processor uses 5-15 timing categories representing instruction classes, not 200+ individual instruction entries:
- Captures 80%+ of execution time with 10-20 instruction types
- Enables workload-weighted performance prediction
- Provides meaningful bottleneck identification

### M/M/1 Queueing Analysis

Models use classical queueing theory to analyze fetch, decode, execute, and memory stages. For prefetch architectures (8086+), models include prefetch queue depth, bus contention, and EA calculation overhead.

## Processor Families (63 Total)

- **Intel (18)**: 4004, 4040, 8008, 8080, 8085, 8086, 8088, 80186, 80188, 80286, 80386, 8048, 8051, 8748, 8751, iAPX 432, 80287, 80387
- **Motorola (12)**: 6800, 6802, 6809, 68000, 68008, 68010, 68020, 6801, 6805, 68HC11, 68881, 68882
- **MOS/WDC (4)**: 6502, 6510, 65C02, 65816
- **Zilog (7)**: Z80, Z80A, Z80B, Z8000, Z80000, Z8, Z180
- **Other (22)**: 1802, 1805, SC/MP, F8, 2650, Am2901, Am2903, Am29000, TMS9900, TMS9995, TMS320C10, NS32016, NS32032, R2000, SPARC, ARM1, T414, WE32000, RTX2000, NC4016

## Quick Start

```bash
pip install -r requirements.txt
python run_all_models.py --validate
python -m intel.i8080.i8080_model
```

## Usage

```python
from intel.i8080 import i8080_model
result = i8080_model.analyze('typical')
print(f"IPS: {result.ips:,.0f}, CPI: {result.cpi:.2f}, Bottleneck: {result.bottleneck}")
```

## License

MIT License
