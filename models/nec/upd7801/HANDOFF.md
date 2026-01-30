# NEC uPD7801 Model Handoff

## Current Status
- **Validation**: MARGINAL
- **CPI Error**: 8.33%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit (1980)
- Clock: 4.0 MHz, NMOS technology
- Categories: alu (4.5c), data_transfer (4.0c), memory (7.0c), control (8.0c), stack (9.0c)
- Predicted typical CPI: 6.500 (target: 6.0)

## Known Issues
- Model uses simplified category-based timing
- Fixed workload profiles may not match all real-world use cases

## Suggested Next Steps
- Validate against datasheet instruction timing tables
- Cross-reference with related processor models
- Add per-instruction timing tests

## Key Architectural Notes
- NEC proprietary 8-bit MCU with large Japanese market share
- Features: NEC proprietary ISA, ~100 instructions, Large Japanese market, Printers/terminals
