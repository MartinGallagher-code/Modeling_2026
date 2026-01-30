# Zilog Z80-SIO

## Overview

**Zilog Z80-SIO** (1977) - Dual-channel serial I/O controller for Z80 systems

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1977 |
| Manufacturer | Zilog |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Transistors | ~8,000 |
| Technology | NMOS |
| Application | Serial I/O |

## Architecture

- **Data Width:** 8-bit interface
- **CPI Range:** 2-5
- **Typical CPI:** 3.5
- Dual async/sync serial, Z80 interrupt support

## Performance

- **IPS Range:** 800,000 - 2,000,000
- **MIPS (estimated):** 0.800 - 2.000
- **Typical CPI:** 3.5

## Validation

| Test | Status |
|------|--------|
| CPI | PASSED (0.0% error) |
| Architecture | Calibrated to serial I/O workload |

**Target Accuracy:** <5% CPI error

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
