# MIPS R2000 Microprocessor

## Overview

**MIPS R2000** (1985) - MIPS architecture origin

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 8.0 MHz |
| Transistors | 115,000 |
| Technology | 2µm CMOS |
| Package | 145-pin PGA |

**Key Designers:** John Hennessy, Stanford team

## Architecture

**Type:** RISC load/store

### Register Set

- **General:** 32 × 32-bit (R0 hardwired to zero)
- **Hi Lo:** HI/LO registers for multiply/divide results
- **Pc:** 32-bit program counter

## History

Commercial version of Stanford MIPS research project.

**Release Date:** 1985

**Significance:** First commercial MIPS processor. Proved RISC viability.

### Notable Systems Using This Processor

- SGI workstations
- DEC workstations (DECstation)
- ACE consortium machines
- PlayStation 1 (R3000 derivative)

**Legacy:** MIPS architecture dominated SGI. R3000 derivative in PlayStation.

## Performance

- **IPS Range:** 3,500,000 - 7,000,000
- **MIPS (estimated):** 3.500 - 7.000
- **Typical CPI:** 2.0

## Technical Insights

- Stanford research led by Hennessy became commercial success
- R0 hardwired to zero simplified many instruction encodings
- Branch delay slot exposed pipeline - compiler filled it
- 5-stage pipeline was clean, classic RISC implementation
- Originally NO interlocking - compiler avoided hazards
- Multiply/divide multi-cycle, results in HI/LO registers
- Clean architecture became standard for teaching computer architecture
- PlayStation 1 CPU (R3000) brought MIPS to millions

## Performance Model

### Usage

```python
from r2000_validated import R2000Model

model = R2000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"MIPS: {result.mips:.3f}")
print(f"Bottleneck: {result.bottleneck}")

# Validate against known specifications
for test, data in model.validate().items():
    status = "✓ PASS" if data['pass'] else "✗ FAIL"
    print(f"{test}: {status}")
```

## Directory Structure

```
r2000/
├── README.md                      # This documentation
├── current/
│   └── r2000_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── r2000_validation.json  # Validation data
└── docs/                          # Additional documentation
```

## Validation

| Test | Status |
|------|--------|
| IPS Range | ✓ Validated against specifications |
| CPI | ✓ Calibrated to workload mix |
| Architecture | ✓ Cross-referenced with datasheets |

**Target Accuracy:** ±15% for performance estimates

---

*Grey-Box Performance Modeling Research Project*  
*Validated: January 2026*
