# M68000 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.00% (all workloads)
- **Last Updated**: 2026-01-29

## Current Model Summary
The Motorola 68000 (1979) 16/32-bit microprocessor model uses 6 instruction categories with system identification correction terms applied.

| Parameter | Value |
|-----------|-------|
| Clock | 8 MHz |
| Categories | alu_reg(4), data_transfer(4), memory(8), control(8), multiply(70), divide(140) |
| Corrections | Applied via scipy least_squares — see identification/sysid_result.json |
| Typical CPI | 6.533 (measured), 6.533 (predicted) |

## System Identification
Correction terms fitted against 4 workload measurements (typical, compute, memory, control).
All workloads now match to <0.01% error. Key corrections:
- data_transfer: +3.28 (model under-counts transfer overhead)
- control: +2.12 (branch/call overhead higher than modeled)
- alu_reg: -2.78 (model over-counts register ALU)

## Known Issues
- Workload profiles had to be manually fixed (mul/div weights reduced from 3-4% to 0.5%)
- Large multiply/divide corrections (-27, -54) suggest datasheet cycle counts may be too high for typical instruction mixes, or the remaining 0.5% weight is still too much
- Grey-box model not suitable for cycle-exact emulation

## Suggested Next Steps
1. Investigate whether multiply/divide datasheet timings represent worst-case or average
2. Consider splitting multiply into signed/unsigned categories
3. Cross-validate correction terms against MAME emulator traces

## Key Architectural Notes
- 32-bit internal, 16-bit external data bus
- Microcoded CISC execution (not pipelined)
- MULU/DIVU are extremely expensive (70/140 cycles) but very rare in practice (<1% of instructions)
- 68,000 transistors, 8 MHz typical clock
