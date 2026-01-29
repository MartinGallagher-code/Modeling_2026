# Namco 50xx Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create Namco 50xx model for arcade score/coin handling chip

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model
   - 4-bit custom state machine architecture
   - 5 instruction categories: alu, data_transfer, io, control, timer
   - 4 workload profiles: typical, scoring, coin_handling, idle
   - Target CPI: 5.0

2. Created validation JSON with timing data
   - Sources: MAME emulation, community reverse engineering

**Final state:**
- CPI: 4.85 (3.0% error vs 5.0 expected)
- Validation: PASSED

---
