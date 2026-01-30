# Rockwell R65C02 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- CMOS implementation of the 6502 architecture
- WDC 65C02 compatible with Rockwell-specific bit manipulation extensions
- RMB0-7 (Reset Memory Bit), SMB0-7 (Set Memory Bit) instructions at 5 cycles
- BBR0-7 (Branch on Bit Reset), BBS0-7 (Branch on Bit Set) instructions at 5 cycles
- RMW operations on abs,X are 1 cycle faster than NMOS 6502 (6 vs 7)
- BRA instruction (unconditional branch) at 3 cycles
- PHX/PHY/PLX/PLY for index register stack operations
- No dummy cycles in indexed addressing modes
- Lower power consumption than NMOS 6502
- Up to 4 MHz clock speed
- Used in Apple IIc, embedded systems, and industrial controllers

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Rockwell International |
| Year | 1983 |
| Clock | 4.0 MHz |
| Transistors | 9,000 |
| Data Width | 8-bit |
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

## Instruction Timing Summary

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2.2 | INX/DEX @2, ADC imm @2, ADC zp @3 (same as 65C02) |
| Data Transfer | 2.6 | LDA imm @2, zp @3, abs @4 (faster indexed modes) |
| Memory | 3.6 | STA zp @3, abs @4, RMW abs,X @6 (was 7 on NMOS) |
| Control | 2.5 | BRA @3, branches @2.55 avg, JMP @3 |
| Stack | 3.2 | PHX/PLX @3/4, JSR @6, RTS @6 |
| Bit Ops | 5.0 | RMB/SMB @5, BBR/BBS @5 (Rockwell extensions) |

**Target CPI:** 2.85 (typical workload, same as WDC 65C02)
**Expected IPS:** ~1.4 MIPS at 4 MHz

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The R65C02 is slightly faster than the NMOS 6502 due to CMOS optimizations
   - Elimination of dummy cycles in indexed modes reduces average memory operation cost
   - Rockwell bit manipulation extensions (RMB/SMB/BBR/BBS) are 5-cycle operations
   - Bit ops are weighted at 0% in general-purpose workloads but 15% in embedded workloads
   - The embedded workload profile specifically exercises the Rockwell extensions
   - Memory operations (3.6 cycles) remain the bottleneck in typical workloads
   - CPI of 2.85 reflects the faster-than-NMOS but not-pipelined architecture

## Validation Approach

- Compare against WDC 65C02 and Rockwell R65C02 datasheet timing
- Validate R65C02 is faster than NMOS 6502 (CPI < 3.5)
- Verify Rockwell bit manipulation instructions at 5 cycles each
- Confirm bit_ops instruction category is present (Rockwell extension)
- Target: <5% CPI prediction error vs 2.85 target

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/wdc/w65c02s)
- [Wikipedia](https://en.wikipedia.org/wiki/WDC_65C02)

---
Generated: 2026-01-29
