# Intel 8035 CPU Queueing Model

## Executive Summary
The Intel 8035 (1976) is the **ROM-less version of the 8048**, the first successful single-chip microcontroller. It requires external ROM but retains the 64-byte on-chip RAM.

## Technical Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| ROM | **None (external)** |
| RAM | 64 bytes |
| Clock | 6-11 MHz |
| I/O | 27 lines |

## MCS-48 Family
```
┌─────────────────────────────────────────────────────────┐
│                    MCS-48 FAMILY                        │
├─────────┬──────────┬────────┬───────────────────────────┤
│ Chip    │ ROM      │ RAM    │ Use Case                  │
├─────────┼──────────┼────────┼───────────────────────────┤
│ 8048    │ 1KB      │ 64B    │ Standard production       │
│ 8035    │ External │ 64B    │ Development, large code   │
│ 8748    │ 1KB EPROM│ 64B    │ Prototyping               │
│ 8049    │ 2KB      │ 128B   │ Enhanced production       │
│ 8039    │ External │ 128B   │ Enhanced development      │
└─────────┴──────────┴────────┴───────────────────────────┘
```

## When to Use 8035 vs 8048
| Scenario | Best Choice |
|----------|-------------|
| Production, small code | 8048 |
| Development | **8035** |
| Code > 1KB | **8035** |
| Lowest unit cost | 8048 |
| No mask ROM charge | **8035** |

## Applications
- Development and prototyping
- Systems with external ROM
- Code larger than 1KB
- Flexible memory configurations

---
**Version:** 1.0 | **Date:** January 24, 2026
