# Intel Pentium Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.5%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 32-bit superscalar CISC with dual pipelines
- Year: 1993
- Clock: 60.0 MHz (up to 200 MHz)
- Target CPI: 1.0
- Predicted CPI: 0.985
- Instruction categories: alu (0.5 cycles), data_transfer (0.5), memory (1.0), control (2.0), multiply (11), divide (39)

## Cross-Validation Status
- **Family**: Intel 80x86
- **Position**: First superscalar x86 processor
- **Predecessor**: Intel 80486 (1989) - added dual pipeline, branch prediction
- **Successor**: Intel Pentium Pro (1995) - out-of-order, 3-wide superscalar
- **Variants**: P5 (60/66 MHz), P54C (75-200 MHz), Pentium MMX

## Timing Tests
- 28 per-instruction timing tests documented in validation JSON
- Includes pairing information (UV, V-only, NP)
- Branch prediction: 1 cycle predicted, 4 cycles mispredicted

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Model is fully validated and cross-referenced with family
- Consider adding instruction pairing efficiency modeling
- Add workload profiles optimized for Pentium pairing rules

## Key Architectural Notes
- First superscalar x86 - peak 2 IPC with dual U/V pipelines
- Complex pairing rules limit actual IPC to ~1.0-1.2 in practice
- Separate I/D caches (8KB each) reduce structural hazards
- 256-entry BTB for branch prediction (~80% accuracy)
- 64-bit external data bus improves memory bandwidth
- Famous FDIV bug in early versions led to $475M recall
- 3.1 million transistors (0.8um BiCMOS)
