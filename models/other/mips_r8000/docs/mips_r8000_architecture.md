# MIPS R8000 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- Superscalar
- 4-way FP
- Out-of-order FP

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MIPS |
| Year | 1994 |
| Clock | 90.0 MHz |
| Transistors | 2,600,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.5um CMOS |

## Description

First superscalar MIPS, 4-way FP, scientific workloads

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.2
3. Primary bottleneck: fp_bandwidth
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/MIPS_R8000)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
