# OKI MSM5205 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.2%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 4-bit ADPCM decoder (1983), 384kHz clock
- 7 instruction categories: nibble_fetch (3.0), decode (4.5), step_adjust (3.0), accumulate (2.5), dac_output (4.5), control (3.0), interpolate (7.0)
- DAC output overhead: +1.5 cycles
- Global overhead factor: 1.04 (4%)
- Predicted typical CPI: 3.952 (target: 4.0)

## Known Issues
- None significant; all four workloads pass under 5% error

## Suggested Next Steps
- Model is well-calibrated; no immediate changes needed
- Could investigate per-sample timing against MAME emulation for further validation

## Key Architectural Notes
- Used in hundreds of arcade games for voice/sound effects
- 4-bit ADPCM nibbles decoded to 12-bit DAC output
- Sample rate determined by external clock divider
