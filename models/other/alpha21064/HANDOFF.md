# DEC Alpha 21064 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.68%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 64-bit superscalar RISC (2-way)
- Clock: 150 MHz
- Target CPI: 0.77 (IPC 1.3)
- Key instruction categories: alu (0.5), load (1.0), store (0.8), branch (1.0), multiply (2.5), divide (6.0)

## Validation Status
- 14 per-instruction timing tests added
- Cross-validation against aim__ppc_601, hp_pa_risc, mips_r4000
- 4 architectural consistency checks (all passed)
- SPECint92, SPECfp92, MIPS benchmark references included

## Known Issues
- CPI error at 4.68% is close to 5% threshold
- Model does not capture 7-stage pipeline stalls accurately

## Suggested Next Steps
- Consider adding FP instruction categories for scientific workloads
- Could refine branch prediction model
- May need slight tuning if error increases

## Key Architectural Notes
- First 64-bit RISC microprocessor from DEC (1992)
- 2-way superscalar with 7-stage pipeline
- 8KB I-cache + 8KB D-cache, up to 16MB external cache
- Fastest microprocessor at launch, influenced AMD64 design
- Many Alpha engineers later worked on AMD's K7/K8
