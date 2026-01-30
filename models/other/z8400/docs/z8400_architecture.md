# SGS-Thomson Z8400 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1980)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Second-source implementation of Zilog Z80 by SGS-Thomson
- 8-bit data path with 16-bit address bus
- NMOS technology, 4 MHz clock
- Full Z80 instruction set compatibility
- Block transfer and search instructions (LDIR, CPIR, etc.)
- Two register banks for fast context switching
- Sequential execution with no pipeline
- Pin-compatible with Zilog Z80

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | SGS-Thomson |
| Year | 1980 |
| Clock | 4.0 MHz |
| Transistors | ~8,500 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Technology | NMOS |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->| EXECUTE  |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Identical timing to Zilog Z80 (pin-compatible clone)
   - ALU and data transfer at 4 T-states each
   - Memory indirect and control flow at 6 T-states
   - Block instructions at 12+ T-states (LDIR, CPIR, etc.)
   - Two register banks enable fast interrupt response

## Validation Approach

- Compare against Zilog Z80 known timing
- Cross-validate against SGS-Thomson datasheet
- Target: <5% CPI prediction error

## References

- [SGS-Thomson Z8400 Datasheet](TODO: Add link)
- [Zilog Z80 Reference](https://en.wikipedia.org/wiki/Zilog_Z80)

---
Generated: 2026-01-29
