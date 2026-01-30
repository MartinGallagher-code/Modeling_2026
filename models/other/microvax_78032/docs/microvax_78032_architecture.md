# MicroVAX 78032 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1979-1985
**Queueing Model:** Pipeline queueing network

## Architectural Features

- First single-chip VAX implementation
- Microcoded CISC execution engine
- Subset of full VAX instruction set
- Full VMS operating system compatibility
- 32-bit data and address paths
- On-chip translation buffer

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | DEC |
| Year | 1984 |
| Clock | 5.0 MHz |
| Transistors | ~125,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | CMOS |
| Package | 68-pin CERDIP |

## Queueing Model Architecture

```
                    MicroVAX 78032 Pipeline Model
                    =============================

  Instruction Flow:
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  FETCH   │──>│  DECODE  │──>│ EXECUTE  │──>│WRITEBACK │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘
       │              │              │              │
       │         Microcode      ALU/FPU        Register
       │          ROM           Memory          File
       │              │           │  │
       │              │           │  └─> Memory Bus
       │              │           │
       └──────────────┴───────────┘
              Translation Buffer

  Category-Based CPI Model:
  ┌─────────────┬────────┬──────────────────────────────┐
  │ Category    │ Cycles │ Description                  │
  ├─────────────┼────────┼──────────────────────────────┤
  │ ALU         │   2    │ Register-to-register ops     │
  │ Memory      │   6    │ Load/store with memory       │
  │ Control     │   4    │ Branch and jump              │
  │ String      │  10    │ String manipulation (MOVC)   │
  │ Decimal     │  15    │ Packed decimal arithmetic    │
  │ Float       │  12    │ F-format floating-point      │
  └─────────────┴────────┴──────────────────────────────┘

  Weighted CPI = SUM(weight_i * cycles_i) = 5.5 (typical)
```

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - Microcoded execution adds variable latency per instruction class
   - VAX string and decimal instructions are multi-cycle complex operations
   - Memory access includes translation buffer lookup
   - Full VMS compatibility requires modeling all instruction categories

## Validation Approach

- Compare against DEC MicroVAX 78032 Technical Manual
- Validate with VAX instruction timing documentation
- Target: <5% CPI prediction error

## References

- [MicroVAX 78032 Technical Manual](DEC, 1985)
- [WikiChip](https://en.wikichip.org/wiki/dec/microvax)
- [Wikipedia](https://en.wikipedia.org/wiki/MicroVAX)

---
Generated: 2026-01-29
