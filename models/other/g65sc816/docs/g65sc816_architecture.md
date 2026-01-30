# GTE G65SC816 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- WDC 65C816 second-source with full 65816 pinout
- 8/16-bit switchable registers in native mode
- 24-bit address space (16 MB) via address/data bus multiplexing
- CMOS technology for low power
- Used in Apple IIGS and other 65816-based systems
- Full native mode operation (not limited to emulation mode)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | GTE Microcircuits |
| Year | 1985 |
| Clock | 4.0 MHz |
| Transistors | 22,000 |
| Data Width | 16-bit |
| Address Width | 24-bit |

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
   - Target CPI of 3.8 (slightly higher than G65SC802 due to full addressing)
   - ALU operations fastest at 2 cycles (16-bit native)
   - Data transfer at 3 cycles (16-bit LDA/STA)
   - Memory operations at 4 cycles (indirect, indexed modes)
   - Control flow at 3 cycles (BNE, JMP, JSR)
   - Stack and long addressing modes are slowest at 5 cycles each
   - Multiplexed bus adds a cycle to memory stage vs G65SC802
   - 25% of typical workload uses long (24-bit) addressing

## Validation Approach

- Compare against WDC 65C816 datasheet timing
- Validate with Apple IIGS benchmark data
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/WDC_65C816)

---
Generated: 2026-01-29
