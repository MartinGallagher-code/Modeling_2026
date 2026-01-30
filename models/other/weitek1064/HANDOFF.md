# Weitek 1064/1065 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.5%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: Pipelined FPU pair (1985), 15MHz clock
- 7 instruction categories: fp_add (2.5+0.5), fp_multiply (3.0+0.5), fp_divide (8.0+0.5), fp_sqrt (10.0+0.5), int_alu (1.5+0), data_transfer (1.5+1.5), format_convert (2.5+0.5)
- 4-stage pipeline with throughput factor 0.82
- Queueing overhead: 1.0 + rho * 0.08
- Predicted typical CPI: 2.924 (target: 3.0)

## Known Issues
- Compute workload is marginal at 13.6% error (heavy FP divide/sqrt)
- Memory workload is marginal at 7.6% error

## Suggested Next Steps
- Model is well-calibrated for typical use; no immediate changes needed
- Could investigate pipeline stall behavior for back-to-back dependent operations

## Key Architectural Notes
- Coordinated FPU pair: 1064 handles integer ALU and FP add/subtract, 1065 handles FP multiply
- ECL/CMOS technology, ~40000 transistors
- Used in high-end workstations and Cray systems
- IEEE 754 compliant floating point

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
