# Intel 3001/3002 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Intel |
| Year | 1974 |
| Clock | 5.0 MHz |
| Data Width | 2-bit slice |
| Technology | Schottky Bipolar |
| Transistors | 125 (per slice) |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Intel 3001/3002 was Intel's entry into the bit-slice processor market. The 3002 is a 2-bit ALU slice while the 3001 serves as the microprogram control unit. Multiple 3002 slices are cascaded for wider data paths. All microinstructions execute in a single clock cycle, with 11 general-purpose registers per slice. It competed with AMD's 4-bit Am2901 bit-slice processor.

## Files
- `current/i3002_validated.py` - Active model
- `validation/i3002_validation.json` - Validation data
- `docs/i3002_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
