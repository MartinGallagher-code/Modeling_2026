# Intel 3002 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s bit-slice era
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 2-bit ALU slice (cascadable for wider data paths)
- Schottky bipolar technology for high speed
- Single-cycle microinstruction execution
- 11 general-purpose registers per slice
- Paired with Intel 3001 Microprogram Control Unit
- All micro-operations complete in one clock cycle
- Designed for custom CPU construction via microprogramming

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1974 |
| Clock | 5.0 MHz |
| Transistors | ~125 (per slice) |
| Data Width | 2-bit (slice) |
| Address Width | 2-bit (slice) |

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

For the 3002, the microinstruction pipeline collapses to a single-cycle operation
since the microprogram control unit (3001) handles fetch/decode and the 3002 slice
executes in one cycle. The effective CPI is 1.0 per micro-operation.

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 1.0 | ADD, SUB, AND, OR, XOR operations |
| Shift | 1.0 | Left/right shift operations |
| Pass | 1.0 | Data routing (pass-through) |
| Load | 1.0 | Register load operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - All microinstructions execute in exactly 1 cycle, yielding CPI = 1.0
   - The 3002 is a 2-bit slice; real systems cascade 4-8 slices for 8-16 bit data paths
   - The 3001 microprogram control unit fetches and decodes microinstructions
   - Carry propagation across slices adds no extra cycles (look-ahead carry available)
   - Model treats the slice at the microinstruction level, not at the macro-instruction level
   - Target CPI of 1.0 reflects single-cycle microinstruction execution

## Validation Approach

- Compare against original Intel datasheet timing specifications
- Validate that all micro-operations complete in single cycle
- Target: <5% CPI prediction error (target CPI = 1.0)

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/mcs-3)
- [Wikipedia](https://en.wikipedia.org/wiki/Intel_3000)

---
Generated: 2026-01-29
