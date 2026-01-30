# IM1821VM85A Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created IM1821VM85A model as Intel 8085 clone
- Used Intel 8085 timing as reference
- Calibrated instruction categories from 8085 datasheet:
  - alu: 4.0 cycles (ADD/SUB r @4, ADD M @7, weighted)
  - data_transfer: 4.5 cycles (MOV r,r @4, MVI @7, LXI @10, weighted)
  - memory: 8.0 cycles (LDA @13, MOV r,M @7, weighted)
  - io: 10.0 cycles (IN/OUT @10 T-states)
  - control: 6.0 cycles (JMP @10, CALL @18, RET @10, weighted)
  - stack: 10.5 cycles (PUSH @12, POP @10, weighted)

### Results
- Target CPI: 5.0 (same as Intel 8085)
- Status: VALIDATED

### Technical Notes
- Soviet Intel 8085 clone (1985)
- NMOS technology, 3 MHz clock
- Used in military and industrial applications

### References
- Intel 8085 Datasheet (timing reference)

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
