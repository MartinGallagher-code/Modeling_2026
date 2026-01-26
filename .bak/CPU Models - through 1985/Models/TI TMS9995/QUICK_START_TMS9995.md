# TI TMS9995 - Quick Start

## Enhanced TMS9900 (1981)

Registers live in RAM! (Workspace architecture)

| Spec | TMS9900 | TMS9995 |
|------|---------|---------|
| Bus | 16-bit | **8-bit** |
| On-chip RAM | None | **256B** |
| Timer | External | **On-chip** |

## Workspace Architecture
- WP (Workspace Pointer) points to R0-R15 in RAM
- Context switch = just change WP
- Trade-off: Slower register access

## Used In
- TI-99/8 (unreleased)
- Myarc Geneve 9640
