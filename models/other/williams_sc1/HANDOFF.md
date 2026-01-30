# Williams SC1 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.2%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: Hardware blitter/DMA engine (1981), 1MHz clock
- 5 instruction categories: blit_copy (6+2), blit_xor (7+3), blit_solid (4+1), dma_setup (3+1), bus_arb (2+0)
- M/M/1 queueing with overhead factor 0.06
- Utilization: typical=0.78, sprite_heavy=0.88, screen_clear=0.82, idle=0.35
- Predicted typical CPI: 7.8221 (target: 8.0)

## Known Issues
- Sprite-heavy workload overshoots significantly at 28.7% error due to high utilization
- Screen-clear workload undershoots at 21.2% because blit_solid is cheap
- Non-typical workloads deviate significantly from the 8.0 target

## Suggested Next Steps
- Model is well-calibrated for typical use; no immediate changes needed
- Could investigate per-pixel blitter timing from hardware analysis

## Key Architectural Notes
- Hardware blitter for block copy, XOR blit, and solid fill operations
- Shares bus with Motorola 6809 CPU via bus arbitration
- Used in Williams arcade games: Defender, Joust, Robotron 2084, etc.
- ~4000 transistors, TTL technology
