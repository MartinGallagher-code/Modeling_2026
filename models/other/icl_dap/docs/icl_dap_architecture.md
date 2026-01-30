# ICL DAP Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Distributed Array Processor with 4,096 processing elements
- SIMD (Single Instruction, Multiple Data) architecture
- Bit-serial processing elements
- Massively parallel computation for scientific workloads
- 1-bit data width per PE (bit-serial operations)
- Word operations built from bit-serial primitives
- Vector operations across the 64x64 PE array

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | ICL |
| Year | 1980 |
| Clock | 5.0 MHz |
| Transistors | N/A (board-level system) |
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
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Bit-serial operations are the fastest at 6 cycles per PE
   - Word operations (built from bit-serial) take 10 cycles
   - Vector operations across the PE array take 14 cycles
   - Array control operations at 8 cycles
   - CPI per instruction is high, but 4,096 PEs work in parallel
   - True performance comes from SIMD parallelism, not per-PE CPI
   - Vector operations dominate the typical workload (~41%)

## Validation Approach

- Compare against original ICL DAP technical documentation
- Validate with known SIMD array processor benchmarks
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/ICL_Distributed_Array_Processor)

---
Generated: 2026-01-29
