# Fairchild 9440 MICROFLAME Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 16-bit minicomputer-on-a-chip (Nova ISA)
- Clock: 10 MHz
- Target CPI: 3.5 (register ops fast @2, memory slower @4)
- Key instruction categories: alu, data_transfer, memory, io, control, stack
- Cross-validated with 13 timing tests

## Known Issues
- None currently - model validates within 5% error

## Suggested Next Steps
- Could model indirect addressing mode timing overhead
- Could compare performance against original Nova minicomputer
- Consider modeling auto-increment/auto-decrement addressing

## Key Architectural Notes
- Fairchild 9440 MICROFLAME (1979) implements Data General Nova ISA
- I2L (Integrated Injection Logic) bipolar process
- ~5000 transistors
- 10 MHz clock, 16-bit data bus
- 4 accumulators (AC0-AC3), Nova architecture
- 15-bit address space (32K words)
- Faster than original Data General Nova minicomputer
- Register operations are fast (2 cycles)
- Memory operations are bottleneck (4 cycles)
- I/O operations slowest (6 cycles)
- Nova ISA uses accumulator-based architecture
- JSR saves return address in AC3 (no hardware stack)
