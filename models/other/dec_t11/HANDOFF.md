# DEC T-11 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.13%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: PDP-11 ISA, microcoded, 16-bit (1981)
- Clock: 2.5 MHz, 18,000 transistors, 16-bit address
- 5 instruction categories: alu(4.5c), data_transfer(4.5c), memory(7.0c), control(7.0c), stack(8.0c)
- Simple weighted-sum CPI model (no queueing overhead)
- Predicted typical CPI: 6.008 (target: 6.0)

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| typical | 6.008 | 0.1664 | 416,112 |
| compute | 5.795 | 0.1725 | 431,369 |
| memory | 5.795 | 0.1725 | 431,369 |
| control | 6.108 | 0.1637 | 409,299 |

## Known Issues
- None -- model passes validation with 0.13% error
- Compute and memory workloads produce identical CPI (could be differentiated)

## Suggested Next Steps
- Model is well-calibrated; no immediate changes needed
- Could add queueing overhead for bus contention modeling
- Could differentiate memory vs compute workload profiles more

## Key Architectural Notes
- Full PDP-11 ISA on a single chip (microcoded)
- Used in PDP-11/03 and military systems
- Microcoded design: 3-12 cycles for simple operations
- Much simpler than J-11 (18K vs 175K transistors, 2.5 vs 15 MHz)
