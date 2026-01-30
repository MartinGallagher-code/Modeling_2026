# Hitachi 6309 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Hitachi |
| Year | 1982 |
| Clock | 2.0 MHz |
| Data Width | 8-bit |
| Technology | CMOS |
| Transistors | 12,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Hitachi 6309, often called "the best 8-bit CPU ever made," was an enhanced Motorola 6809 with native mode features. It added additional registers (E, F, W, V, 0, MD), a 32-bit accumulator (Q = D:W), hardware 16x16 multiply (MULD), hardware 32/16 divide (DIVD, DIVQ), and block transfer instructions (TFM). It ran 6809 code 10% faster in emulation mode and even faster in native mode. It was used in the Tandy Color Computer 3 and enhanced CoCo systems.

## Files
- `current/hitachi_6309_validated.py` - Active model
- `validation/hitachi_6309_validation.json` - Validation data
- `docs/hitachi_6309_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
