# NEC uPD612xA Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1983-1990
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Extended uCOM-4 architecture with integrated LCD controller
- On-chip LCD segment driver for consumer electronics
- 4-bit data path for low-power operation
- ROM-based program storage (4K ROM)
- Designed for calculators, watches, and LCD-based devices
- Higher cycle counts due to LCD controller overhead

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1983 |
| Clock | 0.5 MHz |
| Transistors | 3,500 |
| Data Width | 4-bit |
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
   - Extended uCOM-4 with dedicated LCD control instructions
   - Instruction categories: ALU (5c), data_transfer (6c), memory (8c), LCD (9c), control (7c), I/O (8c)
   - LCD segment control instructions are the most expensive at 9 cycles
   - Target CPI of 7.0 reflects LCD controller overhead added to base uCOM-4
   - LCD workloads dominate in typical calculator/display applications
   - Higher cycle counts than base uCOM-4 due to peripheral integration complexity

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against base uCOM-4 (uPD612x should have higher CPI due to LCD overhead)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd612x)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5COM-4)

---
Generated: 2026-01-29
