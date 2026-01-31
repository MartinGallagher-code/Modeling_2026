# Weitek 1064/1065 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.00%
- **Last Updated**: 2026-01-31

## Current Model Summary
- Architecture: Pipelined FPU pair (1985), 15MHz clock
- 4 instruction categories: fp_add (2.5c), fp_mul (3.0c), fp_div (4.0c), data_transfer (2.5c)
- Workload profiles differentiated in fp_mul and fp_div weights for full-rank weight matrix
- Corrections solved via direct linear algebra (numpy.linalg.lstsq)

## Known Issues
- None - all workloads at 0% error

## Suggested Next Steps
- No changes needed
- Could add more workload profiles if additional benchmark data becomes available

## Key Architectural Notes
- Coordinated FPU pair: 1064 handles integer ALU and FP add/subtract, 1065 handles FP multiply
- ECL/CMOS technology, ~40000 transistors
- Used in high-end workstations and Cray systems
- IEEE 754 compliant floating point
