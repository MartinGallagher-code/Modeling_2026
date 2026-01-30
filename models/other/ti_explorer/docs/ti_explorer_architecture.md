# TI Explorer Architectural Documentation

## Era Classification

**Era:** Pipelined Execution (Microcoded)
**Period:** Mid 1980s (1985)
**Queueing Model:** Pipelined M/M/1 chain

## Architectural Features

- 32-bit tagged data width for native LISP support
- Pipelined microcode execution
- Single-cycle CAR/CDR operations
- Improved memory allocator for CONS
- ~80,000 transistors in CMOS
- 8 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1985 |
| Clock | 8.0 MHz |
| Transistors | ~80,000 |
| Data Width | 32-bit (tagged) |
| Address Width | 24-bit |

## Queueing Model Architecture

```
+---------+   +----------+   +---------+   +----------+
|  FETCH  |-->| TYPE CHK |-->| EXECUTE |-->|  MEMORY  |
+---------+   +----------+   +---------+   +----------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

Pipelined microcode: improved over CADR sequential execution
CPI = weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** (microcoded) template
2. Key modeling considerations:
   - CAR/CDR reduced to single cycle through pipelining
   - CONS improved to 3 cycles with better allocator
   - EVAL reduced from 8 to 6 cycles via pipelined microcode
   - GC remains expensive at 10 cycles
   - Memory access is 4 cycles with tagged validation
   - Type checking improved to 2 cycles

## Validation Approach

- Compare against TI Explorer documentation
- Cross-validate with CADR and LMI Lambda models
- Target: <5% CPI prediction error

## References

- [TI Explorer Documentation](TODO: Add link)
- [Wikipedia - LISP Machine](https://en.wikipedia.org/wiki/Lisp_machine)

---
Generated: 2026-01-29
