# Stanford MIPS Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Stanford University |
| Year | 1983 |
| Clock | 2.0 MHz |
| Data Width | 32-bit |
| Technology | NMOS |
| Transistors | 25,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Stanford MIPS was the original academic RISC processor designed by John Hennessy at Stanford University. It featured a 5-stage pipeline (IF, ID, EX, MEM, WB), 32 general-purpose registers, delayed branches with 1 delay slot, load/store architecture, and hardwired control (no microcode). It was the precursor to the commercial MIPS R2000 (1986) and pioneered aggressive pipelining with software scheduling of load delay slots.

## Files
- `current/stanford_mips_validated.py` - Active model
- `validation/stanford_mips_validation.json` - Validation data
- `docs/stanford_mips_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
