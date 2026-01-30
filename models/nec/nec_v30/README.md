# NEC V30 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | NEC |
| Year | 1984 |
| Clock | 10.0 MHz |
| Data Width | 16-bit |
| Technology | CMOS |
| Transistors | 63,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The NEC V30 was a pin-compatible 8086 replacement that offered approximately 30% faster performance at the same clock speed. It featured a 16-bit external data bus, hardware multiply/divide (3-4x faster than 8086), improved microcode efficiency, 50% duty cycle, dual internal 16-bit buses, and an 8080 emulation mode. It was the 16-bit bus sibling of the V20 (which was 8088-compatible).

## Files
- `current/nec_v30_validated.py` - Active model
- `validation/nec_v30_validation.json` - Validation data
- `docs/nec_v30_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
