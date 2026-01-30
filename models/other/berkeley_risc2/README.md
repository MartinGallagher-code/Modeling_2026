# Berkeley RISC II Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | UC Berkeley |
| Year | 1983 |
| Clock | 3.0 MHz |
| Data Width | 32-bit |
| Technology | NMOS |
| Transistors | 40,760 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Berkeley RISC II was the improved second RISC processor from UC Berkeley. It featured a 3-stage pipeline (fetch, decode, execute), 138 registers with 8 overlapping register windows, single-cycle ALU operations, load/store architecture, and delayed branches. With 39 instructions (expanded from RISC I's 31), it improved upon RISC I with more register windows, better pipeline efficiency, and an improved memory interface. It was a direct influence on the Sun SPARC architecture.

## Files
- `current/berkeley_risc2_validated.py` - Active model
- `validation/berkeley_risc2_validation.json` - Validation data
- `docs/berkeley_risc2_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
