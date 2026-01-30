# Rockwell PPS-4 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Rockwell International |
| Year | 1972 |
| Clock | 0.2 MHz |
| Data Width | 4-bit |
| Technology | PMOS |
| Transistors | 5,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Rockwell PPS-4 was the third commercial microprocessor (after the Intel 4004 and 4040). It featured a 4-bit data bus with a serial ALU that processed data one bit at a time, making it inherently slow compared to later parallel ALU designs. Instructions took 1-4 instruction cycles, with each instruction cycle comprising multiple clock cycles. It was used in calculators, pinball machines, and POS terminals.

## Files
- `current/pps4_validated.py` - Active model
- `validation/pps4_validation.json` - Validation data
- `docs/pps4_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
