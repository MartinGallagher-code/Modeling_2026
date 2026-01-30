# Berkeley RISC I Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: First RISC processor (1982)
2-stage pipeline with register windows and delayed branches.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 1 | ADD/SUB/AND/OR @1 cycle |
| load | 2 | LDW @2 cycles (memory access) |
| store | 2 | STW @2 cycles (memory access) |
| branch | 1 | Branch @1 cycle (delay slot filled) |
| call | 1 | CALL @1 cycle (register window switch) |

**Performance:**
- Target CPI: 1.3
- Model CPI: 1.3
- At 4 MHz: ~3 MIPS

## Cross-Validation

Method: Validation against Patterson & Sequin RISC I papers
- All ALU ops single-cycle: verified
- Load/store 2-cycle: verified
- CPI ~1.3 with realistic workload mix: verified

Comparative performance:
- ~7.7x lower CPI than VAX 11/780
- ~4x lower CPI than Zilog Z8000
- ~3x lower CPI than MC68000

## Known Issues

None - model accurately reflects RISC I design principles.

## Suggested Next Steps

1. **Berkeley RISC II model** - improved version with better performance
2. **Link to SPARC lineage** - RISC I directly influenced Sun SPARC
3. Model is well-validated

## Key Architectural Notes

- First RISC processor from UC Berkeley (Patterson & Sequin)
- 2-stage pipeline (simple but effective)
- 78 registers with 6 overlapping windows of 14 registers each
- Delayed branches - instruction after branch always executes
- Load/store architecture - only loads and stores access memory
- 31 instructions total (vs hundreds in CISC)
- 44,500 transistors (vs 100K+ for comparable CISC)
- Direct ancestor of Sun SPARC architecture
- Influenced ARM design philosophy

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
