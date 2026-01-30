# Ensoniq ES5503 DOC Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.02%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit 32-oscillator wavetable synthesis (1985), 7.0 MHz clock
- 5 instruction categories: wavetable_read (6c), interpolation (8c), volume (4c), output (5c), control (3c)
- Sequential execution model
- Predicted typical CPI: 5.501 (target: 5.5)

## Known Issues
- 0.02% rounding error in typical CPI (5.501 vs 5.500) - negligible

## Suggested Next Steps
- Model is well-calibrated; no immediate changes needed
- Could model variable sample rate based on active oscillator count
- Could add oscillator bank switching workload profiles

## Key Architectural Notes
- 32 independent oscillators (DOC = Digital Oscillator Chip)
- Variable wavetable sizes: 256 bytes to 32K bytes per oscillator
- Sample rate inversely proportional to active oscillators
- Hardware interpolation for smooth sample playback
- External wavetable RAM (up to 64KB per bank)
- ~40,000 transistors (CMOS), most complex in this audio batch
- Used in Apple IIGS, Ensoniq Mirage, ESQ-1, SQ-80
