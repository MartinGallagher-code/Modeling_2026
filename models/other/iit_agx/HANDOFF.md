# IIT AGX Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-30

## Current Model Summary
- Architecture: XGA-compatible graphics accelerator
- Year: 1993
- Clock: 50.0 MHz
- Target CPI: 2.2
- Instruction categories: draw (2.0 cyc), pixel (2.0 cyc), register (1.0 cyc), memory (2.0 cyc), branch (3.0 cyc), blit (2.0 cyc)
- Bottleneck: pixel_throughput

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Refine instruction timing with detailed datasheet analysis
- Add more granular workload profiles for specific use cases
- Cross-validate with cycle-accurate simulators if available

## Key Architectural Notes
- IIT AGX (1993) by IIT
- XGA-compatible graphics accelerator
- Key features: XGA compatible, GUI acceleration, VRAM support
