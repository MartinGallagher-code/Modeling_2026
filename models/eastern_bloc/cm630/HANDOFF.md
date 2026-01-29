# CM630 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The CM630 is a Bulgarian CMOS 6502 clone (WDC 65C02 compatible) used in Pravetz Apple II clone computers.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Bulgaria |
| Year | 1984 |
| Clock | 1.0 MHz |
| Architecture | 8-bit, sequential execution, CMOS |
| Target CPI | 2.85 |
| Compatibility | WDC 65C02 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 2.5 | ADC/SBC #imm @2, zp @3 |
| data_transfer | 2.5 | LDA/STA #imm @2, zp @3 |
| memory | 4.0 | Indirect modes @5-6 |
| control | 3.0 | Branch @2.5avg, JMP @3 |
| stack | 3.5 | PHA @3, PLA @4 |

## Historical Context

Bulgaria was a major producer of Apple II clones in the Eastern Bloc through the Pravetz brand. The CM630 was the CPU at the heart of these machines, enabling Bulgaria to produce compatible computers for education and office use throughout the Communist world.

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model page-crossing penalties
3. Does not model decimal mode BCD operations
4. Does not model interrupt latency

## Related Models

- WDC 65C02: Original CMOS processor (this is a clone)
- MOS 6502: Original NMOS processor

## Files

- **Model:** `current/cm630_validated.py`
- **Validation:** `validation/cm630_validation.json`
- **Changelog:** `CHANGELOG.md`
