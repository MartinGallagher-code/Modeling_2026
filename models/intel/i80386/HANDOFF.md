# Intel 80386 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 3.7%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 32-bit CISC with paging and protected mode
- Year: 1985
- Clock: 16.0 MHz
- Target CPI: 4.5
- Predicted CPI: 4.335
- Instruction categories: alu (2.5 cycles), data_transfer (2.5), memory (5), control (9), multiply (14), divide (40)

## Cross-Validation Status
- **Family**: Intel 80x86
- **Position**: First true 32-bit x86 processor
- **Predecessor**: Intel 80286 (1982) - added 32-bit, paging, virtual 8086 mode
- **Successor**: Intel 80486 (1989) - pipeline, on-chip cache and FPU
- **Variants**: 386DX (32-bit bus), 386SX (16-bit bus), 386SL (mobile)

## Timing Tests
- 26 per-instruction timing tests documented in validation JSON
- 32-bit MUL only 14 cycles (vs 40 for DIV)
- Includes LEA instruction timing

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Model is fully validated and cross-referenced with family
- Consider adding external cache modeling (386 had no on-chip cache)
- Add workload profiles for 32-bit operating systems (Unix, Windows)

## Key Architectural Notes
- First x86 to run Unix and Windows in protected mode
- Hardware paging enabled true virtual memory
- Virtual 8086 mode allowed running DOS programs under protected mode
- No on-chip cache - required external cache for good performance
- Required external 80387 coprocessor for floating-point
- Full 32-bit address space (4GB)

## System Identification (2026-01-29)
- **Status**: Did not converge
- **CPI Error**: 0.32%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
