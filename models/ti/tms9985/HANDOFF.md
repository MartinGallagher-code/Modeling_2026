# TMS9985 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.89%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Clock: 2.5 MHz, 16-bit single-chip CPU with 256B on-chip RAM (1978)
- 5 instruction categories (base_cycles only):
  - alu: 6.5, data_transfer: 8.0, memory: 12.0, control: 14.0, stack: 15.0
- Weighted CPI for typical workload: 10.089 vs target 10.0
- Architecture: memory-to-memory with workspace pointers, on-chip workspace RAM

## Known Issues
- None significant. Model validates within 0.89% of target.
- The family relationship is well preserved: TMS9985 (CPI ~10) < TMS9980 (CPI ~12) as expected.

## Suggested Next Steps
- Model is well-calibrated. No immediate changes needed.
- Could add more detailed workspace vs external memory access modeling.
- Consider comparing against TMS9900 (full 16-bit bus) for family validation.

## Key Architectural Notes
- Single-chip integration of TMS9900 architecture with 256 bytes on-chip RAM
- On-chip RAM used for workspace registers, eliminating external bus access for register operations
- External memory access still required for instruction fetch, immediate data, and indirect targets
- 2.5 MHz clock is slightly faster than TMS9980's 2.0 MHz
- Same ISA as TMS9900 family: memory-to-memory, workspace pointer based
- BLWP/RTWP context switch is faster than TMS9980 since workspace is on-chip

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
