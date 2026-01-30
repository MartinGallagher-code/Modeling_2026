# SGS-Thomson D950 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-30

## Current Model Summary
- Architecture: European DSP for GSM baseband processing
- Year: 1991
- Clock: 20.0 MHz
- Target CPI: 1.4
- Instruction categories: mac (1.0 cyc), alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (2.0 cyc), special (3.0 cyc)
- Bottleneck: mac_throughput

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Refine instruction timing with detailed datasheet analysis
- Add more granular workload profiles for specific use cases
- Cross-validate with cycle-accurate simulators if available

## Key Architectural Notes
- SGS-Thomson D950 (1991) by SGS-Thomson
- European DSP for GSM baseband processing
- Key features: GSM baseband, European design, Viterbi support
