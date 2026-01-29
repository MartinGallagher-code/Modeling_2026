# Stanford MIPS Model Handoff

## Current Status
- **Validation**: PASSED (13/13 tests, 100%)
- **CPI Error**: ~4%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: Original academic MIPS processor (Stanford, 1983)
5-stage pipeline with delayed branches and software-scheduled load delays.
Direct predecessor to MIPS R2000 (1986).

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 1.0 | ADD/SUB/AND/OR/XOR/SLT @1 cycle |
| load | 1.5 | LW/LH/LB @1.5 cycles (load delay slot) |
| store | 1.0 | SW/SH/SB @1 cycle (pipelined) |
| branch | 1.5 | BEQ/BNE @1.5 cycles (delay slot) |
| jump | 1.0 | J/JAL/JR @1 cycle (delay slot filled) |

**Performance:**
- Target CPI: 1.2
- Model CPI: 1.15
- At 2 MHz: ~1.74 MIPS

## Comparison to Berkeley RISC

| Feature | Stanford MIPS | Berkeley RISC I | Berkeley RISC II |
|---------|--------------|-----------------|------------------|
| Year | 1983 | 1982 | 1983 |
| CPI | 1.2 | 1.3 | 1.2 |
| Pipeline | 5-stage | 2-stage | 3-stage |
| Registers | 32 flat | 78 (6 windows) | 138 (8 windows) |
| Approach | Software scheduling | Register windows | Register windows |
| Descendant | MIPS R2000 | SPARC | SPARC |

## Cross-Validation

Method: Validation against Hennessy MIPS papers and comparison to Berkeley RISC
- All ALU ops single-cycle: verified
- 5-stage pipeline: verified
- CPI ~1.2 with realistic workload mix: verified

Comparative performance:
- ~8.3x lower CPI than VAX 11/780
- Comparable to Berkeley RISC II (~1.2)
- Foundation for commercial MIPS architecture

## Known Issues

None - model accurately reflects Stanford MIPS design.

## Suggested Next Steps

1. **Link to R2000** - Stanford MIPS directly led to MIPS R2000 (1986)
2. **Compare to R2000** - R2000 achieved CPI ~1.5 at higher clock
3. Model is well-validated

## Key Architectural Notes

- Original academic RISC processor from Stanford (Hennessy)
- MIPS = Microprocessor without Interlocked Pipeline Stages
- 5-stage pipeline: IF (Instruction Fetch), ID (Instruction Decode),
  EX (Execute), MEM (Memory), WB (Write Back)
- 32 general-purpose registers (r0 always zero)
- Delayed branches - instruction after branch always executes
- Load delay slots - software must schedule around load latency
- Hardwired control - no microcode
- ~25,000 transistors
- Different philosophy from Berkeley RISC:
  - MIPS: Move complexity to compiler (software scheduling)
  - RISC: Move complexity to hardware (register windows)

## MIPS Lineage

```
Stanford MIPS (1983)  <-- This model
    |
MIPS R2000 (1986) - First commercial MIPS
    |
MIPS R3000 (1988)
    |
MIPS R4000 (1991) - 64-bit
    |
MIPS R10000 (1996) - Out-of-order
```

Both Stanford MIPS and Berkeley RISC proved that RISC architectures
could achieve dramatically better performance than CISC designs,
leading to the RISC revolution of the late 1980s and 1990s.

See CHANGELOG.md for full history of all work on this model.
