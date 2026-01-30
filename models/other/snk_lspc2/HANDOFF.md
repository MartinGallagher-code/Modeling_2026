# SNK LSPC2-A2 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-30

## Current Model Summary
- Architecture: Neo Geo video processor, hardware sprite scaler
- Year: 1990
- Clock: 24.0 MHz
- Target CPI: 2.5
- Instruction categories: draw (2.0 cyc), pixel (2.0 cyc), register (1.0 cyc), memory (3.0 cyc), branch (4.0 cyc), blit (2.0 cyc)
- Bottleneck: sprite_engine

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Refine instruction timing with detailed datasheet analysis
- Add more granular workload profiles for specific use cases
- Cross-validate with cycle-accurate simulators if available

## Key Architectural Notes
- SNK LSPC2-A2 (1990) by SNK
- Neo Geo video processor, hardware sprite scaler
- Key features: 380 sprites on screen, Hardware scaling, Arcade standard
