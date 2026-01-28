# Z80A Model Changelog

## 2026-01-28: Initial Calibration

### Changes Made
- Replaced incorrect "Prefetch Queue" template with sequential execution model
- Same instruction timing as Z80 (cycles are clock-independent)
- Clock speed: 4.0 MHz (vs Z80's 2.5 MHz)
- Calibrated instruction categories from Z80 datasheet:
  - alu: 4.0 cycles
  - data_transfer: 4.0 cycles
  - memory: 5.8 cycles
  - control: 5.5 cycles
  - stack: 10.0 cycles
  - block: 12.0 cycles

### Results
- CPI Error: 37.33% -> 1.5%
- Status: PASS

### What Worked
- Inheriting Z80's calibrated timing values
- Z80A is just a faster-clocked Z80

### Technical Notes
- Z80A used in: MSX, Amstrad CPC, many arcade machines
- Popular choice for systems needing more performance than original Z80
