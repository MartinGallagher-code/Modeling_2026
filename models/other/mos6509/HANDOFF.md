# MOS 6509 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.17%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit sequential execution (no pipeline)
Based on MOS 6502 - identical instruction timing with bank switching.

The MOS 6509 is the Commodore CBM-II CPU. It is a 6502 with added
bank switching hardware for accessing up to 1 MB of memory.

### Key Differences from 6502

| Feature | 6502 | 6509 |
|---------|------|------|
| Address space | 64KB | 1 MB (banked) |
| Bank registers | None | $0000, $0001 |
| IndBank ($0000) | N/A | Bank for (zp),Y indirect |
| ExecBank ($0001) | N/A | Bank for all other access |
| Clock | 1 MHz | 1 MHz |
| Instruction timing | - | Identical |

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
- At 1 MHz: ~326,000 instructions/second

## Bank Switching

The 6509's bank switching works as follows:

1. **ExecBank ($0001)**: Determines which 64KB bank is active for:
   - Instruction fetch
   - All addressing modes except (zp),Y

2. **IndBank ($0000)**: Determines which 64KB bank is used for:
   - The (zp),Y indirect addressing mode only
   - Allows copying between banks without switching ExecBank

3. **Bank architecture**:
   - 4-bit bank number (0-15)
   - Each bank is 64KB
   - Total addressable: 16 x 64KB = 1 MB

## 6502-Compatible Timing

**The 6509 has IDENTICAL instruction timing to the 6502.**

The bank switching hardware operates transparently and does not
add cycles to any instructions. The bank register stores at $0000
and $0001 take normal zero-page timing (3 cycles for read, 3 for write).

## Commodore CBM-II Systems

The 6509 was used in:
- Commodore B128 (128KB RAM)
- Commodore B256 (256KB RAM)
- Commodore P500 (similar to B128)
- Commodore 600/700 series (European models)

These were business-oriented machines running CP/M or BASIC.

## Known Issues

None - model uses validated 6502 timing data.

## Suggested Next Steps

1. **Validate against VICE emulator** - VICE supports CBM-II emulation
2. **Add bank switching benchmark** - Measure overhead of cross-bank operations
3. **Test against CBM-II software** - BASIC programs, business applications

## Key Architectural Notes

- Zero-page ($00-$FF) is the key to 6509 performance
- $0000 and $0001 are reserved for bank registers
- Indirect,Y mode can access different bank than other modes
- Bank switching requires only STA $0000 or STA $0001 (3 cycles each)
- No additional overhead for banked memory access

See CHANGELOG.md for full history of all work on this model.
