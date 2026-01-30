# Zilog Z8S180 Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- Z80 superset
- DMA controller
- Dual UART

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1988 |
| Clock | 20.0 MHz |
| Transistors | 80,000 |
| Data Width | 8-bit |
| Address Width | 20-bit |
| Technology | 0.8um CMOS |

## Description

Enhanced Z180 with DMA and serial

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 3.5
3. Primary bottleneck: bus_contention
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Zilog_Z8S180)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
