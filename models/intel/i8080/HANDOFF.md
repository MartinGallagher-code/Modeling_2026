# Intel 8080 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.4%
- **Last Updated**: 2026-01-28
- **Cross-validation**: Complete (with i8008, i8085)

## Current Model Summary
- Architecture: 8-bit NMOS microprocessor (industry standard)
- Year: 1974
- Clock: 2.0 MHz
- Target CPI: 9.2 (predicted: 9.075)
- Technology: 6um NMOS, 4500 transistors
- Instruction categories: ALU, data_transfer, memory, control, stack
- Timing: 4-18 cycles per instruction

## Validation Data
- 32 per-instruction timing tests documented
- Cross-validation with i8008 and i8085 complete
- Instruction timing comparison table included

## Known Issues
- 1.4% CPI error is within acceptable range
- Could improve accuracy by adjusting workload profile weights

## Suggested Next Steps
- Model is complete and validated
- Consider adding specific workload profiles for CP/M applications
- Could model wait states for slower memory systems

## Key Architectural Notes
- The Intel 8080 was THE industry standard 8-bit CPU (powered Altair 8800)
- Direct ancestor of x86 architecture (8086 designed for 8080 source compatibility)
- Uses external RAM for stack (unlike 8008's internal stack)
- 40-pin DIP with full 16-bit address bus
- Required +5V, +12V, and -5V power supplies (simplified in 8085)
- CALL (17 cycles) is slower than RET (10 cycles) due to address push
- XTHL at 18 cycles is the slowest instruction (exchange HL with stack)

## Cross-Validation Summary
| Instruction | i8008 | i8080 | i8085 |
|-------------|-------|-------|-------|
| MOV r,r     | 10    | 5     | 4     |
| MOV r,M     | 16    | 7     | 7     |
| ADD r       | 10    | 4     | 4     |
| JMP         | 22    | 10    | 10    |
| CALL        | 22    | 17    | 18    |
| RET         | 10    | 10    | 10    |
| NOP         | 8     | 4     | 4     |

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.30%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
