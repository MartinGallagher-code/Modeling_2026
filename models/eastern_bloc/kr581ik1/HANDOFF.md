# KR581IK1 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The KR581IK1 is the control/microcode component of a Soviet WD MCP-1600 clone. Used with KR581IK2 to form a PDP-11 compatible CPU.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1983 |
| Clock | 2.5 MHz |
| Architecture | 16-bit, microcoded PDP-11 ISA |
| Target CPI | 8.0 |
| Compatibility | WD MCP-1600 / DEC LSI-11 |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 5.0 | ADD/SUB Rn,Rn @4-5, weighted |
| data_transfer | 6.0 | MOV with various addressing modes |
| memory | 10.0 | Memory-indirect, deferred addressing |
| io | 12.0 | Memory-mapped I/O |
| control | 8.0 | JMP/JSR/RTS/SOB |

## Related Models

- KR581IK2: Data path chip (companion to this control chip)
- WD MCP-1600: Original chipset

## Files

- **Model:** `current/kr581ik1_validated.py`
- **Validation:** `validation/kr581ik1_validation.json`
- **Changelog:** `CHANGELOG.md`
