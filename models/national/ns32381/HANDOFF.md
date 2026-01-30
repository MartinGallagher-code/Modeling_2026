# National NS32381 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.5%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Clock: 15.0 MHz, ~60K transistors, pipelined FP execution
- 7 instruction categories: fp_add (6.5), fp_mul (8.5), fp_div (26.5), fp_sqrt (36.5), fp_compare (5.5), data_transfer (4.0), format_convert (5.5)
- Pipeline benefit factor: 0.93 applied to base CPI
- Queueing overhead: rho * 0.06 factor based on bottleneck utilization
- Target CPI: 8.0, Model CPI: 8.042

## Known Issues
- Compute workload CPI (10.376) is significantly higher than typical (8.042), reflecting heavy div/sqrt usage
- Memory workload CPI (5.949) is much lower since data_transfer has only 4.0 total cycles
- The large CPI spread across workloads may warrant per-workload validation targets

## Suggested Next Steps
- Consider adding per-workload target CPIs for more nuanced validation
- Verify pipeline benefit factor (0.93) against actual NS32381 pipeline depth documentation
- The divider utilization metric could be refined with actual divider occupancy data

## Key Architectural Notes
- This is a floating-point coprocessor (slave processor), not a standalone CPU
- Communicates with NS32032/NS32332 CPU via slave bus protocol
- All instruction categories include 1.5 memory_cycles for slave bus communication overhead
- Pipeline benefit reduces effective CPI by 7% from base weighted average
- FP divide (25 cycles) and sqrt (35 cycles) dominate compute-heavy workloads

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
