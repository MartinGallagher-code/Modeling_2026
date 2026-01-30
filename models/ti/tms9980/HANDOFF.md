# TMS9980 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.70%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Clock: 2 MHz, 16-bit CPU with 8-bit external bus (1976)
- 5 instruction categories (base_cycles only):
  - alu: 8.0, data_transfer: 10.0, memory: 14.0, control: 16.0, stack: 18.0
- Weighted CPI for typical workload: 12.084 vs target 12.0
- Architecture: memory-to-memory with workspace pointers in external RAM

## Known Issues
- None significant. Model validates within 0.70% of target.
- Control (16.0) and stack (18.0) cycle counts are high, reflecting BLWP context switching cost.

## Suggested Next Steps
- Model is well-calibrated. No immediate changes needed.
- Could refine control category by splitting simple branches (lower cycles) from BLWP (higher cycles).
- Consider modeling the TMS9900 (16-bit bus) for family comparison.

## Key Architectural Notes
- Cost-reduced TMS9900: same ISA but 8-bit external data bus instead of 16-bit
- All "registers" are actually workspace memory locations accessed via workspace pointer (WP)
- Every 16-bit operation requires 2 bus cycles (byte-at-a-time access)
- BLWP (Branch and Load Workspace Pointer) is the context switch mechanism - very expensive
- No on-chip RAM: all workspace accesses go through the 8-bit external bus

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
