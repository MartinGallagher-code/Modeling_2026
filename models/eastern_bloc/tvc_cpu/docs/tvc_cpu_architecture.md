# TVC CPU Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1983 (8-bit home computer era)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Hungarian modified Z80 clone by MEV/Tungsram
- 8-bit data bus, 16-bit address bus (64KB addressable)
- Z80-compatible instruction set
- Block transfer and search instructions
- Slightly optimized block operations vs standard Z80
- IX/IY index registers, alternate register set
- ~9,000 transistors, NMOS process

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MEV/Tungsram (Hungary) |
| Year | 1983 |
| Clock | 3.5 MHz |
| Transistors | ~9,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | Zilog Z80 (modified) |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->|  EXECUTE |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. Uses **Sequential Execution** template (Z80-based)
2. Minor improvements to block operation timing (11 vs 12 cycles)
3. Control flow slightly faster than standard Z80 (5 vs 6 cycles)
4. Used in the Videoton TVC home computer

## References

- [Videoton TVC](https://en.wikipedia.org/wiki/Videoton_TVC)
- [Zilog Z80](https://en.wikipedia.org/wiki/Zilog_Z80)

---
Generated: 2026-01-29
