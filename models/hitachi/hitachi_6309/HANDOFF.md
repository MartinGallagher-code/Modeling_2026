# Hitachi 6309 Model Handoff

## Current Status
- **Validation**: PASSED
- **Target CPI**: 3.0 (native mode), 3.15 (emulation mode)
- **Last Updated**: 2026-01-29

## Overview

The Hitachi 6309 (1982) is an enhanced version of the Motorola 6809, often called "the best 8-bit CPU ever made". It was produced by Hitachi as a second-source for the 6809 but includes significant undocumented enhancements.

**Key Specifications:**
- Clock: 1-3.5 MHz (2 MHz typical)
- Data width: 8-bit (with 16-bit and 32-bit capabilities)
- Address space: 64 KB
- Estimated transistors: ~12,000

## Operating Modes

### Native Mode (default)
Access to all 6309 features:
- Additional registers (E, F, W, V, 0, MD)
- 32-bit accumulator Q (D:W)
- 16x16 multiply (MULD)
- 32/16 division (DIVQ)
- Block transfers (TFM)
- Bit manipulation instructions
- Most instructions 1 cycle faster than 6809

**Native mode CPI: ~3.0** (~17% faster than 6809)

### Emulation Mode
6809-compatible mode:
- Same instruction set as 6809
- Still ~10% faster due to improved internals
- Used for running unmodified 6809 software

**Emulation mode CPI: ~3.15** (~10% faster than 6809)

## Current Model Summary

### Native Mode Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 1.9 | 8-bit ALU ops (1 cycle faster than 6809) |
| alu_16bit | 2.8 | 16-bit ALU ops |
| data_transfer | 2.3 | LDA/LDD/LDW immediate |
| memory | 3.3 | Direct/indexed memory access |
| control | 3.0 | Branches, jumps, calls |
| stack | 4.2 | PSHS/PULS operations |
| multiply_8x8 | 10.0 | MUL @10 |
| multiply_16x16 | 26.0 | MULD @25-28 (16x16->32) |
| divide | 28.0 | DIVD @25, DIVQ @34 |
| block_transfer | 9.0 | TFM (6+3n cycles) |
| bit_manipulation | 5.0 | BAND, BOR, etc. |

### Emulation Mode Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.2 | ~10% faster than 6809 |
| data_transfer | 2.5 | ~10% faster |
| memory | 3.9 | ~10% faster |
| control | 3.7 | ~10% faster |
| stack | 4.9 | ~10% faster |
| multiply | 10.0 | MUL @10 (vs 6809's 11) |

## Comparison to M6809

| Feature | M6809 | HD6309 (Native) | Improvement |
|---------|-------|-----------------|-------------|
| Typical CPI | 3.5 | 2.97 | 18% faster |
| Accumulators | A, B, D | A, B, D, E, F, W, Q | +32-bit Q |
| Multiply | 8x8 @11 | 8x8 @10, 16x16 @26 | Much faster |
| Division | None | 16/8, 32/16 | New |
| Block Transfer | No | TFM | New |
| Bit Operations | Limited | BAND, BOR, etc. | New |

## 6309-Specific Registers

| Register | Size | Description |
|----------|------|-------------|
| E | 8-bit | Additional accumulator |
| F | 8-bit | Additional accumulator |
| W | 16-bit | E:F concatenated |
| Q | 32-bit | D:W concatenated |
| V | 16-bit | General purpose |
| 0 | 16-bit | Zero register (always 0) |
| MD | 8-bit | Mode and error flags |

## 6309-Specific Instructions

### Arithmetic
- **MULD** - 16x16 signed multiply -> 32-bit result in Q
- **DIVD** - 16/8 signed divide (D / mem -> A rem B)
- **DIVQ** - 32/16 signed divide (Q / mem -> D rem W)

### Block Transfers
- **TFM r+,r+** - Forward transfer (memcpy-like)
- **TFM r-,r-** - Reverse transfer
- **TFM r+,r** - Fill memory
- **TFM r,r+** - Read from port

### Bit Manipulation
- **BAND, BOR, BEOR** - Bit AND/OR/XOR to CC
- **BIAND, BIOR, BIEOR** - Inverted versions
- **LDBT, STBT** - Load/store bit to memory

### Inter-Register Operations
- **ADDR, ADCR** - Add register to register
- **SUBR, SBCR** - Subtract register from register
- **ANDR, ORR, EORR** - Logical operations
- **CMPR** - Compare register to register

## Validation Status
- **Model tests**: All passing
- **Timing tests**: Based on observed 6309 behavior
- **Cross-validation**: Compared against M6809 model

## Known Issues
None - model is validated.

## Suggested Next Steps
1. Add timing tests for individual instructions
2. Validate against Tandy CoCo 3 software timings
3. Consider GIME chip interaction for CoCo 3

## Historical Notes
- The 6309's extra features were officially undocumented
- Discovered by CoCo enthusiasts in the late 1980s
- Hitachi never publicly documented native mode
- Popular in the TRS-80 Color Computer community
- Still used today by CoCo enthusiasts and demoscene

## References
- Original 6809/6309 comparison documents
- CoCo community timing measurements
- NitrOS-9 operating system (6309 native mode optimized)

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 11
- **Corrections**: See `identification/sysid_result.json`
