# DEC T-11 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1981)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- PDP-11 on a chip (full PDP-11 ISA implementation)
- Microcoded architecture
- Military-grade versions available
- 18,000 transistors
- Used in PDP-11/03 and military/embedded systems
- Full PDP-11 addressing modes support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | DEC |
| Year | 1981 |
| Clock | 2.5 MHz |
| Transistors | 18,000 |
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
   - Target CPI of 6.0 reflects microcoded execution
   - ALU and data transfer operations take 4.5 cycles
   - Memory operations at 7 cycles (complex addressing modes)
   - Control flow at 7 cycles (branch/JSR with pipeline flush)
   - Stack operations most expensive at 8 cycles
   - Significantly slower than the pipelined J-11 successor

## Validation Approach

- Compare against original DEC T-11 datasheet
- Validate with PDP-11/03 benchmark data
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/T-11)

---
Generated: 2026-01-29
