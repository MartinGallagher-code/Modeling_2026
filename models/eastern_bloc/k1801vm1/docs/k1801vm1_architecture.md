# K1801VM1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980 (early single-chip PDP-11)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- First Soviet single-chip PDP-11 compatible microprocessor
- 16-bit data bus, 16-bit address bus (64KB addressable)
- PDP-11 instruction set with register-to-register and register-to-memory operations
- 8 general-purpose 16-bit registers (R0-R7, R7=PC, R6=SP)
- Multiple addressing modes (register, autoincrement, autodecrement, indexed, deferred)
- Stack-based subroutine calls and interrupts
- ~15,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1980 |
| Clock | 5.0 MHz |
| Transistors | ~15,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | DEC PDP-11 (single-chip) |

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

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - PDP-11 addressing modes add variable cycles per instruction
   - Stack operations (PUSH/POP) involve memory access overhead
   - Autoincrement/autodecrement modes are common in PDP-11 code
   - Target CPI of ~5.0 for typical systems programming workloads

## Validation Approach

- Compare against PDP-11 instruction timing documentation
- Cross-reference with DVK system performance data
- Target: <5% CPI prediction error

## References

- [PDP-11 Architecture](https://en.wikipedia.org/wiki/PDP-11_architecture)
- [DVK Computer Series](https://en.wikipedia.org/wiki/DVK)

---
Generated: 2026-01-29
