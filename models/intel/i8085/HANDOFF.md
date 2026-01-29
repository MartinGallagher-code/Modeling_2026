# Intel 8085 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-28
- **Cross-validation**: Complete (with i8008, i8080)

## Current Model Summary
- Architecture: 8-bit NMOS microprocessor (enhanced 8080)
- Year: 1976
- Clock: 3.0 MHz
- Target CPI: 5.5
- Technology: 3um NMOS, 6500 transistors
- Instruction categories: data_transfer, memory, ALU, control
- Timing: 4-18 cycles per instruction

## Validation Data
- 34 per-instruction timing tests documented
- Cross-validation with i8008 and i8080 complete
- 8085-unique instructions (RIM, SIM) documented

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- Model is complete and validated
- Consider adding specific workload profiles for embedded applications
- Could model serial I/O timing (SID/SOD pins)

## Key Architectural Notes
- The Intel 8085 was an enhanced 8080 with single +5V power supply
- Binary compatible with 8080 (same ISA + RIM/SIM)
- Integrated clock generator (no external crystal oscillator circuit needed)
- Added serial I/O pins (SID/SOD) for simple serial communication
- Added vectored interrupts (RST 5.5, 6.5, 7.5)
- RIM/SIM instructions for interrupt mask control (4 cycles each)
- Popular in embedded systems and educational settings
- MOV r,r is 4 cycles (1 cycle faster than 8080's 5 cycles)

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

## 8085-Unique Instructions
- **RIM** (Read Interrupt Mask): 4 cycles - reads interrupt mask and serial input
- **SIM** (Set Interrupt Mask): 4 cycles - sets interrupt mask and serial output
