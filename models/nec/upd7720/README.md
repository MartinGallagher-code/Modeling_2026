# NEC uPD7720 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | NEC |
| Year | 1980 |
| Clock | 8.0 MHz |
| Data Width | 16-bit |
| Technology | NMOS |
| Architecture | Digital Signal Processor |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The NEC uPD7720 was an early digital signal processor designed primarily for speech synthesis applications, particularly Linear Predictive Coding (LPC) vocoders. It featured a hardware multiply-accumulate (MAC) unit, pipelined architecture optimized for real-time signal processing, 16-bit data width, and Harvard architecture with separate program and data memory. It was notably used in the Super Nintendo APU for voice synthesis.

## Files
- `current/upd7720_validated.py` - Active model
- `validation/upd7720_validation.json` - Validation data
- `docs/upd7720_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
