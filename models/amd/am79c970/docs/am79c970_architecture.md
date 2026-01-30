# AMD Am79C970 PCnet Architectural Documentation

## Era Classification

**Era:** Network Processor
**Period:** 1986-1994
**Queueing Model:** Packet processing engine

## Architectural Features

- Ethernet controller
- 10 Mbps
- PCI/ISA

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AMD |
| Year | 1993 |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.6um CMOS |

## Description

Ethernet controller with on-chip processor

## Model Implementation Notes

1. This processor uses the **Network Processor** architectural template
2. Target CPI: 2.5
3. Primary bottleneck: packet_processing
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/AMD_Am79C970_PCnet)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
