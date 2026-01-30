# Intel 8061 Architecture

## Overview
The Intel 8061 (1978) is a custom 8-bit microcontroller designed exclusively for Ford Motor Company's Electronic Engine Control (EEC) system. It integrates specialized automotive peripherals on-chip.

## Key Features
- 8-bit data bus, 16-bit address bus
- 6 MHz clock frequency
- ~15,000 NMOS transistors
- Integrated ADC for sensor input
- Hardware timers for ignition timing
- Lookup table support for fuel/spark maps

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3 | Basic arithmetic and logic |
| ADC | 8 | Analog-to-digital conversion read |
| Timer | 4 | Timer capture/compare operations |
| Control | 5 | Branch, call, return |
| Lookup | 6 | Table lookup for fuel maps |

## Application
Used in Ford EEC-I through EEC-IV systems for:
- Fuel injection timing and quantity
- Spark advance calculation
- Idle speed control
- Exhaust gas recirculation

## Related Processors
- Intel 8096 (successor, 16-bit automotive MCU)
- Intel 8051 (general-purpose variant)
