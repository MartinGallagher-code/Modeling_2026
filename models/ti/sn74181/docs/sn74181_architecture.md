# TI SN74181 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s Combinational TTL Logic
**Queueing Model:** Serial M/M/1 chain (single-stage)

## Architectural Features

- First single-chip 4-bit ALU (combinational logic)
- 32 functions: 16 arithmetic + 16 logic operations
- Carry lookahead for ripple-free fast addition
- TTL (Transistor-Transistor Logic) technology
- NOT a CPU -- purely combinational building block
- Used in PDP-11, Data General Nova, and many minicomputers
- Cascadable with SN74182 carry lookahead generator

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1970 |
| Clock | 45.0 MHz (equivalent: 1/22ns propagation delay) |
| Transistors | 75 |
| Data Width | 4-bit |
| Address Width | 0-bit (no address bus -- combinational logic) |

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

Note: As a purely combinational ALU, the SN74181 collapses this to a single-stage model where all operations complete within one propagation delay (~22ns). CPI = 1.0 for all operations.

Target CPI: 1.0

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| Arithmetic | 1 | ADD, SUB, compare, increment (16 functions) |
| Logic | 1 | AND, OR, XOR, NOT (16 functions) |
| Shift | 1 | Carry propagation / shift through cascaded slices |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template (degenerate single-cycle case)
2. Key modeling considerations:
   - All 32 operations complete in exactly one propagation delay cycle
   - CPI is always 1.0 regardless of workload mix (all categories = 1 cycle)
   - The 22ns typical propagation delay defines the equivalent "clock" at ~45 MHz
   - No memory, no registers, no pipeline -- pure combinational logic
   - When cascaded for wider operations, the carry lookahead prevents linear delay scaling
   - The SN74182 companion chip provides group carry lookahead for 16+ bit configurations

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/sn74181)
- [Wikipedia](https://en.wikipedia.org/wiki/74181)

---
Generated: 2026-01-29
