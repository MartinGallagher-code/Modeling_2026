# NEC uCOM-4 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Historical Significance

The NEC uCOM-4 (1972) was **NEC's first microcontroller** and a Japanese competitor to the TI TMS1000:

- Released in 1972, predating the TMS1000 (1974)
- Demonstrated Japanese semiconductor industry competitiveness
- Fixed instruction timing similar to TMS1000
- Higher clock speed (400 kHz) than TMS1000 (300 kHz)

## Current Model Summary

Architecture: 4-bit fixed-cycle MCU (1972)
All instructions execute in exactly 6 clock cycles.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 6 | ADD, SUB, logical operations |
| data_transfer | 6 | Register-memory transfers |
| memory | 6 | Load/store operations |
| control | 6 | Branch, call, return |
| io | 6 | I/O operations |

**Performance:**
- Target CPI: 6.0
- Model CPI: 6.0
- Clock: 400 kHz
- At 400 kHz: ~66,667 IPS

## Cross-Validation

Compared to contemporary 4-bit MCUs:

| Processor | Year | CPI | Clock | IPS | Notes |
|-----------|------|-----|-------|-----|-------|
| **uCOM-4** | 1972 | 6.0 | 400 kHz | 66,667 | NEC's TMS1000 competitor |
| TMS1000 | 1974 | 6.0 | 300 kHz | 50,000 | TI's fixed-timing MCU |
| PPS-4 | 1972 | 12.0 | 200 kHz | 16,667 | Serial ALU |

The uCOM-4's higher clock speed gave it a performance advantage over the TMS1000:
- Same CPI (6.0)
- 33% faster clock (400 vs 300 kHz)
- ~33% higher IPS

## Known Issues

None - fixed instruction timing makes the model inherently accurate.

## Suggested Next Steps

1. **uCOM-43/44/45** - Later enhanced variants in uCOM-4 family
2. Compare with other Japanese MCUs of the era
3. Model is essentially complete - no improvements needed

## Key Architectural Notes

- **Fixed timing**: All instructions take exactly 6 cycles (like TMS1000)
- **Parallel ALU**: 4-bit parallel processing (unlike serial PPS-4)
- **Harvard architecture**: Separate program and data memory
- **Applications**:
  - Calculators
  - Digital watches
  - Consumer electronics
  - Automotive (early)

## NEC vs TI Competition

```
TI TMS1000 (1974):          NEC uCOM-4 (1972):
  Clock: 300 kHz               Clock: 400 kHz
  CPI: 6.0                     CPI: 6.0
  IPS: ~50,000                 IPS: ~66,667

  (Both used fixed 6-cycle timing)
  (uCOM-4 had speed advantage from higher clock)
```

The uCOM-4 demonstrated that Japanese semiconductor companies could compete effectively with American giants like TI, setting the stage for Japan's later dominance in consumer electronics.

See CHANGELOG.md for full history of all work on this model.
