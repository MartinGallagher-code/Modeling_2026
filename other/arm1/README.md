# Acorn RISC Machine ARM1

## Overview

**ARM1** (1985) - First ARM processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 8.0 MHz |
| Transistors | 25,000 |
| Technology | 3µm CMOS |
| Package | 84-pin PLCC |

**Key Designers:** Sophie Wilson, Steve Furber

## Architecture

**Type:** RISC with uniform register file

### Register Set

- **General:** 16 × 32-bit (R0-R15)
- **R15 Special:** Program counter + flags combined
- **Modes:** User, IRQ, FIQ, Supervisor

### Special Features

- Conditional execution on every instruction
- Barrel shifter on second operand
- Multiple register load/store (LDM/STM)
- Fast interrupt (FIQ) with banked registers

## History

Designed by Acorn for next-generation computers. First silicon worked correctly on first attempt.

**Release Date:** April 26, 1985

**Significance:** First ARM processor - started most successful CPU architecture in history.

### Notable Systems Using This Processor

- ARM1 development boards only (never in products)
- Led to ARM2 in Acorn Archimedes

**Legacy:** Founded ARM architecture - now in billions of devices annually.

## Performance

- **IPS Range:** 3,000,000 - 6,000,000
- **MIPS (estimated):** 3.000 - 6.000
- **Typical CPI:** 1.8

## Technical Insights

- Only 25,000 transistors - remarkable simplicity
- Conditional execution reduced branches by ~30%
- Barrel shifter enabled complex address calculations in one cycle
- First silicon worked perfectly - exceptional for new architecture
- Design influenced by 6502 philosophy - simplicity wins
- Sophie Wilson wrote instruction set simulator in BBC BASIC first
- FIQ mode had extra banked registers for fast interrupt response
- Low transistor count = low power - key to later mobile success
- R15 combining PC+flags was later regretted (fixed in ARMv3)

## Performance Model

### Usage

```python
from arm1_validated import ARM1Model

model = ARM1Model()
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
arm1/
├── README.md                      # This documentation
├── current/
│   └── arm1_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── arm1_validation.json  # Validation data
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
