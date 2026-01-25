# TI TMS9995 - Project Summary

## Enhanced TMS9900 (1981)

Improved TMS9900 with on-chip RAM and 8-bit bus.

## Key Features
- 256 bytes on-chip RAM
- 8-bit external bus (lower cost)
- On-chip timer/decrementer
- Workspace architecture

## Workspace Concept
Registers R0-R15 live in RAM, pointed to by WP. Context switch = change WP. Fast interrupts but slower normal register access.

## Historical Note
Would have powered TI-99/8 (cancelled 1983). Used in Myarc Geneve 9640.

---
**Version:** 1.0 | **Date:** January 25, 2026
