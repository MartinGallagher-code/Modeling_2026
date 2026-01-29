# VEB U808 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The VEB U808 is an Intel 8008 clone manufactured by VEB Mikroelektronik Erfurt. It was the first microprocessor produced in East Germany. The model uses identical timing to the Intel 8008.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | VEB Mikroelektronik Erfurt |
| Year | 1978 |
| Clock | 0.5 MHz |
| Architecture | 8-bit, sequential execution, no pipeline |
| Target CPI | 10.0 |
| Compatibility | Full Intel 8008 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 8.0 | ADD/SUB register @5T, memory @8T |
| data_transfer | 7.0 | MOV r,r @5T, MVI @8T |
| memory | 14.0 | Indirect memory ops @8-16T |
| io | 12.0 | INP/OUT with setup overhead |
| control | 10.0 | JMP @11T, CALL @11T, RET @5T |

## Historical Context

The U808 was a critical component of East Germany's efforts to develop indigenous semiconductor capability. It was reverse-engineered from the Intel 8008 and produced at the Erfurt semiconductor plant. Used primarily in industrial control applications.

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states for slow memory
3. Does not model the limited on-chip stack (7 levels)
4. Does not model interrupt response latency

## Related Models

- Intel 8008: Original processor (this is a clone)
- U880: Later East German Z80 clone

## Files

- **Model:** `current/u808_validated.py`
- **Validation:** `validation/u808_validation.json`
- **Changelog:** `CHANGELOG.md`
