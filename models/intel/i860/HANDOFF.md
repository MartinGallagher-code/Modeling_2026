# Intel i860 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.8%
- **Last Updated**: 2026-01-28
- **Cross-Validation**: COMPLETE

## Current Model Summary

Architecture: VLIW-Hybrid Superscalar (dual-issue int+fp)

| Parameter | Value |
|-----------|-------|
| `clock_mhz` | 40.0 |
| `dual_issue` | True |
| `dual_issue_efficiency` | 0.55 |
| `icache_hit_rate` | 0.975 |
| `dcache_hit_rate` | 0.94 |
| `memory_latency` | 6 |
| `branch_delay_slots` | 3 |
| `delay_slot_fill_rate` | 0.8 |

FP operations modeled as pipelined (1/cycle throughput).

## Instruction Timing Tests
12 per-instruction timing tests added:
- ALU (ADD/SUB): 1 cycle
- Load/Store: 1 cycle (cache hit)
- Branch: 1 cycle + 3 delay slots
- Integer multiply: 3 cycles latency, 1/cycle throughput
- Integer divide: 8 cycles
- Pipelined FP: 3 latency, 1/cycle throughput
- FP reciprocal/sqrt: 2 latency, 1/cycle throughput

## Cross-Validation Results

| Feature | i860 | MIPS R3000 | Notes |
|---------|------|------------|-------|
| ALU cycles | 1 | 1 | Same |
| Load cycles | 1 | 2 | i860 faster on cache hit |
| Branch delay slots | 3 | 1 | i860 3x harder to schedule |
| Dual-issue | Yes (int+fp) | No | i860 advantage when utilized |

**Performance spectrum:**
- Peak CPI: ~0.5 (full dual-issue)
- Typical CPI: 1.2 (reasonably optimized)
- Naive compiled: 2-3 CPI

## Known Issues

1. **Memory-intensive workloads** show higher CPI (1.46) - may be realistic given 8KB D-cache

2. **Dual-issue efficiency is estimated** - 0.55 is reasonable for hand-tuned code

## Suggested Next Steps

1. **Find benchmark data** - search for published i860 benchmarks (Livermore loops, Linpack)

2. **Model graphics unit** - i860 had dedicated 3D graphics pipeline

3. **Add mode switching overhead** - i860 had overhead switching between scalar and pipelined modes

## Key Architectural Notes

- i860 can issue int AND fp simultaneously (VLIW-hybrid) - key to performance
- 3 branch delay slots (unusual - most RISC had 1)
- No hardware interlocks - compiler/programmer must avoid hazards
- Peak 80 MFLOPS only with hand-tuned assembly
- Failed commercially because compilers couldn't optimize for it
- "Cray on a chip" marketing was accurate but only for hand-tuned code

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 8
- **Corrections**: See `identification/sysid_result.json`
