# Intel iWarp Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.5%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: VLIW/systolic array, dual-issue, 32-bit (1985)
- Clock: 20.0 MHz
- 7 instruction categories: alu_int(1c), multiply(3c), fp_add(2c), fp_mul(3c), load_store(1c), branch(1c), comm(2c)
- Dual-issue with 80% efficiency (effective width 1.80)
- SRAM hit rate: 85%, external memory penalty: 8 cycles
- Branch penalty: 3 cycles at 50% mispredict rate
- Communication overhead: 2 cycles at 30% rate
- Queueing factor: 15% when utilization > 50%
- Predicted typical CPI: 1.508 (target: 1.5)

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| typical | 1.508 | 0.6631 | 13,262,599 |
| compute | 1.591 | 0.6287 | 12,573,081 |
| memory | 1.698 | 0.5891 | 11,782,032 |
| control | 1.429 | 0.6996 | 13,991,885 |

## Known Issues
- None significant - model is well-calibrated

## Suggested Next Steps
- No changes needed - model passes with excellent 0.5% error
- One of the best-calibrated models in the collection

## Key Architectural Notes
- Intel/CMU joint design, precursor to modern GPU thinking
- Dual-issue: computation agent + communication agent
- Systolic array communication between nodes
- VLIW instruction format
