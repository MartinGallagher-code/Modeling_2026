# RCA CDP1861 (Pixie) Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.9%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Clock: 1.7609 MHz (NTSC-derived), ~2000 transistors, CMOS
- 6 operation categories: dma_fetch (2), display_active (4), horizontal_blank (6), vertical_blank (17), sync (10), interrupt (16)
- DMA contention modeled via M/M/1 queueing formula
- 3 utilization metrics: dma_controller, video_shift_register, sync_generator
- Target CPI: 8.0, Model CPI: 8.229

## Known Issues
- CPI spread across workloads is large (5.956 to 12.669), which is expected for a video controller
- Sync generator has a hardcoded +0.30 base utilization that makes it always dominant
- "CPI" metric is unconventional since this is a video controller, not a CPU

## Suggested Next Steps
- Consider per-workload validation targets since video controller behavior varies dramatically
- The DMA contention model could be refined with actual NTSC line timing data
- sync_generator base utilization (0.30) could be derived from NTSC timing ratios

## Key Architectural Notes
- This is a video display controller, NOT a general-purpose CPU
- Generates 64x32 pixel monochrome display for COSMAC systems (VIP, Studio II)
- Operates by stealing DMA cycles from the CDP1802 CPU during active display
- NTSC: 262 lines/frame, 128 active display lines, 8 bytes/line via DMA
- During vertical blank, no DMA occurs and the 1802 CPU runs freely
- End-of-frame interrupt signals the 1802 via EFx flag line

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
