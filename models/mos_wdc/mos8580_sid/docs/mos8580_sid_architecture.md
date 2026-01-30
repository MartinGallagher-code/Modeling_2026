# MOS 8580 SID Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1986)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Revised SID with HMOS-II process technology
- 3 independent oscillators with 4 waveforms
- Improved multi-mode resonant filter (more accurate response)
- 3 independent ADSR envelope generators
- Reduced audio bleed between channels
- Lower voltage operation (9V vs 12V)
- Register-compatible with MOS 6581

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology |
| Year | 1986 |
| Clock | 1.0 MHz |
| Transistors | ~13,000 |
| Data Width | 8-bit |
| Address Width | 5-bit (32 registers) |
| Package | DIP-28 |
| Technology | HMOS-II |
| Supply Voltage | 9V |

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

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - HMOS-II process allows faster cycle times across all categories
   - Filter response is more linear/accurate than 6581
   - Combined waveform behavior differs from 6581 (AND vs analog mixing)
   - Lower supply voltage reduces analog distortion characteristics

## Validation Approach

- Compare against MOS 8580 timing specifications
- Validate improvements relative to 6581 model
- Target: <5% CPI prediction error

## References

- [MOS 8580 SID Datasheet](TODO: Add link)
- [C64/C128 Hardware Reference](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_6581)

---
Generated: 2026-01-29
