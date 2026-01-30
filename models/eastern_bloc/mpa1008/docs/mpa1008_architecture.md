# MPA1008 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980s (8-bit microprocessor era)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Romanian clone of Zilog Z80A microprocessor
- 8-bit data bus, 16-bit address bus (64KB addressable)
- Full Z80 instruction set including:
  - Block transfer instructions (LDIR, LDDR)
  - Block search instructions (CPIR, CPDR)
  - Bit manipulation instructions
  - IX/IY index registers
  - Alternate register set (shadow registers)
- ~8,500 transistors, NMOS process

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Romania |
| Year | 1982 |
| Clock | 2.5 MHz |
| Transistors | ~8,500 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | Zilog Z80A |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->|  EXECUTE |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. Uses **Sequential Execution** template (identical to Zilog Z80A)
2. Block operations (LDIR, CPIR) are key differentiator from 8080
3. Index register operations (IX+d, IY+d) add extra decode cycles
4. T-state based timing converted to average cycle counts

## References

- [Zilog Z80](https://en.wikipedia.org/wiki/Zilog_Z80)
- [Romanian Computing History](https://en.wikipedia.org/wiki/HC-85)

---
Generated: 2026-01-29
