# Weitek 1064/1065 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- High-speed floating-point coprocessor pair
- 1064 handles floating-point addition/subtraction
- 1065 handles floating-point multiplication/division
- 32-bit IEEE 754 floating-point operations
- Pipelined floating-point execution units
- Used in workstations, Cray supercomputers, and Sun SPARCstations
- Bus interface for coprocessor attachment to host CPU
- 15 MHz clock
- Approximately 40,000 transistors per chip

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Weitek |
| Year | 1985 |
| Clock | 15.0 MHz |
| Transistors | ~40,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |

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
Note: Models the FPU coprocessor operation stream.
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Math coprocessor, not a standalone CPU
   - FP addition averages 2.5 cycles (pipelined)
   - FP multiplication averages 3.0 cycles
   - FP division is most expensive at 4.0 cycles
   - Data transfer (bus interface) averages 2.5 cycles
   - Pipelined design allows overlapped FP operations
   - Paired chip design (1064 + 1065) splits add/mul workloads
   - Significantly faster than software FP emulation on host CPU

## Validation Approach

- Compare against original Weitek datasheet timing
- Validate against published MFLOPS benchmarks
- Cross-validate with Sun SPARCstation FP performance data
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/weitek/1064)
- [Wikipedia](https://en.wikipedia.org/wiki/Weitek)

---
Generated: 2026-01-29
