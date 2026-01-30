# KR581IK2 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-30

## Quick Summary

The KR581IK2 is the data path component of a Soviet WD MCP-1600 clone. Used with KR581IK1 to form a PDP-11 compatible CPU.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1983 |
| Clock | 2.5 MHz |
| Architecture | 16-bit data path, PDP-11 ISA |
| Target CPI | 8.0 |
| Compatibility | WD MCP-1600 / DEC LSI-11 |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 5.5 | ADD/SUB Rn,Rn @4-5, weighted (tuned) |
| data_transfer | 6.5 | MOV with various addressing modes (tuned) |
| memory | 10.0 | Memory-indirect, deferred addressing |
| io | 12.0 | Memory-mapped I/O |
| control | 9.0 | JMP/JSR/RTS/SOB (tuned) |

## Related Models

- KR581IK1: Control/microcode chip (companion to this data path chip)
- WD MCP-1600: Original chipset

## Files

- **Model:** `current/kr581ik2_validated.py`
- **Validation:** `validation/kr581ik2_validation.json`
- **Changelog:** `CHANGELOG.md`

## Timing Tuning (2026-01-30)
- **Status**: PASSED
- **CPI**: 8.0 (0.0% error vs target 8.0)
- **Method**: Manual instruction timing adjustment
- **Changes**: alu 5->5.5, data_transfer 6->6.5, control 8->9 (same as KR581IK1)
