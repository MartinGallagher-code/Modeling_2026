# NEC uPD546 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1975-1982
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Early NEC 4-bit microcontroller from the uCOM-4 family
- BCD (Binary Coded Decimal) arithmetic support
- Designed for calculators and consumer appliances
- Variable instruction timing (4-6.5 cycles)
- Small die size with minimal transistor count
- ROM-based program storage

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1975 |
| Clock | 0.5 MHz |
| Transistors | 3,500 |
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
   - Variable instruction timing unlike the uniform uCOM-4
   - Instruction categories: ALU/BCD (4.5c), data_transfer (4c), memory (5.5c), control (6.5c), I/O (5.5c)
   - BCD arithmetic optimized for calculator applications
   - Control flow instructions are slowest at 6.5 cycles (jump operations)
   - Weighted typical CPI depends on workload mix
   - At 500 kHz clock, achieves approximately 95,000-100,000 instructions per second

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against uCOM-4 family timing characteristics
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd546)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5COM-4)

---
Generated: 2026-01-29
