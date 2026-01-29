# MC14500B Architectural Documentation

## Era Classification

**Era:** Fixed-Cycle Combinational Execution
**Period:** 1976
**Queueing Model:** Trivial - all instructions 1 cycle (no queueing effects)

## Architecture Overview

The MC14500B is a **1-bit Industrial Control Unit (ICU)** designed by Motorola in 1976
as a replacement for relay logic and simple PLCs. It is one of the simplest
microprocessors ever manufactured, with only ~500 transistors.

**Key architectural distinction:** The MC14500B has no program counter. An external
sequencer (counter, PROM, etc.) provides instruction addresses. The chip itself only
processes 1-bit data through its Logic Unit and Result Register.

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Motorola |
| Year | 1976 |
| Clock | DC to 1 MHz @ 5V, up to 4 MHz @ 15V |
| Transistors | ~500 |
| Data Width | 1-bit |
| Opcode Width | 4-bit (16 instructions) |
| Package | 16-pin DIP |
| Technology | CMOS (silicon gate) |
| Supply Voltage | 3-18V |
| Power | ~50 µW typical |

## Execution Model

```
         4-bit opcode
              │
              ▼
┌──────────────────────┐
│   Instruction        │     1-bit data in
│   Register (IR)      │◄────────────────
│                      │
│   ┌──────────────┐   │
│   │  Logic Unit  │   │
│   │  (LU)        │   │
│   └──────┬───────┘   │
│          │           │
│   ┌──────▼───────┐   │
│   │  Result Reg  │   │────────────────►  1-bit data out
│   │  (RR)        │   │
│   └──────────────┘   │
│                      │     Flag outputs:
│   IEN  OEN  SKZ      │────────────────►  JMP, RTN, FLAG-F, FLAG-O
└──────────────────────┘

All operations complete in 1 clock cycle.
No pipeline. No prefetch. No cache.
No program counter (external).
```

## Instruction Set (All 1 Cycle)

| Opcode | Mnemonic | Operation |
|--------|----------|-----------|
| 0000 | NOPO | No operation (outputs active) |
| 0001 | LD | RR ← Data |
| 0010 | LDC | RR ← NOT Data |
| 0011 | AND | RR ← RR AND Data |
| 0100 | ANDC | RR ← RR AND (NOT Data) |
| 0101 | OR | RR ← RR OR Data |
| 0110 | ORC | RR ← RR OR (NOT Data) |
| 0111 | XNOR | RR ← RR XNOR Data |
| 1000 | STO | Data Out ← RR (write) |
| 1001 | STOC | Data Out ← NOT RR (write) |
| 1010 | IEN | Input Enable ← Data |
| 1011 | OEN | Output Enable ← Data |
| 1100 | JMP | Set JMP flag output |
| 1101 | RTN | Set RTN flag output |
| 1110 | SKZ | Skip next instruction if RR = 0 |
| 1111 | NOPF | No operation (outputs inactive) |

## Important Architectural Notes

1. **JMP and RTN are NOT branch instructions** in the traditional sense. They set
   output flag pins that an external program counter/sequencer must respond to.
   The MC14500B itself always processes the next instruction presented to it.

2. **SKZ** causes the chip to ignore the next instruction by internally gating the
   write enable. The external counter still advances - the instruction is fetched
   but not executed.

3. **IEN/OEN** gate the data input and output respectively. When IEN=0, all reads
   return 0. When OEN=0, all writes are suppressed.

## Model Implementation

The MC14500B is modeled as a fixed-cycle processor (like TMS1000), because every
instruction takes exactly 1 clock cycle. The CPI is always 1.0 regardless of
workload mix. This makes the model trivially accurate - 0% error.

## Application

Typical applications included:
- Industrial relay logic replacement
- Ladder diagram execution
- Simple sequencing controllers
- Binary decision trees

## References

- [Motorola MC14500B Industrial Control Unit Handbook (1977)](http://www.bitsavers.org/components/motorola/14500/MC14500B_Industrial_Control_Unit_Handbook_1977.pdf)
- [Ken Shirriff - A one-bit processor explained (2021)](http://www.righto.com/2021/02/a-one-bit-processor-explained-reverse.html)
- [WikiChip MC14500B](https://en.wikichip.org/wiki/motorola/mc14500/mc14500b)

---
Generated: 2026-01-29
