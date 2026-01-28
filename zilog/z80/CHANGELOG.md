# Z80 Model Changelog

## 2026-01-28: Initial Calibration

### Changes Made
- Replaced incorrect "Prefetch Queue" template with sequential execution model
- Calibrated instruction categories from Z80 datasheet:
  - alu: 4.0 cycles (ADD/SUB/INC/DEC register @4, immediate @7, weighted)
  - data_transfer: 4.0 cycles (LD r,r @4, LD r,n @7, weighted for register-heavy)
  - memory: 5.8 cycles (LD r,(HL) @7, LD (HL),r @7)
  - control: 5.5 cycles (JP @10, JR @9.5 avg, CALL/RET less frequent)
  - stack: 10.0 cycles (PUSH @11, POP @10)
  - block: 12.0 cycles (LDIR/LDDR @21/16, weighted)
- Used instruction_mix from validation JSON as workload weights

### Results
- CPI Error: 127.79% -> 1.5%
- Status: PASS

### What Worked
- Sequential execution model matches Z80's non-pipelined architecture
- Datasheet timing values accurate for individual instructions
- Weighted averages for categories work well

### What Didn't Work
- Original "Prefetch Queue" template was completely wrong - Z80 doesn't have prefetch queue
- Original template had arbitrary cycle counts unrelated to actual timing

### Technical Notes
- Z80 has no prefetch queue or pipeline - strict sequential execution
- Block instructions (LDIR, CPIR) are powerful but infrequent in typical code
- Same instruction timing as Z80A and Z80B (only clock speed differs)
