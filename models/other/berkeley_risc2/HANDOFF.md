# Berkeley RISC II Model Handoff

## Current Status
- **Validation**: PASSED (13/13 tests, 100%)
- **CPI Error**: ~0.4%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: Improved RISC processor (1983)
3-stage pipeline with register windows and delayed branches.
Direct predecessor to Sun SPARC architecture.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 1.0 | ADD/SUB/AND/OR/XOR @1 cycle |
| load | 2.0 | LDW/LDHU/LDBU @2 cycles (memory access) |
| store | 1.5 | STW/STH/STB @1.5 cycles (write buffer) |
| branch | 2.0 | Branch @2 cycles (with delay slot) |
| call | 1.0 | CALL/RET @1 cycle (register window switch) |

**Performance:**
- Target CPI: 1.2
- Model CPI: 1.205
- At 3 MHz: ~2.5 MIPS

## Comparison to RISC I

| Feature | RISC I | RISC II | Improvement |
|---------|--------|---------|-------------|
| Year | 1982 | 1983 | - |
| CPI | 1.3 | 1.2 | ~8% |
| Pipeline | 2-stage | 3-stage | Better throughput |
| Register windows | 6 | 8 | Fewer overflows |
| Total registers | 78 | 138 | More local storage |
| Transistors | 44,500 | 40,760 | More efficient |
| Clock | 4 MHz | 3 MHz | - |
| Store cycles | 2 | 1.5 | Write buffer |

## Cross-Validation

Method: Validation against Patterson & Sequin RISC II papers
- All ALU ops single-cycle: verified
- Load 2-cycle: verified
- Store 1.5-cycle (write buffer): verified
- CPI ~1.2 with realistic workload mix: verified

Comparative performance:
- ~8.4x lower CPI than VAX 11/780
- ~8% lower CPI than RISC I
- Foundation for Sun SPARC architecture

## Known Issues

None - model accurately reflects RISC II design improvements.

## Suggested Next Steps

1. **Link to SPARC lineage** - RISC II directly influenced Sun SPARC (1987)
2. **Stanford MIPS comparison** - Contemporary competitor from Stanford
3. Model is well-validated

## Key Architectural Notes

- Second RISC processor from UC Berkeley (Patterson & Sequin)
- 3-stage pipeline (improved from RISC I's 2-stage)
- 138 registers with 8 overlapping windows of 32 registers each
- Delayed branches - instruction after branch always executes
- Load/store architecture - only loads and stores access memory
- 39 instructions total (expanded from RISC I's 31)
- 40,760 transistors (more efficient than RISC I)
- Direct ancestor of Sun SPARC architecture (1987)
- Influenced MIPS, ARM, and modern RISC designs
- Key innovations: write buffer for stores, more register windows

## SPARC Lineage

```
Berkeley RISC I (1982)
    |
Berkeley RISC II (1983)  <-- This model
    |
Sun SPARC (1987)
    |
SPARC V7/V8/V9 (1990s)
```

RISC II's register window design was directly adopted by Sun for SPARC,
making it one of the most influential processor designs in history.

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
