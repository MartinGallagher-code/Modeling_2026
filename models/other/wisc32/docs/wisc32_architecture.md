# WISC CPU/32 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1980s (1988)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 32-bit evolution of the WISC CPU/16
- Writable Instruction Set Computer -- user-definable instruction set
- 32-bit stack-oriented architecture with wider data path
- TTL discrete logic construction (board-level)
- RAM-based writable microcode store
- Improved microcode engine over CPU/16
- Phil Koopman's research architecture at Carnegie Mellon University
- 8 MHz clock (2x the CPU/16)
- Lower CPI than CPU/16 due to architectural optimizations

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Phil Koopman (Carnegie Mellon) |
| Year | 1988 |
| Clock | 8.0 MHz |
| Transistors | N/A (TTL discrete) |
| Data Width | 32-bit |
| Address Width | 32-bit |

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
   - Stack operations (push/pop/dup/swap) at 1.5 cycles (faster than CPU/16)
   - 32-bit ALU operations at 1.5 cycles
   - Memory load/store costs 2.5 cycles
   - Control flow (branch/call/return) costs 2.5 cycles
   - Custom microcode instructions average 2.0 cycles
   - Target CPI: ~2.0 (improved over CPU/16's 2.5)
   - Wider data path reduces multi-cycle operations
   - 2x clock speed and lower CPI give significant speedup over CPU/16

## Validation Approach

- Compare against Phil Koopman's published WISC research papers
- Validate CPI is lower than WISC CPU/16 (target 2.0 vs 2.5)
- Validate against Forth benchmark execution times
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/wisc/cpu32)
- [Wikipedia](https://en.wikipedia.org/wiki/Stack_machine)

---
Generated: 2026-01-29
