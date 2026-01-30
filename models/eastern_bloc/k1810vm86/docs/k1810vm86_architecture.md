# K1810VM86 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Soviet clone of the Intel 8086 microprocessor
- 16-bit data bus, 20-bit address bus (1MB addressable)
- 6-byte instruction prefetch queue
- Segment-based memory model (CS, DS, SS, ES)
- Hardware multiply and divide instructions
- String operations with REP prefix
- Full Intel 8086 instruction set compatibility
- 2-200+ cycles per instruction (multiply/divide are very slow)
- Used in ES-1841 and other Soviet IBM PC clones

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1985 |
| Clock | 5.0 MHz |
| Transistors | ~29,000 |
| Data Width | 16-bit |
| Address Width | 20-bit |
| Process | NMOS |
| Western Equivalent | Intel 8086 |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Instruction timing identical to Intel 8086
   - 6-byte prefetch queue partially overlaps fetch with execution, but model treats as sequential for simplicity
   - Effective address (EA) calculation adds cycles to memory operand instructions
   - MUL 16-bit takes 118-133 cycles; DIV 16-bit takes 144-162 cycles
   - String operations with REP prefix modeled as ~12 cycles average per iteration
   - Target CPI of ~6.5 for typical workloads matches Intel 8086

## Validation Approach

- Compare against original Intel 8086 datasheet timing
- Validate with cycle-accurate 8086 emulator (if available)
- Cross-reference with ES-1841 technical documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/8086)
- [Wikipedia - Intel 8086](https://en.wikipedia.org/wiki/Intel_8086)

---
Generated: 2026-01-29
