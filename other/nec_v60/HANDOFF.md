# NEC V60 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.67%
- **Last Updated**: 2026-01-29
- **Cross-validation**: Initial validation complete

## Current Model Summary
- Architecture: 32-bit, new NEC proprietary ISA, sequential execution
- Clock: 16.0 MHz
- Target CPI: 3.0
- Predicted CPI: 3.05

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2 | ALU operations (ADD, SUB, MUL) - 32-bit |
| data_transfer | 2 | Data transfer (MOV, MOVEA) - 32-bit |
| memory | 4 | Memory operations (load/store, indexed) |
| control | 3 | Control flow (BR, Bcc, JSR, RET) |
| float | 8 | Floating point operations (FADD, FMUL) |
| string | 6 | String manipulation (MOVS, CMPS) |

## Cross-Validation Summary
- Per-instruction tests: 11 tests, all passing
- Reference sources: NEC V60 Technical Manual

## Known Issues
- None - model validated within 5% error

## Suggested Next Steps
- Add detailed FPU pipeline timing
- Compare with V70 successor
- Model cache effects if documentation available

## Key Architectural Notes
- NEC V60 (1986) - Japan's first major 32-bit processor
- ~375,000 transistors, 16 MHz CMOS
- New proprietary ISA (NOT x86 compatible)
- On-chip floating point unit
- String manipulation instructions
- 32-bit address space (4GB)
- Used in NEC workstations and embedded systems
- Followed by V70 and V80 successors
