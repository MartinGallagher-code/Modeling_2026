# KR581IK1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Soviet clone of the Western Digital MCP-1600 chipset (control/microcode component)
- Part 1 of a 2-chip CPU: KR581IK1 (control) + KR581IK2 (data path)
- Microcoded architecture -- instruction timing depends on microcode ROM
- Implements PDP-11 instruction set via microcode
- 16-bit data path, 16-bit address bus (64KB addressable)
- Memory-mapped I/O (no dedicated I/O instructions)
- Used in Soviet LSI-11 compatible systems (Elektronika-60)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1983 |
| Clock | 2.5 MHz |
| Transistors | ~8,000 (control chip) |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | Western Digital MCP-1600 (control) |

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
   - Forms one half of a 2-chip CPU (paired with KR581IK2 data path)
   - Microcoded PDP-11 instruction set -- each instruction decomposes into multiple microcode cycles
   - MOV register-to-register takes 3-4 microcode cycles
   - Memory-indirect and deferred addressing modes add significant overhead (~10 cycles)
   - I/O is memory-mapped, costing ~12 cycles per access
   - SOB (subtract one and branch) loop instruction takes 5-6 cycles
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
