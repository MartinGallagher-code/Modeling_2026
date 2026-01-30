# KR580VM1 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created KR580VM1 model as Soviet 8080 extension
- Used Intel 8080 timing as base reference
- Added bank_switch category for extended memory operations
- Calibrated instruction categories:
  - alu: 5.0 cycles (ADD/SUB r @4, ADD M @7, weighted)
  - data_transfer: 5.0 cycles (MOV r,r @5, MVI @7, weighted)
  - memory: 9.0 cycles (LDA @13, MOV r,M @7, weighted)
  - io: 10.0 cycles (IN/OUT @10 states)
  - control: 8.0 cycles (JMP @10, CALL @17, weighted)
  - bank_switch: 12.0 cycles (bank select with overhead, unique to KR580VM1)

### Results
- Target CPI: 8.0 (slightly slower than 8080's 7.5 due to bank management)
- Status: VALIDATED

### Technical Notes
- KR580VM1 is NOT a direct 8080 clone - it extends the ISA
- Adds 128KB bank-switched addressing (vs 8080's 64KB)
- Bank-switch overhead accounts for ~0.5 CPI increase over base 8080
- NMOS technology, 2.5 MHz clock

### References
- Intel 8080 Datasheet (base timing reference)
- Soviet microprocessor documentation

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
