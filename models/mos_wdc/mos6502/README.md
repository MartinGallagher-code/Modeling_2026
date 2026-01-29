# MOS Technology 6502 Microprocessor

## Overview

**MOS 6502** (1975) - Apple II, Commodore, NES CPU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1975 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Transistors | 3,510 |
| Technology | NMOS |
| Package | 40-pin DIP |

**Key Designers:** Chuck Peddle, Bill Mensch, team from Motorola

## Architecture

**Type:** Accumulator-based with zero page

### Register Set

- **Accumulator:** 8-bit (A)
- **Index:** 2 × 8-bit (X, Y)
- **Stack Pointer:** 8-bit (fixed at $01xx)
- **Program Counter:** 16-bit
- **Status:** 7 flags (N,V,-,B,D,I,Z,C)

### Addressing Modes

- Immediate
- Zero Page
- Zero Page,X
- Zero Page,Y
- Absolute
- Absolute,X
- Absolute,Y
- Indirect
- (Indirect,X)
- (Indirect),Y
- Relative
- Implied

### Memory Architecture

- **Address Space:** 64 KB
- **Zero Page:** $00-$FF (fast access pseudo-registers)
- **Stack:** $0100-$01FF (fixed location)

### Special Features

- Zero page as 256 pseudo-registers
- Decimal mode for BCD arithmetic
- Efficient indexed addressing
- Simple pipeline (2 cycles minimum)

## History

Designed by ex-Motorola team to be cheap and fast.

**Release Date:** September 1975

**Original Price:** $25 (vs $179 for 8080)

**Significance:** Made microcomputers affordable. Enabled personal computer revolution.

### Notable Systems Using This Processor

- Apple I and Apple II
- Commodore PET, VIC-20, C64 (6510 variant)
- Atari 400/800/2600
- Nintendo Entertainment System (NES)
- BBC Micro
- Many arcade games

**Legacy:** One of most important processors ever. Still manufactured today by WDC.

## Performance

- **IPS Range:** 250,000 - 500,000
- **MIPS (estimated):** 0.250 - 0.500
- **Typical CPI:** 3.5

## Technical Insights

- Zero page was brilliant - 256 bytes of fast pseudo-registers
- Price ($25) was revolutionary - 1/7th the cost of 8080
- Fewer transistors than 8080 yet often faster effective performance
- Decimal mode enabled calculator-like BCD without external logic
- (Indirect),Y mode was ideal for array/string processing
- Fixed stack page simplified hardware at cost of 256-byte limit
- Only 3 general-purpose registers yet extremely capable
- Still manufactured by WDC - remarkable 50-year production run
- NES games showed what skilled programmers could achieve

## Performance Model

### Usage

```python
from mos6502_validated import MOS6502Model

model = MOS6502Model()
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
mos6502/
├── README.md                      # This documentation
├── current/
│   └── mos6502_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── mos6502_validation.json  # Validation data
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
