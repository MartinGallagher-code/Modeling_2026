# iWarp Architectural Documentation

## Era Classification

**Era:** Cache/RISC Architecture
**Period:** Mid 1980s (1985)
**Queueing Model:** Cache hierarchy + pipeline network

## Architectural Features

- VLIW (Very Long Instruction Word) dual-issue processor
- Systolic array communication links
- Joint Intel/CMU research project
- 32-bit data and address width
- Pipelined floating-point unit
- On-chip memory for low-latency access
- Precursor to modern GPU/parallel processing concepts
- 200,000 transistors
- 20 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel/CMU |
| Year | 1985 |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |

## Queueing Model Architecture

```
                    ┌────────────┐
                    │  I-Cache   │
                    └─────┬──────┘
                          │
┌──────┐  ┌──────┐  ┌─────▼────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│    EX    │─►│  MEM │─►│  WB  │
└──────┘  └──────┘  └──────────┘  └──┬───┘  └──────┘
                                     │
                               ┌─────▼──────┐
                               │  D-Cache   │
                               └────────────┘

RISC Goal: CPI ≈ 1.0
Actual CPI = 1.0 + cache_misses + hazards + branch_penalties
```

## Model Implementation Notes

1. This processor uses the **Cache/RISC Architecture** architectural template
2. Key modeling considerations:
   - VLIW ALU operations execute in 1 cycle (dual-issue capable)
   - Floating-point operations take 2 cycles (pipelined)
   - Memory access at 2 cycles (on-chip memory)
   - Systolic communication links at 2 cycles
   - Control/sequencing at 2 cycles
   - High ALU weight in typical workload (~49%) reflects VLIW efficiency
   - Dual-issue capability means effective CPI can be < 1.0 for parallel code
   - Systolic communication enables inter-node data flow

## Validation Approach

- Compare against Intel/CMU iWarp research papers
- Validate with known systolic array benchmark results
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/IWarp)

---
Generated: 2026-01-29
