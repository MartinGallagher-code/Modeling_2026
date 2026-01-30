# National NS32081 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s 32-bit floating-point coprocessors
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Floating-point coprocessor for the NS32000 family
- IEEE 754 compatible floating-point standard support
- Single-precision (32-bit) and double-precision (64-bit) operations
- Hardware multiply, divide, and square root
- Tightly coupled with NS32016/NS32032 via slave processor protocol
- Format conversion between single and double precision
- Dedicated floating-point register file
- Direct memory interface for operand fetching

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1982 |
| Clock | 10.0 MHz |
| Transistors | N/A |
| Data Width | 32-bit |
| Address Width | 32-bit (via host processor) |

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

### Instruction Category Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| FP Add | 8.0 | Single-precision add/subtract (ADDF, SUBF) |
| FP Multiply | 12.0 | Single-precision multiply (MULF) |
| FP Divide | 20.0 | Single-precision divide (DIVF) |
| FP Square Root | 30.0 | Square root (SQRTF) |
| DP Add | 12.0 | Double-precision add/subtract (ADDL, SUBL) |
| DP Multiply | 18.0 | Double-precision multiply (MULL) |
| DP Divide | 32.0 | Double-precision divide (DIVL) |
| Conversion | 6.0 | Format conversion (MOVFL, MOVLF, etc.) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Target CPI of 15.0 reflects the mix of fast conversions and slow divides/square roots
   - As a coprocessor, instruction fetch is handled by the host NS32016/NS32032
   - Double-precision operations take roughly 1.5x the cycles of single-precision equivalents
   - Division and square root are iterative algorithms, hence the high cycle counts (20-32 cycles)
   - Conversion operations are the fastest at 6 cycles (simple format repackaging)
   - IEEE 754 compliance adds overhead for denormal handling and rounding modes

## Validation Approach

- Compare against original National Semiconductor NS32081 datasheet timing tables
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/national_semiconductor/ns32081)
- [Wikipedia](https://en.wikipedia.org/wiki/NS32000)

---
Generated: 2026-01-29
