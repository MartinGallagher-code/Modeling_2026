# Intel 8086 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.56%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 16-bit CISC microprocessor (first x86)
- Year: 1978
- Clock: 5.0 MHz
- Target CPI: 4.5 (effective, with prefetch queue overlap)
- Predicted CPI: 4.525
- Instruction categories: ALU (2.5), data_transfer (2.5), memory (7.0), control (10.0)

## Cross-Validation Status
- **Related processor**: Intel 8088 (8-bit external bus variant)
- **Relationship verified**: 8088 is 86.5% of 8086 performance
- **Key differences documented**:
  - External bus width: 8086=16-bit, 8088=8-bit
  - Prefetch queue: 8086=6 bytes, 8088=4 bytes
  - Memory access penalty on 8088: +4 cycles per 16-bit transfer

## Instruction Timing Tests
- 28 comprehensive tests documented in validation JSON
- Covers: data transfer, memory, ALU, control, stack, mul/div, string operations
- All tests sourced from Intel datasheet

## Known Issues
- None - model validates within 5% error
- Model uses category-based effective cycles, not individual instruction timings

## Suggested Next Steps
- Model is stable; no changes needed unless better documentation found
- Could add more workload profiles for specific historical applications
- Could refine category timing if per-instruction validation desired

## Key Architectural Notes
- The Intel 8086 launched the x86 architecture that would dominate computing for the next 45+ years
- Its 16-bit segmented memory model and instruction set became the foundation for all subsequent x86 processors
- The 6-byte prefetch queue enables BIU/EU parallelism, significantly reducing effective CPI below raw instruction timing
- Raw instruction timings range 2-200+ cycles; effective CPI of 4.5 accounts for overlap
