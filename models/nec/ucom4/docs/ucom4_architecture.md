# NEC uCOM-4 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1972-1980
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- NEC's first microcontroller design
- 4-bit data path with parallel ALU
- Harvard architecture (separate program/data memory)
- Fixed-cycle instruction timing (all instructions 6 cycles)
- Competitor to TI TMS1000
- Used in calculators, watches, and consumer electronics
- Japanese alternative to American microcontrollers

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1972 |
| Clock | 0.4 MHz |
| Transistors | 7,500 |
| Data Width | 4-bit |
| Address Width | 10-bit |

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
   - Fixed 6-cycle timing for all instruction categories (ALU, data_transfer, memory, control, I/O)
   - CPI is constant at 6.0 regardless of workload mix
   - Similar performance characteristics to TI TMS1000 (same CPI target)
   - At 400 kHz clock, achieves ~66,667 instructions per second
   - Harvard architecture provides separate instruction and data paths
   - Simplicity of fixed timing reflects the era's uniform instruction execution

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against TI TMS1000 (CPI = 6.0, comparable 4-bit MCU)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/ucom-4)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5COM-4)

---
Generated: 2026-01-29
