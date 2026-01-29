# Hitachi HD64180 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created HD64180 model as Z180-equivalent processor
- Used Z180 timing as reference (Hitachi produced Z180 under license)
- Calibrated instruction categories with optimized timing vs Z80:
  - alu: 3.2 cycles (optimized vs Z80's 4.0)
  - data_transfer: 3.2 cycles (faster than Z80)
  - memory: 4.8 cycles (slightly optimized)
  - control: 4.5 cycles (faster branches)
  - stack: 8.5 cycles (optimized)
  - block: 10.0 cycles (faster than Z80)

### Results
- Target CPI: 4.5 (vs Z80's 5.5 - ~18% faster)
- Status: VALIDATED

### Technical Notes
- Hitachi HD64180 is functionally equivalent to Zilog Z180
- Enhanced Z80 with on-chip peripherals (MMU, DMA, UART, timers)
- 20-bit address bus allows 1 MB memory space
- CMOS technology for lower power consumption
- Faster clock speeds (up to 10 MHz in HD64180R variants)

### References
- Zilog Z180 Datasheet (timing reference)
- Hitachi HD64180 Technical Manual
