# Zilog Z80 Microprocessor

## Overview

**Zilog Z80** (1976) - Most popular 8-bit CPU ever

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 2.5 MHz |
| Transistors | 8,500 |
| Technology | NMOS |
| Package | 40-pin DIP |

**Key Designers:** Federico Faggin, Masatoshi Shima

## Architecture

**Type:** Accumulator-based (8080 superset)

### Register Set

- **Main:** A, B, C, D, E, H, L, F (8080 compatible)
- **Alternate:** A', B', C', D', E', H', L', F' (shadow set)
- **Index:** 2 × 16-bit (IX, IY)
- **Special:** I (interrupt vector), R (refresh counter)
- **Stack Pointer:** 16-bit
- **Program Counter:** 16-bit

### Addressing Modes

- 8080 modes plus:
- Indexed (IX+d, IY+d)
- Bit operations on any register/memory

### Memory Architecture

- **Address Space:** 64 KB
- **Io Space:** 256 ports

### Special Features

- Shadow register set for fast context switch
- Built-in DRAM refresh counter
- Two interrupt modes (IM 0, 1, 2)
- Block move/search/I/O instructions
- Indexed addressing with displacement

## History

Designed by 8080 creators who left Intel for Zilog.

**Release Date:** July 1976

**Significance:** Became most popular 8-bit processor ever made.

### Notable Systems Using This Processor

- TRS-80 (Radio Shack)
- Sinclair ZX80/ZX81/Spectrum
- MSX computers (Japan/Europe)
- CP/M business systems
- Pac-Man and many arcade games
- Sega Master System/Game Gear
- TI graphing calculators (as eZ80)

**Legacy:** Still manufactured and used. Massive software library. eZ80 variant in TI calculators.

## Performance

- **IPS Range:** 250,000 - 580,000
- **MIPS (estimated):** 0.250 - 0.580
- **Typical CPI:** 7.8

## Technical Insights

- Shadow registers enabled interrupt handlers without saving state
- DRAM refresh was built-in - saved external chip and complexity
- Block operations (LDIR, CPIR, etc.) were revolutionary
- IX/IY indexed addressing ideal for structured data and stack frames
- CP/M compatibility ensured business software library
- Bit operations addressed a major 8080 weakness
- Per-clock performance similar to 8080 - additions cost cycles
- Still in TI calculators as eZ80 - remarkable longevity

## Performance Model

### Usage

```python
from z80_validated import Z80Model

model = Z80Model()
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
z80/
├── README.md                      # This documentation
├── current/
│   └── z80_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z80_validation.json  # Validation data
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
