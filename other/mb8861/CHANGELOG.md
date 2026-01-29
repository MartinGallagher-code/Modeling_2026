# Fujitsu MB8861 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created MB8861 model as 6800-compatible clone
- Used M6800 timing as reference (Fujitsu maintained full compatibility)
- Calibrated instruction categories from M6800 datasheet:
  - alu: 2.8 cycles (ADDA imm @2, INCA @2, weighted)
  - data_transfer: 3.2 cycles (LDAA imm @2, register moves)
  - memory: 4.5 cycles (LDAA dir @3, LDAA ext @4, STAA @4)
  - control: 4.5 cycles (JMP @3, BEQ @4, weighted)
  - stack: 5.0 cycles (PSHA/PULA @4)
  - call_return: 9.0 cycles (JSR @9, RTS @5, weighted)

### Results
- Target CPI: 4.0 (same as M6800)
- Status: VALIDATED

### Technical Notes
- Fujitsu MB8861 is a second-source 6800 clone with identical timing
- Used in early Japanese arcade machines and computers
- MB8861A variant available at higher clock speeds
- Full instruction set and timing compatibility with Motorola 6800

### References
- Motorola M6800 Datasheet (timing reference)
- Fujitsu MB8861 Datasheet
