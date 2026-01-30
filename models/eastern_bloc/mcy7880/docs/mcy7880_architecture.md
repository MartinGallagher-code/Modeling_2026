# MCY7880 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1979 (8-bit microprocessor era)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Polish clone of Intel 8080A microprocessor
- 8-bit data bus, 16-bit address bus (64KB addressable)
- Full Intel 8080A instruction set compatibility
- 7 8-bit registers (A, B, C, D, E, H, L) plus flags
- Stack pointer and program counter
- Interrupt system with RST instructions
- ~6,000 transistors, NMOS process

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | CEMI (Poland) |
| Year | 1979 |
| Clock | 2.0 MHz |
| Transistors | ~6,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | Intel 8080A |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->|  EXECUTE |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. Uses **Sequential Execution** template (identical to Intel 8080A)
2. T-state based timing converted to average cycle counts
3. Stack operations are particularly expensive (10 cycles avg)
4. Memory operations involve 16-bit address calculation overhead

## References

- [Intel 8080](https://en.wikipedia.org/wiki/Intel_8080)
- [CEMI Poland](https://en.wikipedia.org/wiki/CEMI)

---
Generated: 2026-01-29
