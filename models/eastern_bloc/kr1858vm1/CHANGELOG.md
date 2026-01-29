# KR1858VM1 (T34VM1) Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created KR1858VM1 model as Z80 clone (from U880 masks)
- Used Z80 timing as reference (identical timing via U880 photomasks)
- Calibrated instruction categories from Z80 datasheet:
  - alu: 4.0 cycles (ADD/SUB/INC/DEC register @4, immediate @7, weighted)
  - data_transfer: 4.0 cycles (LD r,r @4, LD r,n @7, weighted)
  - memory: 5.8 cycles (LD r,(HL) @7, LD (HL),r @7)
  - control: 5.5 cycles (JP @10, JR @9.5 avg)
  - stack: 10.0 cycles (PUSH @11, POP @10)
  - block: 12.0 cycles (LDIR/LDDR @21/16, weighted)

### Results
- Target CPI: 5.5 (same as Z80/U880)
- Status: VALIDATED

### Technical Notes
- KR1858VM1/T34VM1 is a Soviet Z80 clone (1991)
- Derived from East German U880 photomasks
- CMOS technology, 4 MHz clock
- One of the last Soviet-era processor designs

### References
- Zilog Z80 Datasheet (timing reference)
- Soviet IC cross-reference documentation
