# NEC uPD7759 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-30

## Current Model Summary
- Architecture: ADPCM voice synthesis for arcade games
- Year: 1987
- Clock: 5.0 MHz
- Target CPI: 3.0
- Instruction categories: oscillator (3.0 cyc), envelope (2.0 cyc), register (1.0 cyc), memory (2.0 cyc), control (3.0 cyc), mixing (2.0 cyc)
- Bottleneck: sample_decode

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Refine instruction timing with detailed datasheet analysis
- Add more granular workload profiles for specific use cases
- Cross-validate with cycle-accurate simulators if available

## Key Architectural Notes
- NEC uPD7759 (1987) by NEC
- ADPCM voice synthesis for arcade games
- Key features: ADPCM decoding, Speech synthesis, Arcade standard
