# Z180 Model Changelog

## 2026-01-28: Initial Calibration

### Changes Made
- Replaced incorrect template with optimized Z80-compatible sequential execution model
- Z180 has faster execution than Z80 (1-2 fewer cycles per instruction)
- Clock speed: 6.0 MHz (up to 20 MHz in later variants)
- Calibrated instruction categories for optimized timing:
  - alu: 3.2 cycles (optimized vs Z80's 4.0)
  - data_transfer: 3.2 cycles (faster than Z80)
  - memory: 4.8 cycles (optimized memory access)
  - control: 4.5 cycles (faster branches)
  - stack: 8.5 cycles (optimized PUSH/POP)
  - block: 10.0 cycles (faster block ops)

### Results
- CPI Error: 67.85% -> 1.9%
- Status: PASS

### What Worked
- Modeling Z180 as "optimized Z80" with reduced cycle counts
- On-chip peripherals don't affect instruction timing directly

### Technical Notes
- Z180 is enhanced Z80 with on-chip MMU, DMA, UART, timers
- Binary compatible with Z80 but faster execution
- MMU provides 1MB address space (vs Z80's 64KB)
- Popular in embedded systems and industrial controllers
