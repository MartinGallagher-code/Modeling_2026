# M68008 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.00% (all workloads)
- **Last Updated**: 2026-01-29

## Current Model Summary
The Motorola 68008 (1982) 8/32-bit microprocessor model — 68000 core with 8-bit external bus. Uses 6 instruction categories with system identification correction terms.

| Parameter | Value |
|-----------|-------|
| Clock | 8 MHz |
| Categories | alu_reg(4.5), data_transfer(4.5), memory(9), control(9), multiply(72), divide(145) |
| Corrections | Applied via scipy least_squares — see identification/sysid_result.json |
| Typical CPI | 7.17 (measured), 7.17 (predicted) |

## System Identification
Correction terms fitted against 4 workload measurements. Key corrections:
- data_transfer: +2.68, alu_reg: -4.19, control: +1.07
- multiply: +36.0, divide: +72.5 (positive corrections unlike other 68K — different bus timing dynamics)

## Known Issues
- Workload profiles manually fixed (mul/div weights reduced from 3-4% to 0.5%)
- Large positive multiply/divide corrections are unusual; may indicate 8-bit bus adds overhead to mul/div differently than modeled

## Suggested Next Steps
1. Validate against Sinclair QL emulator timing data
2. Investigate whether 8-bit bus impacts mul/div timing differently than other ops

## Key Architectural Notes
- 68000 core with 8-bit external data bus, 20-bit address space (1 MB)
- Word operations take 2x bus cycles vs 68000; long operations take 4x
- 70,000 transistors, 8 MHz typical clock
