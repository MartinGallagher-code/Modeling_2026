# KR581IK2 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Soviet clone of the Western Digital MCP-1600 chipset (data path component)
- Part 2 of a 2-chip CPU: KR581IK1 (control) + KR581IK2 (data path)
- 16-bit ALU and register file
- PDP-11 compatible addressing modes
- Supports all PDP-11 addressing modes including deferred and auto-increment
- 16-bit data bus, 16-bit address bus (64KB addressable)
- Used in Soviet LSI-11 compatible systems (Elektronika-60)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1983 |
| Clock | 2.5 MHz |
| Transistors | ~6,000 (data path chip) |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | Western Digital MCP-1600 (data path) |

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
   - Forms one half of a 2-chip CPU (paired with KR581IK1 control/microcode)
   - The data path chip provides the 16-bit ALU and register file
   - Instruction timing is identical to KR581IK1 as they form a single logical CPU
   - PDP-11 addressing modes (register, register indirect, auto-increment, etc.) handled by data path
   - Memory-indirect and deferred addressing adds ~10 cycles
   - I/O is memory-mapped at ~12 cycles per access
   - Target CPI of ~8.0 for typical workloads matches WD MCP-1600

## Validation Approach

- Compare against Western Digital MCP-1600 documentation
- Validate with DEC LSI-11 timing specifications
- Cross-reference with Elektronika-60 technical manuals
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/western_digital/mcp-1600)
- [Wikipedia - LSI-11](https://en.wikipedia.org/wiki/LSI-11)

---
Generated: 2026-01-29
