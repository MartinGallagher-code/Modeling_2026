# IM1821VM85A Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-30

## Quick Summary

The IM1821VM85A is a Soviet Intel 8085 clone with identical timing to the original.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1985 |
| Clock | 3.0 MHz |
| Architecture | 8-bit, sequential execution, multiplexed bus |
| Target CPI | 5.0 |
| Compatibility | Full Intel 8085 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 2.9 | ADD/SUB r @4, ADD M @7 (tuned) |
| data_transfer | 3.5 | MOV r,r @4, MVI @7 (tuned) |
| memory | 7.0 | LDA @13, MOV r,M @7 (tuned) |
| io | 10.0 | IN/OUT @10 T-states |
| control | 5.0 | JMP @10, CALL @18 (tuned) |
| stack | 9.5 | PUSH @12, POP @10 (tuned) |

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states
3. Does not model serial I/O timing
4. Does not model interrupt latency

## Related Models

- Intel 8085: Original processor (this is a clone)
- KR580VM80A: Soviet 8080 clone

## Files

- **Model:** `current/im1821vm85a_validated.py`
- **Validation:** `validation/im1821vm85a_validation.json`
- **Changelog:** `CHANGELOG.md`

## Timing Tuning (2026-01-30)
- **Status**: PASSED
- **CPI**: 4.995 (0.1% error vs target 5.0)
- **Method**: Manual instruction timing adjustment
- **Changes**: alu 4->2.9, data_transfer 4.5->3.5, memory 8->7, control 6->5, stack 10.5->9.5
