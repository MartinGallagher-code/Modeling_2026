# Zilog Z280 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Z80 instruction set superset with significant enhancements
- On-chip 256-byte instruction/data cache
- On-chip Memory Management Unit (MMU)
- 24-bit address space (16 MB)
- 10 MHz clock
- ~68,000 transistors
- On-chip peripherals
- Pipelined execution with cache support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1985 |
| Clock | 10.0 MHz |
| Transistors | 68,000 |
| Data Width | 8-bit |
| Address Width | 24-bit |
| Cache | 256 bytes (on-chip) |
| MMU | On-chip |
| ISA Compatibility | Z80 superset |

## Queueing Model Architecture

```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│  OF  │─►│  EX  │─►│  WB  │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘
   │         │         │         │         │
   I1        I1        I1        I1        I1
             I2        I2        I2        I2

Ideal CPI = 1.0
Actual CPI = 1.0 + hazards + stalls + cache_misses
```

**Cache Hierarchy:**
- 256-byte on-chip unified cache
- Cache hits reduce memory access latency significantly
- Cache misses incur full external bus penalty

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3.5 | Cached ALU operations (3-4 cycles) |
| Data Transfer | 3.5 | Transfer operations (3-4 cycles) |
| Memory | 5.0 | Cached memory access (4-7 cycles) |
| Control | 5.0 | Branch/call operations (4-8 cycles) |
| Stack | 8.0 | Stack operations (7-10 cycles) |

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - The Z280 is the most architecturally advanced Z80-family processor, with cache and MMU on-chip
   - The 256-byte cache is very small by modern standards but provides meaningful speedup for tight loops
   - Cache hit/miss behavior significantly affects CPI -- cache hits bring ALU and transfer ops down to 3-4 cycles
   - The MMU adds address translation overhead but enables protected multitasking
   - Stack operations are notably slow (7-10 cycles) due to multiple memory accesses through the cache/MMU path
   - Despite pipelining, the Z80-compatible instruction encoding with variable-length instructions limits pipeline efficiency
   - Commercial adoption was limited due to complexity and competition from 16/32-bit processors

## Validation Approach

- Compare against original Zilog Z280 datasheet timing specifications
- Cross-reference with Z80 base timing for compatible instructions
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/zilog/z280)
- [Wikipedia](https://en.wikipedia.org/wiki/Zilog_Z280)

---
Generated: 2026-01-29
