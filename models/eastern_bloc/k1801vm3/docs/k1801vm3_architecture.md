# K1801VM3 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1985 (advanced single-chip PDP-11)
**Queueing Model:** Pipelined M/M/1 chain

## Architectural Features

- Final and most advanced Soviet PDP-11 compatible microprocessor
- 16-bit data bus, 16-bit address bus (64KB addressable)
- Pipelined execution for improved throughput
- Full PDP-11 instruction set with floating point support
- 8 general-purpose 16-bit registers
- ~40,000 transistors enabling pipeline implementation

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1985 |
| Clock | 10.0 MHz |
| Transistors | ~40,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | DEC PDP-11 (pipelined single-chip) |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->|  EXECUTE |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Pipeline-adjusted weighted average (overlapped stages)
```

## Model Implementation Notes

1. Uses **Pipelined Execution** template
2. Key improvements over K1801VM2:
   - Pipeline overlaps fetch/decode/execute stages
   - Data transfer reduced to 2 cycles (vs 3 in VM2)
   - Memory access reduced to 5 cycles (vs 6 in VM2)
   - Control flow reduced to 3 cycles (vs 4 in VM2)
   - Improved FP at 8 cycles (vs 10 in VM2)

## K1801 Family Evolution

| Model | Year | Clock | Transistors | CPI |
|-------|------|-------|-------------|-----|
| K1801VM1 | 1980 | 5 MHz | 15,000 | 5.0 |
| K1801VM2 | 1983 | 8 MHz | 25,000 | 4.0 |
| K1801VM3 | 1985 | 10 MHz | 40,000 | 3.2 |

## References

- [PDP-11 Architecture](https://en.wikipedia.org/wiki/PDP-11_architecture)
- [Elektronika-85](https://en.wikipedia.org/wiki/Elektronika)

---
Generated: 2026-01-29
