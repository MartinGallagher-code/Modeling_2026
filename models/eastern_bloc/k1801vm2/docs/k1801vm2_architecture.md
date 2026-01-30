# K1801VM2 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1983 (enhanced single-chip PDP-11)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Enhanced Soviet PDP-11 compatible microprocessor
- 16-bit data bus, 16-bit address bus (64KB addressable)
- Full PDP-11 instruction set with floating point support
- 8 general-purpose 16-bit registers
- Improved execution speed over K1801VM1
- Higher clock frequency (8 MHz vs 5 MHz)
- ~25,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1983 |
| Clock | 8.0 MHz |
| Transistors | ~25,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | DEC PDP-11 (enhanced single-chip) |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->|  EXECUTE |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. Uses **Sequential Execution** template with improved timing
2. Key improvements over K1801VM1:
   - Faster ALU operations (2 vs 3 cycles)
   - Faster data transfers (3 vs 4 cycles)
   - Added floating point support (10 cycles)
   - Higher clock (8 MHz vs 5 MHz)

## References

- [PDP-11 Architecture](https://en.wikipedia.org/wiki/PDP-11_architecture)
- [DVK Computer Series](https://en.wikipedia.org/wiki/DVK)

---
Generated: 2026-01-29
