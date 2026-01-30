# Western Digital WD16 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1977)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- DEC PDP-11 compatible microprocessor in a single chip
- LSI-11 instruction set compatibility
- 16-bit data path
- Register-to-register, immediate, memory, and byte operations
- Subroutine call/return (JSR/RTS) support
- Trap/interrupt handling
- Designed for embedded systems and minicomputer replacement
- 3.3 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Western Digital |
| Year | 1977 |
| Clock | 3.3 MHz |
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
   - PDP-11 compatible instruction set with variable-length instructions
   - Register operations are fastest at 3 cycles
   - Immediate and branch operations average 5 cycles
   - Memory read/write and JSR operations cost 6 cycles
   - Byte operations average 5 cycles
   - Trap/interrupt handling is most expensive at 8 cycles
   - Target CPI: ~5.0 for typical embedded workloads
   - Complex instruction set leads to higher average CPI than simpler 8-bit CPUs

## Validation Approach

- Compare against original Western Digital datasheet
- Cross-validate with DEC PDP-11 timing documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/western_digital/wd16)
- [Wikipedia](https://en.wikipedia.org/wiki/Western_Digital#Early_products)

---
Generated: 2026-01-29
