# AMD Am9511 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | AMD |
| Year | 1977 |
| Clock | 3.0 MHz |
| Data Width | 32-bit floating point |
| Technology | NMOS |
| Architecture | Stack-based math coprocessor |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The AMD Am9511 was an early arithmetic processing unit designed to accelerate floating-point and fixed-point math operations for 8-bit microprocessor systems. It featured a 4-level internal stack and supported 32-bit floating point and 16/32-bit fixed point operations. It was used as a math coprocessor alongside CPUs like the Intel 8080 and Zilog Z80.

## Files
- `current/am9511_validated.py` - Active model
- `validation/am9511_validation.json` - Validation data
- `docs/am9511_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
