# Ricoh RP2C02 PPU Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit Picture Processing Unit (1983), 5.37 MHz clock
- 5 instruction categories: background (3c), sprite_eval (5c), pixel_output (2c), vram_fetch (4c), oam (6c)
- Sequential execution model
- Predicted typical CPI: 3.500 (target: 3.5)

## Known Issues
- No known issues; model matches target exactly

## Suggested Next Steps
- Model is well-calibrated; no immediate changes needed
- Could model per-scanline rendering pipeline phases more precisely
- Could investigate sprite 0 hit timing behavior

## Key Architectural Notes
- NTSC NES/Famicom PPU at 5.37 MHz (3x 1.79 MHz CPU clock)
- 262 scanlines per frame at 60 Hz (240 visible + 22 VBlank)
- 341 PPU cycles per scanline
- 64 sprites in OAM (256 bytes), 8 sprites per scanline limit
- 2 pattern tables (4KB each), 4 nametables (1KB each, 2 physical)
- Background and sprite rendering are interleaved within each scanline
