# GTE G65SC816 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.32%
- **Last Updated**: 2026-01-29
- **Cross-validation**: Initial validation complete

## Current Model Summary
- Architecture: 8/16-bit, WDC 65C816 second-source, sequential execution
- Clock: 4.0 MHz (CMOS)
- Target CPI: 3.8
- Predicted CPI: 3.75

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2 | ALU operations (ADC, SBC) - 16-bit |
| data_transfer | 3 | Data transfer (LDA, STA) - 16-bit |
| memory | 4 | Memory operations (indirect, indexed) |
| control | 3 | Control flow (BNE, JMP, JSR) |
| stack | 5 | Stack operations (PHA 16-bit, PEA) |
| long_addr | 5 | Long addressing modes (24-bit) |

## Cross-Validation Summary
- Per-instruction tests: 6 tests, all passing
- Reference sources: WDC 65C816 Data Sheet

## Known Issues
- None - model validated within 5% error

## Suggested Next Steps
- Add emulation mode vs native mode separate analysis
- Model bus multiplexing overhead more precisely

## Key Architectural Notes
- GTE G65SC816 (1985) - WDC 65C816 second-source, full pinout
- 24-bit address space (16MB) via multiplexed address/data bus
- 16-bit native mode with switchable 8/16-bit registers
- CMOS, 4 MHz operation
- Used in Apple IIGS and embedded systems

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
