# Intel i860 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.8%
- **Last Updated**: 2026-01-28

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

## Known Issues

1. **Memory-intensive workloads** show higher CPI (1.46) - may be realistic given 8KB D-cache, but could use validation data

2. **Bottleneck always shows icache** - 4KB I-cache is the limiting factor; seems architecturally correct but worth verifying

3. **Dual-issue efficiency is estimated** - 0.55 is reasonable for hand-tuned code, but varied by programmer skill

## Suggested Next Steps

1. **Find benchmark data** - search for published i860 benchmarks (Livermore loops, Linpack) to validate against real measurements

2. **Model graphics unit** - i860 had dedicated 3D graphics pipeline; could add `graphics` workload profile

3. **Add mode switching overhead** - i860 had overhead switching between scalar and pipelined modes

4. **Model cache management** - i860 required manual cache control; could add flush/invalidate overhead

## Key Architectural Notes

- i860 can issue int AND fp simultaneously (VLIW-hybrid) - this is the key to its performance
- 3 branch delay slots (unusual - most RISC had 1)
- No hardware interlocks - compiler/programmer must avoid hazards
- Peak 80 MFLOPS only with hand-tuned assembly
- Failed commercially because compilers couldn't optimize for it
- Expected CPI 1.2 = "reasonably optimized" code
- Peak CPI ~0.5 = full dual-issue utilization
- Naive compiled code = CPI 2-3

See CHANGELOG.md for full history of all work on this model.
