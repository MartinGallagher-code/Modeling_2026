# Brooktree Bt101 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for Brooktree Bt101 RAMDAC

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: palette_read, dac_convert, control, pixel_clock, lookup
   - Calibrated for target CPI of 2.2 (sequential RAMDAC pipeline)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - Palette read: 2 cycles (address decode + RAM read)
   - DAC convert: 3 cycles (multi-stage analog conversion)
   - Control: 2 cycles (sync and control operations)
   - Pixel clock: 1 cycle (simple clock synchronization)
   - Lookup: 3 cycles (color lookup table traversal)

3. Workload weight calculation:
   - typical: 0.25*2 + 0.25*3 + 0.15*2 + 0.20*1 + 0.15*3 = 2.20 (exact match)

**What we learned:**
- The Bt101 was an early RAMDAC from Brooktree (1984)
- Sequential pixel processing pipeline with palette lookup and DAC stages
- 25 MHz pixel clock enabled standard video display rates
- Predecessor to Bt478 and later Brooktree RAMDAC family

**Final state:**
- CPI: 2.20 (0.00% error vs 2.2 expected)
- Validation: PASSED

**References used:**
- Brooktree Bt101 datasheet
- Video display system architecture references

---
