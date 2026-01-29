# Intel 4004 Microprocessor

## Overview

**Intel 4004** (1971) - First commercial microprocessor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1971 |
| Manufacturer | Various |
| Data Width | 4-bit |
| Clock | 0.74 MHz |
| Transistors | 2,300 |
| Technology | 10µm PMOS |
| Package | 16-pin DIP |

**Key Designers:** Federico Faggin, Ted Hoff, Stanley Mazor, Masatoshi Shima

## Architecture

**Type:** Accumulator-based Harvard architecture

### Register Set

- **Accumulator:** 4-bit
- **Index Registers:** 16 × 4-bit (8 pairs for 8-bit operations)
- **Program Counter:** 12-bit
- **Stack:** 3-level hardware stack

### Addressing Modes

- Register
- Immediate
- Direct

### Memory Architecture

- **Rom:** 4 KB (4096 bytes)
- **Ram:** 640 bytes (1280 × 4-bit nibbles)
- **Architecture:** Harvard (separate program/data)

### Special Features

- BCD arithmetic support
- Decimal adjust instruction
- Multiplexed 4-bit bus (reduces pin count)

## History

Developed for Busicom calculator project. Intel negotiated to retain rights, making it the first general-purpose microprocessor.

**Release Date:** November 15, 1971

**Original Price:** $200 (1971)

**Significance:** First commercially available single-chip microprocessor. Launched the microprocessor revolution.

### Notable Systems Using This Processor

- Busicom 141-PF calculator (original application)
- Various industrial controllers
- Educational systems

**Legacy:** Established Intel as the microprocessor leader. Architecture concepts influenced all subsequent processors.

## Performance

- **IPS Range:** 46,250 - 92,500
- **MIPS (estimated):** 0.046 - 0.092
- **Typical CPI:** 1.5

## Technical Insights

- Despite only 4-bit data width, could handle 8-digit BCD numbers using register pairs
- Harvard architecture was chosen to maximize limited pin count (only 16 pins)
- The 3-level stack limited subroutine nesting but saved transistors
- Multiplexed bus required external latches, adding system complexity
- BCD focus reflects calculator origins - binary operations were secondary
- Remarkably, Linux was booted on a 4004 in 2024 (took 5 days to boot)
- Transistor efficiency: 40 IPS per transistor - exceptional for the era

## Performance Model

### Usage

```python
from i4004_validated import I4004Model

model = I4004Model()
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
i4004/
├── README.md                      # This documentation
├── current/
│   └── i4004_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i4004_validation.json  # Validation data
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
