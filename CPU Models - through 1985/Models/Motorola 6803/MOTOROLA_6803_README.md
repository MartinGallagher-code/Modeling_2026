# Motorola 6803 CPU Queueing Model

## Executive Summary
The Motorola 6803 (1979) is the **ROM-less version of the 6801**. It removes the 2KB on-chip ROM but keeps the 128-byte on-chip RAM, allowing external ROM for larger programs.

## Technical Specifications
| Spec | 6801 | 6803 |
|------|------|------|
| On-chip ROM | 2 KB | **None** |
| On-chip RAM | 128 B | 128 B |
| I/O pins | 29 | **13** (bus uses pins) |
| External ROM | Optional | **Required** |

## When to Use 6803 vs 6801
| Scenario | Best Choice |
|----------|-------------|
| Small program (<2KB) | 6801 |
| Large program (>2KB) | **6803** |
| Maximum I/O | 6801 |
| Development/prototyping | **6803** |

## Trade-offs
```
6803 Advantages:
+ Unlimited program size (external ROM)
+ Lower chip cost (no ROM mask)
+ Better for development

6803 Disadvantages:
- Fewer I/O pins (13 vs 29)
- Needs external ROM chip
- Higher system cost
```

## Same as 6801
- 128 bytes on-chip RAM
- Hardware MUL instruction
- Full-duplex UART
- 16-bit timer
- Same instruction set

---
**Version:** 1.0 | **Date:** January 24, 2026
