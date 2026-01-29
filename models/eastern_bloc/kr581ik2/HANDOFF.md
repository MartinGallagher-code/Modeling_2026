# KR581IK2 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

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
| alu | 5.0 | ADD/SUB Rn,Rn @4-5, weighted |
| data_transfer | 6.0 | MOV with various addressing modes |
| memory | 10.0 | Memory-indirect, deferred addressing |
| io | 12.0 | Memory-mapped I/O |
| control | 8.0 | JMP/JSR/RTS/SOB |

## Related Models

- KR581IK1: Control/microcode chip (companion to this data path chip)
- WD MCP-1600: Original chipset

## Files

- **Model:** `current/kr581ik2_validated.py`
- **Validation:** `validation/kr581ik2_validation.json`
- **Changelog:** `CHANGELOG.md`
