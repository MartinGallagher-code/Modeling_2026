# Intel 8085A CPU Queueing Model

## Executive Summary
The Intel 8085A (1976) was the **system-friendly version of the 8080**. Same instruction set, but with on-chip clock generator and system controller. This reduced a minimum 8080 system from 3 chips to 1, and simplified power from three voltages to just +5V.

## Technical Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| Clock | 3-6 MHz |
| ISA | **8080 compatible** |
| Power | **+5V only** |
| Clock gen | **On-chip** |
| Serial | **SID/SOD pins** |

## Improvements Over 8080
| Feature | 8080 | 8085 |
|---------|------|------|
| Clock generator | External 8224 | **On-chip** |
| System controller | External 8228 | **On-chip** |
| Power supplies | +5V, -5V, +12V | **+5V only** |
| Serial I/O | None | **SID/SOD** |
| Vectored interrupts | 1 | **4** |

## Historical Impact
- Made 8080 systems much simpler
- Powered CP/M computers
- Industrial controllers
- **Still taught in universities!**

## Educational Legacy
The 8085 is still used to teach microprocessor concepts:
- Simple enough to understand completely
- Real instruction set (not toy)
- Cheap development boards
- Extensive documentation

---
**Version:** 1.0 | **Date:** January 24, 2026
