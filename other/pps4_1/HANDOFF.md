# Rockwell PPS-4/1 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29

## Historical Significance

The Rockwell PPS-4/1 (1976) was a **single-chip implementation** of the PPS-4 architecture:

- Integrated ROM, RAM, and I/O on a single die
- Inherited serial ALU design from multi-chip PPS-4
- Reduced cost and board space vs multi-chip PPS-4 solution
- Faster due to on-chip integration (no external bus overhead)

## Current Model Summary

Architecture: 4-bit single-chip serial ALU MCU (1976)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 12 | Serial ADD/SUB (bit-by-bit processing) |
| memory | 9 | On-chip load/store (faster than PPS-4) |
| branch | 10 | Conditional/unconditional jumps |
| io | 8 | On-chip I/O operations |

**Performance:**
- Target CPI: 10.0
- Model CPI: ~10.0
- Clock: 250 kHz
- At 250 kHz: ~25,000 IPS

## Cross-Validation

Compared to related processors:

| Processor | Year | CPI | Clock | Notes |
|-----------|------|-----|-------|-------|
| PPS-4 | 1972 | 12.0 | 200 kHz | Multi-chip, serial ALU |
| **PPS-4/1** | 1976 | 10.0 | 250 kHz | Single-chip integration |
| TMS1000 | 1974 | 6.0 | 300 kHz | Fixed timing, parallel ALU |

The improved CPI (10.0 vs 12.0) reflects on-chip integration benefits:
- Reduced memory access latency
- Faster I/O operations
- Higher clock speed support

## Known Issues

None currently. Single-chip integration benefits correctly modeled.

## Suggested Next Steps

1. **PPS-4/2** - Later enhanced variant
2. Compare with other single-chip MCUs of the era
3. Model may benefit from more detailed instruction-level timing data

## Key Architectural Notes

- **Serial ALU**: Inherited from PPS-4, processes 4-bit data one bit at a time
- **Single-chip**: ROM, RAM, I/O integrated on one die
- **On-chip benefits**: Reduced memory/I/O latency vs multi-chip
- **Applications**:
  - Consumer electronics
  - Appliances
  - Cost-sensitive embedded systems

## PPS-4 vs PPS-4/1 Comparison

```
Multi-chip PPS-4 (1972):
  CPU <--bus--> ROM <--bus--> RAM <--bus--> I/O
  (External bus adds latency to every access)

Single-chip PPS-4/1 (1976):
  +---------------------------+
  |  CPU   ROM   RAM   I/O    |
  |  (On-chip interconnect)   |
  +---------------------------+
  (Faster internal access, lower system cost)
```

See CHANGELOG.md for full history of all work on this model.
