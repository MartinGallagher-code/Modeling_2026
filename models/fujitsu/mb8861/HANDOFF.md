# Fujitsu MB8861 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The Fujitsu MB8861 is a 6800-compatible clone manufactured by Fujitsu. The model uses identical timing to the Motorola 6800 as Fujitsu maintained full compatibility.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Fujitsu |
| Year | 1977 |
| Clock | 1.0 MHz |
| Architecture | 8-bit, sequential execution, no pipeline |
| Target CPI | 4.0 |
| Compatibility | Full M6800 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 2.8 | ADDA imm @2, INCA @2 |
| data_transfer | 3.2 | LDAA imm @2, register moves |
| memory | 4.5 | LDAA dir @3, ext @4 |
| control | 4.5 | JMP @3, BEQ @4 |
| stack | 5.0 | PSHA/PULA @4 |
| call_return | 9.0 | JSR @9, RTS @5 |

## Historical Context

Fujitsu produced the MB8861 as a second-source for the Motorola 6800. It was widely used in Japanese systems including:
- Early Japanese arcade machines
- Various Japanese home computers
- Industrial and embedded systems

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states for slow memory
3. Does not model interrupt response latency
4. Assumes uniform instruction distribution within categories

## Related Models

- Motorola M6800: Original processor (this is a clone)
- Motorola M6801: Enhanced MCU version
- Hitachi HD6301: Enhanced 6801

## Files

- **Model:** `current/mb8861_validated.py`
- **Validation:** `validation/mb8861_validation.json`
- **Changelog:** `CHANGELOG.md`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
