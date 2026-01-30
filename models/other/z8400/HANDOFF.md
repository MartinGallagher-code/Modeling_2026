# SGS-Thomson Z8400 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit sequential execution (1980)
- Clock: 4.0 MHz, NMOS technology
- Categories: alu (4.0c), data_transfer (4.0c), memory (6.0c), control (6.0c), block (12.0c)
- Predicted typical CPI: 5.500 (target: 5.5)

## Known Issues
- Model uses simplified category-based timing
- Block instruction timing varies widely (12-21 T-states per iteration)

## Suggested Next Steps
- Cross-validate against Zilog Z80 model for consistency
- Refine block instruction timing with iteration count modeling
- Consider adding IX/IY indexed addressing category

## Key Architectural Notes
- Direct pin-compatible clone of Zilog Z80 manufactured by SGS-Thomson (Italy)
- Z80 adds block transfer/search, IX/IY index registers over 8080
- Two register banks for fast context switching
- SGS-Thomson later became STMicroelectronics
- Widely used in European consumer electronics and computing
