# Goodyear STARAN Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s (1972)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Massively parallel associative processor with 256 processing elements (PEs)
- Bit-serial computation across all PEs simultaneously
- Content-addressable (associative) memory for parallel search
- 1-bit data width per PE (bit-serial architecture)
- 16-bit address space
- Designed for NASA satellite imagery processing
- 5 MHz clock for the control unit
- SIMD-style parallel execution model

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Goodyear Aerospace |
| Year | 1972 |
| Clock | 5.0 MHz |
| Transistors | N/A (board-level) |
| Data Width | 1-bit (per PE) |
| Address Width | 16-bit |

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
Note: Models the control unit; 256 PEs execute in parallel.
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Model represents the control unit instruction stream
   - Bit-serial operations average 4 cycles per PE instruction
   - Word-level operations require 8 cycles (bit-serial across word width)
   - Associative search operations are expensive at 12 cycles
   - Array control operations average 6 cycles
   - True throughput is multiplied by 256 PEs for data parallelism
   - Designed for image processing and pattern matching workloads

## Validation Approach

- Compare against original Goodyear Aerospace documentation
- Validate with NASA STARAN usage reports
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/goodyear/staran)
- [Wikipedia](https://en.wikipedia.org/wiki/STARAN)

---
Generated: 2026-01-29
