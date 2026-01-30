# NEC uPD780 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The NEC uPD780 is a Z80-compatible clone manufactured by NEC. The model uses identical timing to the Zilog Z80 as NEC maintained full compatibility.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1976 |
| Clock | 2.5 MHz (original), 4.0 MHz (uPD780C) |
| Architecture | 8-bit, sequential execution, no pipeline |
| Target CPI | 5.5 |
| Compatibility | Full Z80 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 4.0 | ADD/SUB/INC/DEC register @4 |
| data_transfer | 4.0 | LD r,r @4 dominates |
| memory | 5.8 | LD r,(HL) @7 weighted |
| control | 5.5 | JP @10, JR @9.5 avg |
| stack | 10.0 | PUSH @11, POP @10 |
| block | 12.0 | LDIR weighted for termination |

## Historical Context

NEC produced the uPD780 as a second-source for the Zilog Z80. It was widely used in Japanese computers including:
- NEC PC-8001 (1979)
- NEC PC-8801 (1981)
- Various MSX computers

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states for slow memory
3. Does not model IX/IY prefix overhead (+4 cycles per instruction)
4. Does not model interrupt response latency

## Related Models

- Zilog Z80: Original processor (this is a clone)
- uPD780C: Higher clock speed variant (4 MHz)

## Files

- **Model:** `current/upd780_validated.py`
- **Validation:** `validation/upd780_validation.json`
- **Changelog:** `CHANGELOG.md`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
