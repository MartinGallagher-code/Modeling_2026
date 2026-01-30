# Ricoh RP2C07 PPU Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit Picture Processing Unit (1986), 5.32 MHz clock
- 5 instruction categories: background (3c), sprite_eval (5c), pixel_output (2c), vram_fetch (4c), oam (6c)
- Sequential execution model
- Predicted typical CPI: 3.500 (target: 3.5)

## Known Issues
- No known issues; model matches target exactly

## Suggested Next Steps
- Model is well-calibrated; no immediate changes needed
- Could model the extended VBlank period (70 scanlines vs 20 on NTSC)
- Could investigate PAL-specific color encoding differences

## Key Architectural Notes
- PAL NES/Famicom PPU at 5.32 MHz (3x 1.77 MHz CPU clock)
- 312 scanlines per frame at 50 Hz (240 visible + 72 VBlank)
- 341 PPU cycles per scanline (same as NTSC)
- Same internal architecture as RP2C02, different frame timing
- Extended VBlank gives CPU significantly more processing time per frame
- PAL color encoding differs from NTSC but internal pixel pipeline is identical
