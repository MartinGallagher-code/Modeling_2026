# Inmos T424 Model Handoff

## Current Status
- **Validation**: MARGINAL
- **CPI Error**: 20.00%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 32-bit (1985)
- Clock: 15.0 MHz, CMOS technology
- Categories: alu (1.5c), data_transfer (1.5c), memory (2.5c), control (3.0c), channel (3.5c)
- Predicted typical CPI: 2.400 (target: 2.0)

## Known Issues
- Model uses simplified category-based timing
- Fixed workload profiles may not match all real-world use cases

## Suggested Next Steps
- Validate against datasheet instruction timing tables
- Cross-reference with related processor models
- Add per-instruction timing tests

## Key Architectural Notes
- 32-bit transputer with 4KB on-chip RAM, T414 variant
- Features: 32-bit transputer, 4KB on-chip SRAM, T414 variant, Occam/CSP
