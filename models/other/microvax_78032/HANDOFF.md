# MicroVAX 78032 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 32-bit CISC (VAX subset)
- Clock: 5 MHz
- Target CPI: 5.5
- Key instruction categories: alu, memory, control, string, decimal, float
- 4 workload profiles: typical, compute, memory, control

## Known Issues
- None currently - model validates within 5% error

## Suggested Next Steps
- Consider adding more workload profiles for specific VMS application types
- Could refine cycle counts with more detailed VAX microcode documentation
- Add emulation-based workload traces if available

## Key Architectural Notes
- First single-chip VAX processor (1984)
- Microcoded CISC with full VMS compatibility
- Complex instruction set includes string manipulation and packed decimal
- 68-pin CERDIP package, ~125,000 transistors
- Floating-point operations are particularly expensive (12 cycles)
