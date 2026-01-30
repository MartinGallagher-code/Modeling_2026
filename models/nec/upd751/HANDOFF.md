# NEC uPD751 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29

## Historical Significance

The NEC uPD751 (1974) was NEC's **enhanced 4-bit microcontroller**:

- Evolution of the uCOM-4 architecture
- Added more complex instruction set and addressing modes
- Variable instruction timing (unlike fixed-timing uCOM-4)
- Trade-off: more features at cost of higher average CPI

## Current Model Summary

Architecture: 4-bit variable-cycle MCU (1974)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 8 | ADD, SUB, BCD arithmetic |
| data_transfer | 7 | Register-memory transfers |
| memory | 9 | Load/store with addressing modes |
| control | 8 | Branch, call, return |
| io | 7 | I/O operations |

**Performance:**
- Target CPI: 8.0
- Model CPI: ~8.0
- Clock: 400 kHz
- At 400 kHz: ~50,000 IPS

## Cross-Validation

Compared to related NEC processors:

| Processor | Year | CPI | Clock | IPS | Notes |
|-----------|------|-----|-------|-----|-------|
| uCOM-4 | 1972 | 6.0 | 400 kHz | 66,667 | Fixed timing |
| **uPD751** | 1974 | 8.0 | 400 kHz | 50,000 | Variable timing |
| TMS1000 | 1974 | 6.0 | 300 kHz | 50,000 | Fixed timing |

The uPD751 sits between simple fixed-timing MCUs and more complex variable-timing designs:
- More features than uCOM-4/TMS1000
- Higher CPI due to added complexity
- Similar IPS to TMS1000 despite higher CPI (offset by faster clock)

## Known Issues

None currently. Variable timing model correctly predicts workload-dependent performance.

## Suggested Next Steps

1. **uPD75xx family** - Extended family of 4-bit MCUs
2. Compare with other mid-1970s MCUs
3. Model may benefit from more detailed instruction-level timing data

## Key Architectural Notes

- **Variable timing**: Instructions take 7-9 cycles depending on type
- **Enhanced instruction set**: More addressing modes than uCOM-4
- **BCD arithmetic**: Useful for calculator/financial applications
- **Applications**:
  - Consumer electronics
  - Appliances
  - Industrial controllers
  - Automotive

## uCOM-4 vs uPD751 Trade-off

```
uCOM-4 (1972):                uPD751 (1974):
  Simple instruction set        Enhanced instruction set
  Fixed 6-cycle timing          Variable 7-9 cycle timing
  CPI: 6.0                      CPI: 8.0
  IPS: 66,667                   IPS: 50,000

  (Trade-off: speed vs. features)
```

The uPD751 represents NEC's approach to adding functionality:
- Accept higher CPI for more powerful instructions
- Additional addressing modes reduce instruction count
- Net effect: similar code size, slightly slower execution

## Variable Timing Analysis

The variable instruction timing means workload composition affects performance:

| Workload | CPI | Primary Factor |
|----------|-----|----------------|
| typical | ~8.0 | Balanced mix |
| compute | ~7.9 | ALU-heavy |
| memory | ~8.3 | Memory ops dominate |
| control | ~7.8 | Branch/I/O heavy |

Memory-intensive workloads see highest CPI due to 9-cycle memory operations.

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
