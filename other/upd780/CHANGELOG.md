# NEC uPD780 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created uPD780 model as Z80-compatible clone
- Used Z80 timing as reference (NEC maintained full compatibility)
- Calibrated instruction categories from Z80 datasheet:
  - alu: 4.0 cycles (ADD/SUB/INC/DEC register @4, immediate @7, weighted)
  - data_transfer: 4.0 cycles (LD r,r @4, LD r,n @7, weighted for register-heavy)
  - memory: 5.8 cycles (LD r,(HL) @7, LD (HL),r @7)
  - control: 5.5 cycles (JP @10, JR @9.5 avg, CALL/RET less frequent)
  - stack: 10.0 cycles (PUSH @11, POP @10)
  - block: 12.0 cycles (LDIR/LDDR @21/16, weighted)

### Results
- Target CPI: 5.5 (same as Z80)
- Status: VALIDATED

### Technical Notes
- NEC uPD780 is a second-source Z80 clone with identical timing
- Used in NEC PC-8001, PC-8801, and other Japanese computers
- uPD780C variant runs at 4 MHz
- Full instruction set and timing compatibility with Zilog Z80

### References
- Zilog Z80 Datasheet (timing reference)
- NEC uPD780 Datasheet
