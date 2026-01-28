# Z80B Model Changelog

## 2026-01-28: Initial Calibration

### Changes Made
- Replaced incorrect "Prefetch Queue" template with sequential execution model
- Same instruction timing as Z80/Z80A (cycles are clock-independent)
- Clock speed: 6.0 MHz (highest Z80 variant)
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
- Z80B is just the fastest-clocked Z80 variant

### Technical Notes
- Z80B is the highest speed standard Z80 at 6 MHz
- Same die as Z80/Z80A, just binned for higher speed
