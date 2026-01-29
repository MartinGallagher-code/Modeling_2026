# K1810VM86 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The K1810VM86 is a Soviet Intel 8086 clone with identical timing to the original.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1985 |
| Clock | 5.0 MHz |
| Architecture | 16-bit, prefetch queue, segmented memory |
| Target CPI | 6.5 |
| Compatibility | Full Intel 8086 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 4.0 | ADD reg,reg @3, INC @2 |
| data_transfer | 4.0 | MOV reg,reg @2, MOV reg,imm @4 |
| memory | 10.0 | Memory with EA calculation |
| io | 10.0 | IN/OUT @8-12 |
| control | 8.0 | JMP @15, CALL @19, RET @8 |
| stack | 9.0 | PUSH @11, POP @8 |
| string | 12.0 | REP MOVSW/STOSW |

## Historical Context

The K1810VM86 enabled the Soviet Union to produce IBM PC-compatible computers, most notably the ES-1841. This was crucial for Soviet computing as it allowed running Western software.

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model prefetch queue effects in detail
3. Does not model segment override penalties
4. Does not model multiply/divide cycle counts individually

## Related Models

- Intel 8086: Original processor (this is a clone)

## Files

- **Model:** `current/k1810vm86_validated.py`
- **Validation:** `validation/k1810vm86_validation.json`
- **Changelog:** `CHANGELOG.md`
