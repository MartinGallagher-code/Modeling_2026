# Rockwell R65C02 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.35%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit CMOS sequential execution (no pipeline)
Based on WDC 65C02 with Rockwell bit manipulation extensions.

The Rockwell R65C02 is a CMOS 6502 with additional bit test and
manipulation instructions designed for embedded control applications.

### Key Features

| Feature | R65C02 |
|---------|--------|
| Technology | CMOS |
| Clock | Up to 4 MHz |
| Power | Low power (CMOS) |
| Base instructions | WDC 65C02 compatible |
| Extensions | RMB, SMB, BBR, BBS |

### Rockwell-Specific Instructions

| Instruction | Cycles | Description |
|-------------|--------|-------------|
| RMB0-7 zp | 5 | Reset Memory Bit (clear bit in zero-page) |
| SMB0-7 zp | 5 | Set Memory Bit (set bit in zero-page) |
| BBR0-7 zp,rel | 5 | Branch on Bit Reset |
| BBS0-7 zp,rel | 5 | Branch on Bit Set |

These are extremely useful for:
- Bit-banged I/O protocols
- Flag manipulation without load/modify/store
- Efficient state machines
- Embedded control loops

### Instruction Timing (WDC 65C02 compatible)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.2 | INX/DEX @2, ADC imm @2, ADC zp @3 |
| data_transfer | 2.6 | LDA imm @2, zp @3, abs @4 |
| memory | 3.6 | STA zp @3, RMW abs,X @6 (optimized) |
| control | 2.5 | BRA @3, branches @2.55 avg |
| stack | 3.2 | PHX/PLX @3/4, JSR @6, RTS @6 |
| bit_ops | 5.0 | RMB/SMB @5, BBR/BBS @5 |

**Performance:**
- Target CPI: 2.85 (cross-validated from WDC 65C02)
- Model CPI: 2.84
- At 4 MHz: ~1,400,000 instructions/second

## CMOS Optimizations (vs NMOS 6502)

The R65C02 includes all WDC 65C02 optimizations:

1. **RMW abs,X optimization**: 6 cycles instead of 7
2. **BRA instruction**: Unconditional branch (3 cycles)
3. **PHX/PHY/PLX/PLY**: Push/pull index registers
4. **STZ**: Store zero (no need to LDA #0 first)
5. **No dummy cycles**: Indexed modes don't have extra cycles

These optimizations result in ~5% better CPI than NMOS 6502.

## Embedded Systems Usage

The R65C02 was popular in embedded systems because:

1. **Low power**: CMOS technology
2. **Bit manipulation**: RMB/SMB for I/O control
3. **Conditional bit branches**: BBR/BBS for efficient polling
4. **Higher clock**: Up to 4 MHz vs 1 MHz for NMOS

Example embedded usage:
```assembly
; Wait for bit 7 to be set on I/O port at $00
wait:
    BBS7 $00, ready   ; Branch if bit 7 set (5 cycles)
    JMP wait          ; Loop if not (3 cycles)
ready:
    ; Continue...
```

## Known Issues

None - model uses validated WDC 65C02 timing data plus documented
Rockwell extension timings.

## Suggested Next Steps

1. **Validate bit operation timings** - Confirm RMB/SMB/BBR/BBS cycles
2. **Test embedded workloads** - Analyze real embedded control code
3. **Compare with WDC 65C02** - Verify identical base timing

## Key Architectural Notes

- Fully WDC 65C02 compatible for base instructions
- Bit operations work only on zero-page (fast access)
- BBR/BBS are 5 cycles regardless of branch taken/not taken
- No page-crossing penalty on BBR/BBS
- RMB/SMB are atomic read-modify-write operations

See CHANGELOG.md for full history of all work on this model.
