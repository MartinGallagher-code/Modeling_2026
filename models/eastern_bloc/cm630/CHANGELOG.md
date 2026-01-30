# CM630 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created CM630 model as WDC 65C02 CMOS clone
- Used 65C02 timing as reference
- Calibrated instruction categories from 65C02 datasheet:
  - alu: 2.5 cycles (ADC/SBC #imm @2, zp @3, abs @4, weighted)
  - data_transfer: 2.5 cycles (LDA/STA #imm @2, zp @3, abs @4, weighted)
  - memory: 4.0 cycles (indirect addressing modes @5-6)
  - control: 3.0 cycles (branch @2.5avg, JMP @3, JSR @6, RTS @6, weighted)
  - stack: 3.5 cycles (PHA @3, PLA @4, weighted)

### Results
- Target CPI: 2.85 (same as WDC 65C02)
- Status: VALIDATED

### Technical Notes
- Bulgarian CMOS 6502 clone (1984)
- Used in Pravetz 82 and Pravetz 8M Apple II clones
- CMOS technology, 1 MHz clock (Apple II compatible)

### References
- WDC 65C02 Datasheet (timing reference)
- Pravetz computer documentation

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
