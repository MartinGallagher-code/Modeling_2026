# MOS 6507 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.17%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit sequential execution (no pipeline)
Based on MOS 6502 - identical instruction timing.

The MOS 6507 is the Atari 2600 CPU. It is a cost-reduced version of the 6502
with the same internal die but fewer external pins.

### Key Differences from 6502

| Feature | 6502 | 6507 |
|---------|------|------|
| Package | 40-pin DIP | 28-pin DIP |
| Address lines | 16 (A0-A15) | 13 (A0-A12) |
| Address space | 64KB | 8KB |
| Clock (typical) | 1.0 MHz | 1.19 MHz |
| RDY pin | Yes | No |
| NMI pin | Yes | No |
| SO pin | Yes | No |

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
- At 1.19 MHz: ~388,000 instructions/second

## Address Space Implications

The 13-bit address bus (8KB) is a significant constraint:
- $0000-$007F: TIA (Television Interface Adapter) registers
- $0080-$00FF: 128 bytes RAM (RIOT chip)
- $0280-$0297: RIOT (6532) I/O and timer
- $F000-$FFFF: 4KB ROM cartridge (mirrored)

The limited address space means:
- Programs must fit in 4KB (or use bank switching)
- Only 128 bytes of RAM available
- Zero-page is shared with TIA and RAM
- All absolute addresses within 8KB range

## 6502-Compatible Timing

**The 6507 has IDENTICAL instruction timing to the 6502.**

This is because the 6507 uses the same silicon die as the 6502.
The only difference is the package and which pins are bonded out.

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
- JMP abs: 3 cycles
- JMP (ind): 5 cycles

## Atari 2600 Considerations

The 6507 in the Atari 2600 must "race the beam" - generating display
output in real-time as the TV draws each scanline. This requires:

1. **Precise cycle counting** - Every instruction cycle matters
2. **Tight loops** - Display kernels repeat every 76 cycles (1 scanline)
3. **Heavy control flow** - Frequent branches for timing alignment
4. **Limited stack usage** - Less RAM means less stack space

The 'atari_kernel' workload profile reflects this with higher control
flow weight (30%) and lower stack usage (5%).

## Known Issues

None - model uses validated 6502 timing data.

## Suggested Next Steps

1. **Validate against Stella emulator** - Compare cycle counts
2. **Add Atari 2600 specific tests** - Racing the beam scenarios
3. **Test known 2600 games** - Analyze instruction mix in real games

## Key Architectural Notes

- Zero-page ($00-$FF) is the key to 6507 performance
- On Atari 2600, zero-page overlaps with TIA and RAM
- Immediate mode is fastest (2 cycles) - use for constants
- (Indirect),Y mode is the workhorse for array processing
- Branch taken adds +1 cycle, page cross adds +1 more
- JSR/RTS both take exactly 6 cycles
- No NMI means VBLANK must be polled, not interrupt-driven

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
