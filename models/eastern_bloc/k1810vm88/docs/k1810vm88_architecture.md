# K1810VM88 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Soviet clone of the Intel 8088 microprocessor
- 8-bit external data bus, 16-bit internal data bus
- 20-bit address bus (1MB addressable)
- 4-byte instruction prefetch queue (vs 6-byte on 8086/K1810VM86)
- Segment-based memory model (CS, DS, SS, ES)
- Hardware multiply and divide instructions
- String operations with REP prefix
- Full Intel 8088 instruction set compatibility
- ~29,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1986 |
| Clock | 5.0 MHz |
| Transistors | ~29,000 |
| Data Width | 16-bit (internal), 8-bit (external) |
| Address Width | 20-bit |
| Process | NMOS |
| Western Equivalent | Intel 8088 |

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
Note: 8-bit bus causes additional memory access penalties vs 8086
```

## Model Implementation Notes

1. Uses **Sequential Execution** template (identical to Intel 8088)
2. Key differences from K1810VM86 (8086 clone):
   - 8-bit external bus (slower 16-bit memory accesses)
   - 4-byte prefetch queue (vs 6-byte)
   - Slightly lower effective CPI due to bus optimization
3. Multiply/divide operations are very expensive (30+ cycles avg)

## Related Models

- K1810VM86: Soviet Intel 8086 clone (16-bit external bus)

## References

- [Intel 8088](https://en.wikipedia.org/wiki/Intel_8088)
- [Soviet IBM PC Clones](https://en.wikipedia.org/wiki/ES_EVM)

---
Generated: 2026-01-29
