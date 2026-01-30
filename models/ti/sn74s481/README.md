# Texas Instruments SN74S481 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Texas Instruments |
| Year | 1976 |
| Clock | 8.0 MHz |
| Data Width | 4-bit slice |
| Technology | Schottky TTL |
| Transistors | 180 (per slice) |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Texas Instruments SN74S481 was TI's bit-slice ALU offering, providing a 4-bit arithmetic logic unit with look-ahead carry capability for high-speed operation. Built using Schottky TTL technology, all operations completed in a single clock cycle. It was compatible with the 74S182 carry look-ahead generator for cascading multiple slices into wider data paths.

## Files
- `current/sn74s481_validated.py` - Active model
- `validation/sn74s481_validation.json` - Validation data
- `docs/sn74s481_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
