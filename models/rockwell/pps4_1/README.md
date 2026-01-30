# Rockwell PPS-4/1 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Rockwell International |
| Year | 1976 |
| Clock | 0.25 MHz |
| Data Width | 4-bit |
| Technology | PMOS |
| Transistors | 6,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Rockwell PPS-4/1 was a single-chip microcontroller variant of the PPS-4 architecture. It integrated ROM, RAM, and I/O on a single die, inheriting the serial ALU from the PPS-4 but benefiting from on-chip integration that reduced external bus overhead. This resulted in slightly faster performance than the original multi-chip PPS-4. It was used in consumer electronics and appliances.

## Files
- `current/pps4_1_validated.py` - Active model
- `validation/pps4_1_validation.json` - Validation data
- `docs/pps4_1_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
