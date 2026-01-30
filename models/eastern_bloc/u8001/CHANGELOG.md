# VEB U8001 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created U8001 model as Zilog Z8001 clone
- Used Z8000 timing as reference (VEB maintained full compatibility)
- Calibrated instruction categories from Z8000 technical manual:
  - alu: 4.0 cycles (ADD/SUB R,R @4, R,IM @7, weighted)
  - data_transfer: 4.0 cycles (LD R,R @3, LD R,IM @7, weighted)
  - memory: 6.0 cycles (LD R,@R @7, LD R,addr @9)
  - io: 7.0 cycles (IN/OUT @10-12 with port addressing)
  - control: 6.0 cycles (JP @7, CALL @12, RET @9, weighted)
  - string: 8.0 cycles (block transfer/search operations)

### Results
- Target CPI: 5.5 (same as Z8000)
- Status: VALIDATED

### Technical Notes
- VEB U8001 is the first 16-bit processor in the Eastern Bloc (1984)
- Clone of Zilog Z8001 with identical timing
- NMOS technology, 4 MHz clock
- Segmented memory addressing (8MB)
- Used in industrial and military systems

### References
- Zilog Z8000 CPU Technical Manual (timing reference)
- VEB Mikroelektronik Erfurt documentation

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
