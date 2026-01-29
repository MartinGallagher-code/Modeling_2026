# Tesla MHB8080A Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The Tesla MHB8080A is a Czechoslovak Intel 8080A clone by Tesla Piestany with identical timing to the original.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Tesla Piestany (Czechoslovakia) |
| Year | 1982 |
| Clock | 2.0 MHz |
| Architecture | 8-bit, sequential execution, no pipeline |
| Target CPI | 7.5 |
| Compatibility | Full Intel 8080A instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 5.0 | ADD/SUB r @4, ADD M @7 |
| data_transfer | 5.5 | MOV r,r @5, MVI @7 |
| memory | 10.0 | LDA @13, MOV r,M @7 |
| io | 10.0 | IN/OUT @10 |
| control | 9.0 | JMP @10, CALL @17, RET @10 |
| stack | 10.5 | PUSH @11, POP @10 |

## Historical Context

Tesla Piestany was one of the main semiconductor manufacturers in Czechoslovakia. The MHB8080A was used in several significant Czechoslovak computers, including the PMI-80 educational computer and the PMD 85 personal computer.

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states
3. Does not model interrupt latency

## Related Models

- Intel 8080A: Original processor (this is a clone)

## Files

- **Model:** `current/tesla_mhb8080a_validated.py`
- **Validation:** `validation/tesla_mhb8080a_validation.json`
- **Changelog:** `CHANGELOG.md`
