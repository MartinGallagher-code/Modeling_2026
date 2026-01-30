# NEC V850 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-30

## Current Model Summary
- Architecture: Embedded RISC for automotive ECUs
- Year: 1994
- Clock: 20.0 MHz
- Target CPI: 1.4
- Instruction categories: alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (1.0 cyc), multiply (2.0 cyc), divide (10.0 cyc)
- Bottleneck: pipeline_stall

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Refine instruction timing with detailed datasheet analysis
- Add more granular workload profiles for specific use cases
- Cross-validate with cycle-accurate simulators if available

## Key Architectural Notes
- NEC V850 (1994) by NEC
- Embedded RISC for automotive ECUs
- Key features: 5-stage pipeline, On-chip ROM/RAM, Automotive grade
