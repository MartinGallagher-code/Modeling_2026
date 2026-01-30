# Intersil 6100 (IM6100) Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1975)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- CMOS PDP-8/E instruction set implementation (PDP-8 on a chip)
- 12-bit word size
- Variable instruction timing (6-22 states per instruction)
- Fully static CMOS design (can halt clock indefinitely)
- 8 basic instructions (PDP-8/E compatible)
- Direct, indirect, and autoindex addressing modes
- 4K word address space (expandable to 32K)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intersil |
| Year | 1975 |
| Clock | 4.0 MHz |
| Transistors | 4,000 |
| Data Width | 12-bit |
| Address Width | 12-bit |

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
   - Target CPI of 10.5 states (weighted average of all instructions)
   - Arithmetic (TAD) and logic (AND) at 10 states (direct), 15 indirect
   - Memory operations (DCA, ISZ) at 12 states average
   - Jump operations (JMP, JMS) at 12 states
   - I/O (IOT) at 12 states
   - Operate (OPR) group is fastest at 6 states
   - Each state = 500ns at 4 MHz (2 clock cycles per state)
   - Expected ~190 KIPS throughput

## Validation Approach

- Compare against original Intersil IM6100 datasheet
- Validate with known PDP-8 software timing
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Intersil_6100)

---
Generated: 2026-01-29
