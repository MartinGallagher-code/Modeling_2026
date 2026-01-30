# NEC uPD7725 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Pipelined M/M/1 chain

## Architectural Features

- Enhanced NEC digital signal processor
- 16-bit data width with Harvard architecture
- Single-cycle MAC unit
- On-chip program and data ROM
- ~30,000 transistors in CMOS
- Used as SNES DSP-1 coprocessor

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1985 |
| Clock | 8.0 MHz |
| Transistors | ~30,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |

## Queueing Model Architecture

```
+---------+   +---------+   +---------+
|  FETCH  |-->| DECODE  |-->| EXECUTE |
+---------+   +---------+   +---------+
    |              |              |
    v              v              v
  M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue

Pipeline enables single-cycle MAC/ALU throughput
CPI = weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - MAC and ALU operations execute in single cycle
   - Data transfers require 2 cycles for register-memory movement
   - Control flow incurs 2-cycle branch penalty
   - External memory access is the slowest at 3 cycles
   - On-chip ROM eliminates program fetch penalties

## Validation Approach

- Compare against NEC uPD7725 datasheet specifications
- Validate with SNES DSP workload profiles
- Target: <5% CPI prediction error

## References

- [NEC uPD7725 Datasheet](TODO: Add link)
- [SNES Hardware Documentation](https://wiki.superfamicom.org/)

---
Generated: 2026-01-29
