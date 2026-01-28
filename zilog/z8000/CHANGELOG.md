# Z8000 Model Changelog

## 2026-01-28: Initial Calibration

### Changes Made
- Replaced incorrect template with sequential execution model
- Z8000 is a completely different architecture from Z80 (not compatible)
- 16-bit data bus with 16 general-purpose registers
- Calibrated instruction categories from reference timing:
  - alu: 3.2 cycles (ADD R,R @4, weighted avg)
  - data_transfer: 2.8 cycles (LD R,R @3, fast 16-bit moves)
  - memory: 5.0 cycles (various addressing modes)
  - control: 4.8 cycles (JP @7, JR faster, weighted)
  - stack: 8.0 cycles (PUSH/POP 16-bit registers)
  - block: 9.0 cycles (block transfer operations)

### Results
- CPI Error: 66.18% -> 0.7%
- Status: PASS

### What Worked
- Recognizing Z8000 is NOT a Z80 variant - completely different architecture
- 16-bit orthogonal instruction set has faster register operations
- Weighted averages based on reference timing data

### What Didn't Work
- Initial attempt used cycle counts too close to reference singles (6.1% error)
- Had to fine-tune for weighted averages to hit 4.5 CPI target

### Technical Notes
- Z8000 has regular orthogonal instruction encoding
- Z8001 has segmented 23-bit address space
- Z8002 has non-segmented 16-bit address space
- Used in Olivetti M20, some Unix workstations
- Not popular due to competition from 68000 and market timing
