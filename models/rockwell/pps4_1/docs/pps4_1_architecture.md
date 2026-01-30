# Rockwell PPS-4/1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Single-chip variant of the PPS-4 architecture
- 4-bit serial ALU inherited from PPS-4
- Integrated ROM, RAM, and I/O on a single die
- Slightly faster than original PPS-4 due to on-chip integration (no external bus overhead)
- 250 kHz clock (faster than PPS-4's 200 kHz)
- 11-bit address bus supporting 2KB ROM
- Used in consumer electronics and appliances

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Rockwell International |
| Year | 1976 |
| Clock | 0.25 MHz |
| Transistors | 6,000 (estimated) |
| Data Width | 4-bit |
| Address Width | 11-bit |

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

## Instruction Timing Summary

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 12 | Serial ADD/SUB (bit-by-bit processing) |
| Memory | 9 | On-chip load/store (faster than PPS-4) |
| Branch | 10 | Conditional/unconditional jumps |
| I/O | 8 | On-chip I/O operations |

**Target CPI:** 10.0 (typical workload, improved from PPS-4's 12.0)
**Expected IPS:** ~25,000 at 250 kHz

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - On-chip integration reduces memory access overhead (9 cycles vs PPS-4's 11)
   - I/O operations benefit most from integration (8 cycles vs PPS-4's 10)
   - Serial ALU remains the bottleneck but is slightly improved (12 cycles vs 14)
   - Overall CPI improves from 12.0 to 10.0 (~17% faster than PPS-4)
   - Higher clock speed (250 kHz vs 200 kHz) provides additional throughput gain
   - Single-chip design trades address space (11-bit vs 12-bit) for integration benefits

## Validation Approach

- Compare against original Rockwell PPS-4/1 datasheet timing
- Validate that CPI is faster than PPS-4 (CPI < 12.0)
- Verify all workload CPIs fall in 8-12 cycle range
- Target: <5% CPI prediction error vs 10.0 target

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rockwell/pps-4)
- [Wikipedia](https://en.wikipedia.org/wiki/Rockwell_PPS-4)

---
Generated: 2026-01-29
