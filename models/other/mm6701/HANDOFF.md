# Monolithic Memories 6701 Model Handoff

## Current Status
- **Validation**: PASSED (17/17 tests, 100%)
- **CPI Error**: 0%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 4-bit slice ALU (1975)
Bipolar Schottky technology with single-cycle microinstructions.
Competitor to AMD Am2901 in the bit-slice market.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 1.0 | ADD/SUB/AND/OR/XOR @1 cycle |
| shift | 1.0 | SHL/SHR @1 cycle |
| pass | 1.0 | Data routing @1 cycle |
| zero | 1.0 | Clear operations @1 cycle |

**Performance:**
- Target CPI: 1.0 (per microinstruction)
- Model CPI: 1.0
- At 8 MHz: 8 MOPS (million operations per second)

## Comparison to AMD Am2901

| Feature | MM 6701 | AMD Am2901 |
|---------|---------|------------|
| Year | 1975 | 1975 |
| CPI | 1.0 | 1.0 |
| Data width | 4-bit | 4-bit |
| Registers | 16 | 16 |
| Transistors | ~180 | ~200 |
| Clock | 8 MHz | 10 MHz |
| Technology | Bipolar Schottky | Bipolar |

## Cross-Validation

Method: Validation against Monolithic Memories datasheets and comparison to Am2901
- All microinstructions single-cycle: verified
- CPI = 1.0 for all workloads: verified
- Consistent with Am2901 architecture: verified

Comparative performance:
- Equivalent to Am2901 in CPI
- Slightly lower clock speed (8 MHz vs 10 MHz)
- Both are 4-bit slices cascaded for wider data paths

## Known Issues

None - model accurately reflects MM 6701 bit-slice design.

## Suggested Next Steps

1. **Model complete 16-bit system** - 4 slices cascaded
2. **Add microsequencer** - For complete microprogrammed system
3. Model is well-validated

## Key Architectural Notes

- 4-bit slice ALU component (not a complete CPU)
- All microinstructions execute in single clock cycle
- Bipolar Schottky technology for high speed
- 16 general-purpose registers per slice
- Carry look-ahead support for cascading multiple slices
- Multiple slices cascaded for wider data paths:
  - 4 slices = 16-bit
  - 8 slices = 32-bit
- Part of the competitive bit-slice market of the 1970s
- Monolithic Memories was later acquired by AMD (1987)
- Used in custom minicomputers and signal processors

## Bit-Slice Market (1975)

```
AMD Am2901 (1975)           - Most popular, became industry standard
Intel 3002 (1974)           - 2-bit slice
Monolithic Memories 6701    - This model
Texas Instruments SN74181   - Earlier 4-bit ALU (not quite bit-slice)
Fairchild 9341              - Another competitor
```

The bit-slice approach allowed designers to build custom processors
by cascading multiple slices and writing microcode. This was popular
before single-chip microprocessors became powerful enough for most
applications.

## System Architecture

A complete microprogrammed computer using MM 6701 would include:
- Multiple 6701 slices (4 for 16-bit, 8 for 32-bit)
- Microprogram sequencer (e.g., Am2910)
- Microprogram ROM
- Status/carry logic
- Bus interface

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
