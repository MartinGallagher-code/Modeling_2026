# Elbrus El-90 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- VLIW-like
- Soviet design
- Superscalar

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MCST |
| Year | 1990 |
| Clock | 50.0 MHz |
| Transistors | 2,000,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.8um CMOS |

## Description

Soviet superscalar design, VLIW-like

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: vliw_schedule
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Elbrus_El-90)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
