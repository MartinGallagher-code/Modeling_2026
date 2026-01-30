# Zilog Z380 Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- Z80 compatible
- 32-bit extensions
- Embedded/telecom

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1994 |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.6um CMOS |

## Description

32-bit Z80 extension, Z80 compatibility

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 3.0
3. Primary bottleneck: bus_contention
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Zilog_Z380)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
