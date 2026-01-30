# Clipper C100 Architectural Documentation

## Era Classification

**Era:** Cache/RISC
**Period:** 1985-1990
**Queueing Model:** Pipelined RISC with cache hierarchy

## Architectural Features

- Load/store RISC architecture
- Separate instruction and data caches
- Pipelined execution (single-cycle ALU)
- 32-bit data and address paths
- Floating-point coprocessor support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Fairchild |
| Year | 1985 |
| Clock | 33.0 MHz |
| Transistors | ~132,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | CMOS |
| Package | PGA |

## Queueing Model Architecture

```
                    Clipper C100 Pipeline Model
                    ===========================

  RISC Pipeline:
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  FETCH   │──>│  DECODE  │──>│ EXECUTE  │──>│WRITEBACK │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘
       │                             │
   I-Cache                       D-Cache
       │                             │
       └──────────┬──────────────────┘
                  │
            Main Memory

  Category-Based CPI Model:
  ┌─────────────┬────────┬──────────────────────────────┐
  │ Category    │ Cycles │ Description                  │
  ├─────────────┼────────┼──────────────────────────────┤
  │ ALU         │   1    │ Register-to-register ops     │
  │ Load        │   2    │ Load from cache              │
  │ Store       │   1    │ Store to cache               │
  │ Branch      │   2    │ Branch/jump (taken penalty)  │
  │ Float       │   3    │ Floating-point operations    │
  └─────────────┴────────┴──────────────────────────────┘

  Weighted CPI = SUM(weight_i * cycles_i) = 1.5 (typical)
```

## Model Implementation Notes

1. This processor uses the **Cache/RISC** architectural template
2. Key modeling considerations:
   - Single-cycle ALU and store operations (RISC ideal)
   - Load operations incur cache lookup latency
   - Branch penalty from pipeline flush on taken branches
   - Floating-point operations require additional pipeline stages

## Validation Approach

- Compare against Fairchild Clipper C100 Technical Reference
- Validate with RISC pipeline performance models
- Target: <5% CPI prediction error

## References

- [Clipper C100 Technical Reference Manual](Fairchild, 1986)
- [WikiChip](https://en.wikichip.org/wiki/fairchild/clipper)
- [Wikipedia](https://en.wikipedia.org/wiki/Clipper_architecture)

---
Generated: 2026-01-29
