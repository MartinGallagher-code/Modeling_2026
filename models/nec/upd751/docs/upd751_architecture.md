# NEC uPD751 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1974-1982
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- NEC's early enhanced 4-bit microcontroller
- 4-bit data path with parallel ALU
- Variable instruction timing (7-9 cycles)
- Enhanced instruction set over uCOM-4
- BCD arithmetic support
- Used in consumer electronics and appliances
- More complex than uCOM-4 with additional addressing modes

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1974 |
| Clock | 0.4 MHz |
| Transistors | 8,500 |
| Data Width | 4-bit |
| Address Width | 11-bit |

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
   - Variable instruction timing unlike the uniform uCOM-4 (which has fixed 6-cycle timing)
   - Instruction categories: ALU/BCD (8c), data_transfer (7c), memory (9c), control (8c), I/O (7c)
   - Target CPI of 8.0 places it between uCOM-4 (CPI=6.0) and PPS-4 (CPI=12.0)
   - Memory operations are most expensive at 9 cycles due to additional addressing modes
   - Enhanced instruction set adds complexity, resulting in higher average cycle counts than uCOM-4
   - At 400 kHz clock, achieves ~50,000 instructions per second

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against uCOM-4 (CPI=6.0, simpler predecessor)
- Validate CPI falls between uCOM-4 and PPS-4 ranges
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd751)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5COM-4)

---
Generated: 2026-01-29
