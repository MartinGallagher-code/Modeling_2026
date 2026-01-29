# KR581IK2 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created KR581IK2 model as WD MCP-1600 clone (data path chip)
- Same timing as KR581IK1 (they form one CPU)
- Calibrated instruction categories:
  - alu: 5.0 cycles (ADD/SUB Rn,Rn @4-5, weighted)
  - data_transfer: 6.0 cycles (MOV with various modes)
  - memory: 10.0 cycles (indirect/deferred addressing)
  - io: 12.0 cycles (memory-mapped I/O)
  - control: 8.0 cycles (JMP/JSR/RTS/SOB)

### Results
- Target CPI: 8.0 (same as WD MCP-1600 and KR581IK1)
- Status: VALIDATED

### Technical Notes
- Soviet MCP-1600 clone (1983), part 2 of 2-chip CPU
- Data path chip with 16-bit ALU and register file
- Used with KR581IK1 (control) for PDP-11 compatible system

### References
- WD MCP-1600 documentation
- DEC LSI-11 technical manual
