# PowerPC 601 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.60%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 3-way superscalar RISC
- Clock: 66 MHz
- Target CPI: 0.67 (IPC 1.5)
- Key instruction categories: alu (0.5), load (1.0), store (0.5), branch (0.8), multiply (1.0), divide (1.5), fp_ops (0.5), fp_div (2.0)

## Validation Status
- 15 per-instruction timing tests added
- Cross-validation against mc68040, alpha21064, pentium
- 4 architectural consistency checks (all passed)
- SPECint92, SPECfp92, MIPS benchmark references included

## Known Issues
- None currently - model validates within 1% error
- Divide latency is amortized rather than actual 36-cycle latency

## Suggested Next Steps
- Consider adding fused multiply-add (FMA) instruction category
- Could model branch prediction more accurately

## Key Architectural Notes
- First PowerPC processor from AIM alliance (Apple/IBM/Motorola), 1993
- 3-way superscalar: Integer + FPU + Branch can execute simultaneously
- CPI < 1.0 demonstrates superscalar advantage
- Replaced 68040 in Macs, delivering 3x performance improvement
- 32KB unified cache, 4-stage pipeline
