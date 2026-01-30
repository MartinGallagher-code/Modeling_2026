# Intel i960CF Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-30

## Current Model Summary
- Architecture: Enhanced i960 with on-chip FPU
- Year: 1992
- Clock: 33.0 MHz
- Target CPI: 0.85
- Instruction categories: alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (1.0 cyc), multiply (2.0 cyc), divide (8.0 cyc)
- Bottleneck: issue_width

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Refine instruction timing with detailed datasheet analysis
- Add more granular workload profiles for specific use cases
- Cross-validate with cycle-accurate simulators if available

## Key Architectural Notes
- Intel i960CF (1992) by Intel
- Enhanced i960 with on-chip FPU
- Key features: On-chip FPU, 4KB I-cache, Superscalar
