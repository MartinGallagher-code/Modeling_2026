# Z8 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.6%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Clock: 8.0 MHz
- Architecture: 8-bit single-chip microcontroller with register-file
- Expected CPI: 10.0
- Predicted CPI: 9.54

Key instruction timings:
- Register ops: 6 cycles
- Immediate: 6 cycles
- Memory (indexed): 12 cycles
- Control flow: 12 cycles
- Stack: 14 cycles
- Call/return: 20 cycles

## Known Issues
- None currently - model validates within 5% error target

## Suggested Next Steps
- Could refine timings if Z8 datasheet becomes available
- Consider adding I/O instruction category for peripheral operations
- May want to add interrupt handling overhead for real-time workloads

## Key Architectural Notes
- Z8 is a single-chip MCU, not just a CPU like Z80
- Uses register-file architecture with 144 general-purpose registers
- On-chip peripherals: timers, UART, I/O ports
- Designed for embedded control applications
- Slower per-instruction than Z80 but more integrated
