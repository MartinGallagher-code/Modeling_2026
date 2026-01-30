# Cyrix Cx486DLC Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- 386 pin-compatible
- 1KB cache
- 486 instruction set

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Cyrix |
| Year | 1992 |
| Clock | 33.0 MHz |
| Transistors | 600,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.8um CMOS |

## Description

486 ISA in 386 pin-out, 1KB cache

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 2.5
3. Primary bottleneck: small_cache
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Cyrix_Cx486DLC)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
