# WISC CPU/16 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1986)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Writable Instruction Set Computer (WISC) -- user-definable instruction set
- 16-bit stack-oriented architecture
- TTL discrete logic construction (board-level, not monolithic)
- Fully RAM-based microcode (writable control store)
- Stack machine design (Forth-like operation)
- User can redefine instruction set at runtime
- Phil Koopman's research architecture at Carnegie Mellon University
- 4 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Phil Koopman (Carnegie Mellon) |
| Year | 1986 |
| Clock | 4.0 MHz |
| Transistors | N/A (TTL discrete) |
| Data Width | 16-bit |
| Address Width | 16-bit |

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
   - Stack operations (push/pop/dup/swap) are fast at 2 cycles
   - ALU operations (add/sub/and/or) also 2 cycles
   - Memory load/store costs 3 cycles
   - Control flow (branch/call/return) costs 3 cycles
   - Custom microcode instructions average 2.5 cycles
   - Target CPI: ~2.5 (stack machines are inherently efficient)
   - Writable microcode allows instruction set optimization per application
   - Stack architecture eliminates register allocation overhead

## Validation Approach

- Compare against Phil Koopman's published WISC research papers
- Validate against Forth benchmark execution times
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/wisc/cpu16)
- [Wikipedia](https://en.wikipedia.org/wiki/Stack_machine)

---
Generated: 2026-01-29
