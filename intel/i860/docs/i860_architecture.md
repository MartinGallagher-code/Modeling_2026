# I860 Architectural Documentation

## Era Classification

**Era:** VLIW-Hybrid Superscalar
**Period:** 1989
**Queueing Model:** Dual-issue pipeline with pipelined FP

## Architectural Features

- Dual instruction mode (issue int AND fp simultaneously)
- 5-stage pipeline with 3 branch delay slots
- 4KB I-cache, 8KB D-cache
- Pipelined floating-point units (80 MFLOPS peak)
- No hardware interlocks - programmer handles hazards
- 64-bit data path
- "Cray on a chip" architecture

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1989 |
| Clock | 25.0 MHz |
| Transistors | 1,000,000 |
| Data Width | 64-bit |
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
   - Cache hierarchies with RISC-style execution

## Validation Approach

- Compare against original Intel datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/i860)
- [Wikipedia](https://en.wikipedia.org/wiki/i860)

---
Generated: 2026-01-27
