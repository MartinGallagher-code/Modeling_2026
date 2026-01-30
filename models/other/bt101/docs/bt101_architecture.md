# Brooktree Bt101 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1984)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Early RAMDAC (Random Access Memory Digital-to-Analog Converter)
- 8-bit data width with integrated palette RAM
- 25 MHz pixel clock rate
- ~20,000 transistors in CMOS technology
- Sequential pixel processing pipeline

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Brooktree |
| Year | 1984 |
| Clock | 25.0 MHz |
| Transistors | ~20,000 |
| Data Width | 8-bit |
| Technology | CMOS |

## Queueing Model Architecture

```
+-------------+   +-------------+   +-------------+   +-------------+
| PIXEL_READ  |-->| PALETTE     |-->| DAC         |-->| OUTPUT      |
| (addr)      |   | LOOKUP      |   | CONVERT     |   | (analog)    |
+-------------+   +-------------+   +-------------+   +-------------+
     |                  |                  |                  |
     v                  v                  v                  v
   M/M/1              M/M/1              M/M/1              M/M/1
   Queue              Queue              Queue              Queue

CPI = weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Palette read requires address decode + RAM access (2 cycles)
   - DAC conversion is multi-stage analog process (3 cycles)
   - Pixel clock synchronization is single-cycle
   - Color lookup table operations require full table traversal (3 cycles)
   - Control/sync operations handle blanking and timing (2 cycles)

## Validation Approach

- Compare against Brooktree datasheet specifications
- Validate with known video display timing requirements
- Target: <5% CPI prediction error

## References

- [Brooktree Bt101 Datasheet](TODO: Add link)
- [RAMDAC Architecture Overview](https://en.wikipedia.org/wiki/RAMDAC)

---
Generated: 2026-01-29
