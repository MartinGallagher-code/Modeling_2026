# Intel 80C186 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.9%
- **Last Updated**: 2026-01-29

## Current Model Summary
- 6 instruction categories: alu (3c), data_transfer (2c), memory (8c), control (8c), stack (8c), multiply (25c)
- Memory stall model: memory_fraction * memory_latency(2) * 0.85
- M/M/1 queueing overhead on bus utilization
- 6-byte prefetch queue modeled
- Target CPI: 6.0, Model CPI: 5.943
- Clock: 8 MHz, ~55,000 transistors, CMOS (1982)

## Known Issues
- Prefetch queue is always the bottleneck (fixed at 0.70 utilization) which may be overly simplistic
- Compute workload CPI (7.167) is notably higher than typical due to 10% multiply weight at 25 cycles
- No separate validation targets for non-typical workloads

## Suggested Next Steps
- Model is validated and accurate; no immediate changes needed
- Could refine prefetch queue utilization to vary by workload
- Could add string operation and segment override categories for finer granularity

## Key Architectural Notes
- CMOS version of 80186; identical instruction set and timing to NMOS 80186
- Integrates clock generator, 2x DMA, 3x timers, interrupt controller, chip selects
- 8086-compatible instruction set with added ENTER/LEAVE, PUSHA/POPA, BOUND, etc.
- 20-bit address space (1 MB), 16-bit data bus
- Widely used in embedded/networking applications; billions shipped

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
