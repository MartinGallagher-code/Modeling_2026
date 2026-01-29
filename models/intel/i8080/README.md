# Intel 8080 Microprocessor

## Overview

**Intel 8080** (1974) - Industry standard, basis for x86

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1974 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| Transistors | 4,500 |
| Technology | 6µm NMOS |
| Package | 40-pin DIP |

**Key Designers:** Federico Faggin, Masatoshi Shima, Stanley Mazor

## Architecture

**Type:** Accumulator-based with register pairs

### Register Set

- **Accumulator:** 8-bit (A)
- **General Purpose:** 6 × 8-bit (B,C,D,E,H,L) - can pair as BC,DE,HL
- **Stack Pointer:** 16-bit (SP)
- **Program Counter:** 16-bit (PC)
- **Flags:** 5 flags (S,Z,AC,P,CY)

### Addressing Modes

- Register
- Register Indirect
- Immediate
- Direct
- Stack

### Memory Architecture

- **Address Space:** 64 KB
- **Io Space:** 256 ports (separate I/O)
- **Architecture:** Von Neumann

### Special Features

- External stack in RAM (unlimited depth)
- 16-bit register pairs for addressing
- Separate I/O address space
- Vectored interrupts (RST instructions)

## History

Complete redesign of 8008 with NMOS technology and proper 40-pin package.

**Release Date:** April 1974

**Original Price:** $360 (1974)

**Significance:** Became the industry standard 8-bit processor. Defined microcomputer architecture.

### Notable Systems Using This Processor

- Altair 8800 (launched personal computer industry)
- IMSAI 8080
- Cromemco systems
- Many S-100 bus computers

**Legacy:** Direct ancestor of 8085, Z80, and through them, influenced x86. CP/M OS written for 8080.

## Performance

- **IPS Range:** 200,000 - 500,000
- **MIPS (estimated):** 0.200 - 0.500
- **Typical CPI:** 7.8

## Technical Insights

- The 40-pin package allowed separate address/data buses - huge improvement over 8008
- NMOS technology provided 10x speed improvement and +5V/-5V/+12V supplies
- External stack was controversial but enabled unlimited subroutine depth
- Instruction set became the de facto standard - Z80 was compatible extension
- Separate I/O space was Intel philosophy; Motorola chose memory-mapped I/O
- Required external clock generator (8224) and bus controller (8228)
- The Altair 8800 with 8080 started the personal computer revolution in 1975

## Performance Model

### Usage

```python
from i8080_validated import I8080Model

model = I8080Model()
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
i8080/
├── README.md                      # This documentation
├── current/
│   └── i8080_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8080_validation.json  # Validation data
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
