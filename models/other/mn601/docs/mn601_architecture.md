# Data General mN601 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1977)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Single-chip implementation of Data General's Nova minicomputer architecture
- Also known as microNova
- Accumulator-based architecture inherited from Nova
- Skip instructions for conditional execution (Nova heritage)
- Stack operations for subroutine support
- I/O instructions for peripheral control
- 4 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Data General |
| Year | 1977 |
| Clock | 4.0 MHz |
| Transistors | N/A |
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
   - Efficient Nova architecture with good cycle performance
   - ALU operations fastest at 3.0 cycles
   - Memory read and I/O at 5.0 cycles; memory write at 4.0 cycles
   - Jump and skip instructions at 4.0 cycles each
   - Stack operations slowest at 6.0 cycles
   - Target CPI of 4.0 reflects Nova's efficient instruction set
   - 8 instruction categories model Nova's diverse instruction types

## Validation Approach

- Compare against original Data General datasheet
- Cross-validate against Nova minicomputer performance data
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/data_general)
- [Wikipedia](https://en.wikipedia.org/wiki/Data_General_microNova)

---
Generated: 2026-01-29
