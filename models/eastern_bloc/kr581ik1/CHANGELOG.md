# KR581IK1 Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created KR581IK1 model as WD MCP-1600 clone (control chip)
- Used MCP-1600 timing as reference
- Calibrated instruction categories:
  - alu: 5.0 cycles (ADD/SUB Rn,Rn @4-5, weighted)
  - data_transfer: 6.0 cycles (MOV with various modes)
  - memory: 10.0 cycles (indirect/deferred addressing)
  - io: 12.0 cycles (memory-mapped I/O)
  - control: 8.0 cycles (JMP/JSR/RTS/SOB)

### Results
- Target CPI: 8.0 (same as WD MCP-1600)
- Status: VALIDATED

### Technical Notes
- Soviet MCP-1600 clone (1983), part 1 of 2-chip CPU
- Used with KR581IK2 (data path) for PDP-11 compatible system
- Used in Elektronika-60 minicomputers

### References
- WD MCP-1600 documentation
- DEC LSI-11 technical manual
