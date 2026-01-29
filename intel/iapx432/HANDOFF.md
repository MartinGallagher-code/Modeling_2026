# Intel iAPX 432 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 3.5%
- **Last Updated**: 2026-01-28
- **Cross-Validation**: COMPLETE

## Current Model Summary
- Architecture: 32-bit capability-based object-oriented (multi-chip)
- Year: 1981
- Clock: 8.0 MHz
- Target CPI: 50.0
- Predicted CPI: 48.25
- Instruction categories: alu, data_transfer, memory, control, object_ops

## Instruction Timing Tests
12 per-instruction timing tests added:
- ALU with capability check: 25 cycles (documented: 20-30)
- Data transfer: 35 cycles (documented: 30-45)
- Memory with capability: 60 cycles (documented: 50-75)
- Control flow: 50 cycles (documented: 40-80)
- Object operations: 120 cycles (documented: 80-400+)
- Rights verification: 25 cycles (documented: 15-35)

## Cross-Validation Results

| Operation | iAPX 432 | 8086 | Ratio |
|-----------|----------|------|-------|
| ALU | 25 | 3 | 8.3x slower |
| Data transfer | 35 | 4 | 8.75x slower |
| Memory access | 60 | 10 | 6.0x slower |
| Branch | 50 | 16 | 3.1x slower |

The 5-10x slowdown vs 8086 is well-documented and explains the commercial failure.

## Known Issues
- None - model validates within 5% error
- Object deletion cycles (80-400+) have wide variance due to garbage collection

## Suggested Next Steps
- No changes needed unless better documentation emerges
- Could add Ada-specific workload profile

## Key Architectural Notes
- Every operation includes capability checking overhead
- Hardware support for garbage collection made object ops expensive
- Designed specifically for Ada language support
- Commercial failure led Intel to abandon capability-based approach
- 80286's simpler protected mode won the market
- Considered one of the biggest failures in CPU history

**Why it failed:**
1. 5-10x slower than 8086 despite more transistors
2. Capability checking on every memory access
3. Complex multi-chip design
4. Ada focus limited market appeal

See CHANGELOG.md for full history of all work on this model.
