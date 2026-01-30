# Inmos T212 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.04% (typical workload)
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 16-bit transputer with CSP concurrency (1985), 15MHz clock
- 5 instruction categories (all cycles are base, no separate memory component):
  - alu: 1.5 cycles (single-cycle ALU at 1-2c)
  - data_transfer: 1.5 cycles (register moves at 1-2c)
  - memory: 3.0 cycles (memory ops at 2-4c)
  - control: 4.0 cycles (branch/process at 3-6c)
  - stack: 3.5 cycles (stack ops at 3-4c)
- No queueing overhead applied; CPI is purely weighted average
- 4KB on-chip SRAM, 75K transistors, 32-bit address space

## All Workload Results
| Workload | CPI | IPC | Error | Status |
|----------|-----|-----|-------|--------|
| typical | 2.499 | 0.400 | 0.04% | PASS |
| compute | 2.349 | 0.426 | 6.0% | MARGINAL |
| memory | 2.349 | 0.426 | 6.0% | MARGINAL |
| control | 2.662 | 0.376 | 6.5% | MARGINAL |

## Known Issues
- Compute and memory workloads have ~6% error (slightly above 5% threshold)
- Control workload has 6.5% error due to control ops being 4.0 cycles (heavier than average)
- No queueing overhead is modeled; the simple weighted average suffices for typical workload

## Suggested Next Steps
- To improve compute workload: could slightly increase ALU base_cycles from 1.5 toward 1.7
- To improve control workload: could reduce control base_cycles from 4.0 toward 3.5
- Both changes would affect typical workload accuracy, so careful rebalancing would be needed
- Consider adding a small process scheduling overhead factor for non-typical workloads

## Key Architectural Notes
- Stack-based architecture (3-register evaluation stack)
- Hardware process scheduler with CSP-style channel communication
- 4KB on-chip SRAM for workspace
- Designed for Occam programming language
- 16-bit data width, 32-bit address space

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
