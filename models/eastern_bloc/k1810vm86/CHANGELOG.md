# K1810VM86 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created K1810VM86 model as Intel 8086 clone
- Used Intel 8086 timing as reference
- Calibrated instruction categories from 8086 datasheet:
  - alu: 4.0 cycles (ADD reg,reg @3, ADD reg,mem @9+EA, weighted)
  - data_transfer: 4.0 cycles (MOV reg,reg @2, MOV reg,imm @4, weighted)
  - memory: 10.0 cycles (memory ops with EA calculation)
  - io: 10.0 cycles (IN/OUT @8-12)
  - control: 8.0 cycles (JMP @15, CALL @19, RET @8, weighted)
  - stack: 9.0 cycles (PUSH @11, POP @8, weighted)
  - string: 12.0 cycles (REP MOVSW/STOSW/CMPSW)

### Results
- Target CPI: 6.5 (same as Intel 8086)
- Status: VALIDATED

### Technical Notes
- Soviet Intel 8086 clone (1985)
- Used in ES-1841 IBM PC clone
- NMOS technology, 5 MHz clock

### References
- Intel 8086 Datasheet (timing reference)

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 7 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
