# TI TMS9985 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s 16-bit Single-Chip Microcomputer
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Single-chip implementation of the TMS9900 architecture
- 256 bytes of on-chip RAM for workspace registers
- 16-bit internal and external data path
- Memory-to-memory architecture with workspace pointers
- On-chip RAM reduces workspace access latency compared to TMS9980
- Context switch via workspace pointer change (BLWP instruction)
- Full 16-bit bus (unlike 8-bit-bus TMS9980)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1978 |
| Clock | 2.5 MHz |
| Transistors | 10,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |

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

Target CPI: 10.0

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 6.5 | On-chip workspace ALU operations (5-8 cycles) |
| Data Transfer | 8 | Memory moves (6-10 cycles) |
| Memory | 12 | External memory access (10-14 cycles) |
| Control | 14 | Branch and BLWP (10-20 cycles) |
| Stack | 15 | Context switch operations (12-18 cycles) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The 256B on-chip RAM significantly improves workspace access compared to the TMS9980 (CPI 10.0 vs 12.0)
   - ALU operations benefit most from on-chip workspace: 6.5 cycles vs 8 cycles on the TMS9980
   - External memory access remains expensive at 12 cycles -- on-chip RAM only helps workspace operations
   - The full 16-bit bus (vs TMS9980's 8-bit bus) eliminates the double-access penalty
   - Context switch operations (15 cycles) are still expensive but this is inherent to the workspace architecture
   - The 2.5 MHz clock is a modest improvement over the TMS9980's 2.0 MHz
   - At CPI=10.0 and 2.5 MHz, throughput is 250K instructions per second
   - The workspace pointer architecture still requires memory access for every "register" operation, keeping CPI high compared to register-file architectures

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/tms9985)
- [Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_TMS9900)

---
Generated: 2026-01-29
