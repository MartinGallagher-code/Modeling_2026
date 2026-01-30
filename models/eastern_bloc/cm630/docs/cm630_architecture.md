# CM630 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Bulgarian CMOS clone of the WDC 65C02
- 8-bit data bus, 16-bit address bus (64KB addressable)
- CMOS low-power design (vs NMOS original 6502)
- 65C02-compatible instruction set with improved timing on some instructions
- Zero-page addressing for fast memory access
- Hardware stack at page 1 ($0100-$01FF)
- 2-7 cycles per instruction
- Used in Pravetz 82 and Pravetz 8M (Bulgarian Apple II clones)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Bulgaria (CMOS clone) |
| Year | 1984 |
| Clock | 1.0 MHz |
| Transistors | ~4,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | CMOS |
| Western Equivalent | WDC 65C02 |

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
   - Instruction timing identical to WDC 65C02, not the original NMOS 6502
   - CMOS version eliminates some undocumented NMOS behaviors
   - Zero-page addressing modes are faster (fewer cycles) than absolute addressing
   - Indirect addressing mode (zp) available on 65C02 but not original 6502
   - Target CPI of ~2.85 for typical workloads matches 65C02 behavior

## Validation Approach

- Compare against original WDC 65C02 datasheet timing
- Validate with cycle-accurate 65C02 emulator (if available)
- Cross-reference with Pravetz technical documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mos_technology/mos_6502)
- [Wikipedia - Pravetz computers](https://en.wikipedia.org/wiki/Pravetz_series_8)

---
Generated: 2026-01-29
