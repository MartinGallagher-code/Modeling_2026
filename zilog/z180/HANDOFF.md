# Z180 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.89%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Clock: 6.0 MHz (up to 20 MHz in later variants)
- Architecture: 8-bit, Z80-compatible, CMOS with optimized timing
- Expected CPI: 4.5
- Predicted CPI: 4.585
- Typical IPS: ~1.31 MIPS
- Timing Tests: 17 per-instruction tests added

Key instruction categories (optimized vs Z80):
| Category | Cycles | Z80 Equiv | Optimization |
|----------|--------|-----------|--------------|
| alu | 3.2 | 4.0 | 20% faster |
| data_transfer | 3.2 | 4.0 | 20% faster |
| memory | 4.8 | 5.8 | 17% faster |
| control | 4.5 | 5.5 | 18% faster |
| stack | 8.5 | 10.0 | 15% faster |
| block | 10.0 | 12.0 | 17% faster |

## Known Issues
- None - model is fully validated
- Per-instruction accuracy varies due to category averaging (expected behavior)
- MLT instruction not weighted heavily (rare in typical code)

## Suggested Next Steps
- Could model on-chip DMA separately for DMA-heavy workloads
- Could add MMU address translation overhead if needed
- UART/timer peripheral modeling if interrupt latency is important

## Key Architectural Notes
- Z180 is enhanced Z80 with faster execution (1-2 cycles per instruction)
- CMOS technology (vs Z80's NMOS)
- Binary compatible with Z80 instruction set
- On-chip peripherals don't affect instruction timing

## On-Chip Enhancements
- MMU: 1MB address space (vs Z80's 64KB)
- DMA: 2 channels
- UART (ASCI): 2 channels
- Timers: 2 programmable
- Wait state generator
- Clock prescaler

## Cross-Validation Summary
- Methodology: Grey-box queueing model with Z80-derived timing, reduced by 18% avg
- Timing verified against Z180 datasheet (ps0140.pdf)
- Z180-specific instructions (MLT, SLP, IN0/OUT0) documented
- CPI accuracy: 1.89% error on typical workload

## Related Models
- Z80/Z80A/Z80B: Base architecture, slower timing
- Z180 trades higher transistor count for faster execution

## Files
- Model: `current/z180_validated.py`
- Validation: `validation/z180_validation.json`
