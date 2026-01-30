# Synertek SY6502A Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.17%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit sequential execution (no pipeline)
Licensed 6502 from Synertek, speed-binned for 2 MHz operation.

The Synertek SY6502A is a second-source 6502 rated for higher clock
speeds. It is fully compatible with the MOS 6502 with identical timing.

### Key Features

| Feature | SY6502A | MOS 6502 |
|---------|---------|----------|
| Manufacturer | Synertek | MOS Technology |
| Clock (max) | 2 MHz | 1 MHz |
| Technology | NMOS | NMOS |
| Transistors | 3510 | 3510 |
| Die | Same | Same |
| Timing | Identical | - |

### Speed-Binning

The "A" suffix indicates a speed-binned part:
- **SY6502**: Standard 1 MHz rated
- **SY6502A**: 2 MHz rated (selected for higher speed)

Speed binning involves testing chips and selecting those that
operate reliably at higher frequencies.

### Instruction Timing (Identical to 6502)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.3 | INX/DEX @2, ADC imm @2, ADC zp @3 |
| data_transfer | 2.8 | LDA imm @2, zp @3, abs @4 |
| memory | 4.0 | STA zp @3, abs @4, indexed @4-5 |
| control | 2.6 | Branches @2.55 avg, JMP @3 |
| stack | 3.5 | PHA @3, PLA @4, JSR/RTS @6 |

**Performance:**
- Target CPI: 3.0 (cross-validated from 6502)
- Model CPI: 3.065
- At 2 MHz: ~652,000 instructions/second
- At 1 MHz (for comparison): ~326,000 IPS

## Performance Comparison

| Processor | Clock | CPI | IPS |
|-----------|-------|-----|-----|
| MOS 6502 | 1 MHz | 3.0 | 326K |
| SY6502A | 2 MHz | 3.0 | 652K |

The SY6502A provides exactly 2x the throughput when run at 2 MHz,
as the instruction timing is identical to the 6502.

## Synertek as 6502 Second-Source

Synertek was one of several companies licensed to manufacture the
6502 family:

| Manufacturer | Part Number | Notes |
|--------------|-------------|-------|
| MOS Technology | 6502 | Original |
| Synertek | SY6502/A | Speed grades |
| Rockwell | R6502 | Later added CMOS |
| NCR | NCR6502 | For NCR systems |
| GTE | GTE6502 | Limited production |

All second-source 6502s are fully compatible with identical timing.

## 6502-Compatible Timing

**The SY6502A has IDENTICAL instruction timing to the MOS 6502.**

This is because Synertek used the same mask set licensed from MOS
Technology. The only difference is the speed-binning process that
selects chips capable of higher clock rates.

Individual instruction timings (from MOS datasheet):
- Implied (INX, TAX, NOP): 2 cycles
- Immediate (LDA #nn): 2 cycles
- Zero-page (LDA zp): 3 cycles
- Zero-page,X (LDA zp,X): 4 cycles
- Absolute (LDA abs): 4 cycles
- Absolute,X/Y (LDA abs,X): 4-5 cycles (+1 if page cross)
- Indirect,X (LDA (zp,X)): 6 cycles
- Indirect,Y (LDA (zp),Y): 5-6 cycles (+1 if page cross)
- Branch not taken: 2 cycles
- Branch taken: 3 cycles (+1 if page cross)
- JSR/RTS: 6 cycles each

## Known Issues

None - model uses validated 6502 timing data.

## Suggested Next Steps

1. **Validate against 2 MHz systems** - Test on actual 2 MHz 6502 systems
2. **Compare with other second-sources** - Verify Rockwell R6502 identical
3. **Document system requirements** - RAM/ROM timing at 2 MHz

## Key Architectural Notes

- Fully MOS 6502 compatible
- Higher clock requires faster RAM and peripherals
- Zero-page is still the key to performance
- Immediate mode is fastest (2 cycles)
- All timing in cycles - MHz affects absolute time only

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
