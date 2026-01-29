# Motorola 68060 CPU Queueing Model

## Executive Summary
The Motorola 68060 (1994) was the **last and fastest 68k processor**. Superscalar execution, branch prediction, pipelined FPU - technically excellent. But by 1994, the PowerPC Mac had shipped and the 68k era was over.

## Technical Specifications
| Spec | Value |
|------|-------|
| Year | 1994 |
| Transistors | 2,500,000 |
| Clock | 50-75 MHz |
| Pipeline | **10 stages** |
| Issue width | **2 (superscalar)** |
| I-Cache | 8 KB |
| D-Cache | 8 KB |
| IPC | **>1.0** |

## Superscalar Features
- Dual instruction issue
- Branch prediction (256-entry cache)
- 10-stage pipeline
- Pipelined FPU
- Out-of-order (limited)

## Performance
| Metric | 68040 | 68060 |
|--------|-------|-------|
| IPC | 0.90 | **1.20** |
| Clock | 40 MHz | **75 MHz** |
| MIPS | 35 | **100+** |
| MFLOPS | 6 | **35** |

## The Tragedy
```
1994: 68060 ships
1994: PowerPC Mac ships

The 68060 was technically excellent but:
- Apple had already committed to PowerPC
- No major systems adopted it
- Only used in accelerator cards and embedded
```

## Where Used
- Amiga 4000T accelerators
- Atari Falcon accelerators
- Embedded systems
- Enthusiast upgrades

## Legacy
The 68060 showed what 68k could have become. But timing is everything in the processor market.

---
**Version:** 1.0 | **Date:** January 24, 2026
