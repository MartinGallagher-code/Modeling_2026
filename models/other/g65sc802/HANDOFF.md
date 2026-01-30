# GTE G65SC802 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.86%
- **Last Updated**: 2026-01-29
- **Cross-validation**: Initial validation complete

## Current Model Summary
- Architecture: 8/16-bit, WDC 65C816 second-source, sequential execution
- Clock: 4.0 MHz (CMOS)
- Target CPI: 3.5
- Predicted CPI: 3.40

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2 | ALU operations (ADC, SBC, AND, ORA) |
| data_transfer | 3 | Data transfer (LDA, STA, TAX) |
| memory | 4 | Memory operations (indirect, indexed) |
| control | 3 | Control flow (BNE, JMP, JSR) |
| stack | 4 | Stack operations (PHA, PLA, PEA) |
| long_addr | 5 | Long addressing modes (24-bit) |

## Cross-Validation Summary
- Per-instruction tests: 6 tests, all passing
- Reference sources: WDC 65C816 Data Sheet

## Known Issues
- None - model validated within 5% error

## Suggested Next Steps
- Add native mode vs emulation mode separate workload profiles
- Compare with WDC 65C816 original

## Key Architectural Notes
- GTE G65SC802 (1985) - WDC 65C816 second-source
- 6502-compatible 40-pin DIP package
- Internal 16-bit registers, 24-bit addressing via bank register
- CMOS, 4 MHz operation
- Can run both 6502 emulation and 65816 native mode code

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
