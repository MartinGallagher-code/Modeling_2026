# Cyrix Cx486SLC Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- 386SX pin-compatible
- 1KB cache
- 16-bit bus

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Cyrix |
| Year | 1992 |
| Clock | 25.0 MHz |
| Transistors | 600,000 |
| Data Width | 32-bit |
| Address Width | 16-bit |
| Technology | 0.8um CMOS |

## Description

486 ISA for 386SX systems, 16-bit bus

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 3.0
3. Primary bottleneck: bus_16bit
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Cyrix_Cx486SLC)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
