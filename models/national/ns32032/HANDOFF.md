# National Semi NS32032 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.6%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 32-bit CISC with orthogonal ISA
- Clock: 10 MHz
- Target CPI: 10.0
- Predicted CPI: 10.16
- Key instruction categories: register_ops, immediate, memory_read, memory_write, branch, call_return, complex

## Cross-Validation Status
- **Instruction timing tests**: 15 tests added
- **Family comparison**: 15-20% faster than NS32016 (32-bit bus vs 16-bit)
- **Era comparison**: Compared against Motorola 68020 and Intel 80386

## Known Issues
- None currently - model validates within 5% error (excellent 1.6%)
- Very accurate model for this processor

## Suggested Next Steps
- Model is well-calibrated, minimal changes needed
- Could add NS32332 comparison when that model is created

## Key Architectural Notes
- Improved NS32016 from National Semiconductor (1984)
- Full 32-bit external data bus (vs 16-bit on NS32016)
- Single-cycle 32-bit memory access (vs 2-cycle on NS32016)
- Orthogonal instruction set design
- Variable-length instructions (1-23 bytes)
- 8 general-purpose 32-bit registers
- Demand-paged virtual memory support
- Still heavily microcoded, causing higher CPI than Intel/Motorola contemporaries
- Better memory bandwidth significantly improves performance over NS32016
