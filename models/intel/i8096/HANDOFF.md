# Intel 8096 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 16-bit register-file microcontroller (MCS-96)
- Year: 1982
- Clock: 12.0 MHz (typical automotive)
- Target CPI: 4.0 (actual: 4.0)
- Register file: 232 bytes (addresses 00h-E7h)
- 8 dedicated registers (R0-R14, word aligned)

## Instruction Categories
| Category   | Cycles | Description                          |
|------------|--------|--------------------------------------|
| alu        | 3.0    | ADD/SUB/AND/OR reg-to-reg           |
| memory     | 4.5    | LD/ST indirect memory access        |
| multiply   | 6.0    | MUL 16x16->32 (hardware)            |
| divide     | 12.0   | DIV 32/16->16 (hardware)            |
| branch     | 4.0    | JMP/CALL/RET/conditional branches   |
| peripheral | 4.0    | PWM/ADC/Timer SFR access            |

## Cross-Validation Status
- **Related to**: Intel 8051 (predecessor, 8-bit MCU)
- **Family members**: 8097 (ROM-less), 80196 (enhanced)
- **Timing tests**: 40+ instructions documented
- **Timing rule**: State time = 3 clock cycles

## Known Issues
- None - model validates with 0% error

## Suggested Next Steps
- Model is fully validated with comprehensive instruction timing
- Future work could add specific automotive benchmark workloads
- Could add 80196 variant model (enhanced version with more I/O)

## Key Architectural Notes
- The Intel 8096 was the dominant automotive microcontroller for 20 years
- Register-file architecture (232 bytes) more flexible than accumulator
- Hardware multiply (16x16->32) and divide (32/16->16) critical for:
  - Fuel injection timing calculations
  - Engine RPM/speed calculations
  - Sensor linearization
- On-chip peripherals designed for automotive:
  - PWM outputs for motor control (throttle, fuel injectors)
  - 10-bit A/D converter for sensor inputs
  - High-Speed I/O (HSIO) for precise event timing
  - Watchdog timer for safety-critical operation
- Memory map:
  - 00h-17h: Register file (banked)
  - 18h-E7h: General-purpose registers
  - E8h-FFh: Special Function Registers (SFRs)
- Used in millions of automotive ECUs worldwide

## Typical Automotive Applications
- Engine control units (ECU)
- Anti-lock braking systems (ABS)
- Transmission control
- Climate control
- Body electronics
