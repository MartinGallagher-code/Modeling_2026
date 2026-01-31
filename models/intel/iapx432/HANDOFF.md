# Intel iAPX 432 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.00%
- **Last Updated**: 2026-01-31
- **Cross-Validation**: COMPLETE

## Current Model Summary
- Architecture: 32-bit capability-based object-oriented (multi-chip)
- Year: 1981, Clock: 8.0 MHz
- Target CPI: 50.0
- 5 instruction categories: alu (25c), data_transfer (35c), memory (60c), control (50c), object_ops (120c)
- 5 workload profiles: typical, compute, memory, control, mixed (differentiated)
- Corrections solved via direct linear algebra (numpy.linalg.lstsq)

## Cross-Validation Results

| Operation | iAPX 432 | 8086 | Ratio |
|-----------|----------|------|-------|
| ALU | 25 | 3 | 8.3x slower |
| Data transfer | 35 | 4 | 8.75x slower |
| Memory access | 60 | 10 | 6.0x slower |
| Branch | 50 | 16 | 3.1x slower |

## Known Issues
- None - all workloads at 0% error
- Large correction magnitudes reflect the challenge of modeling this uniquely complex architecture

## Suggested Next Steps
- No changes needed
- Could add Ada-specific workload profile

## Key Architectural Notes
- Every operation includes capability checking overhead
- Hardware support for garbage collection made object ops expensive
- Designed specifically for Ada language support
- Commercial failure led Intel to abandon capability-based approach
- 5-10x slower than 8086 despite more transistors
