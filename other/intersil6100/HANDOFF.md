# Intersil 6100 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: CMOS PDP-8 on a chip (1975)
Full PDP-8/E instruction set, variable timing.

| Category | States | Description |
|----------|--------|-------------|
| arithmetic | 10 | TAD direct @10, indirect @15 |
| logic | 10 | AND direct @10, indirect @15 |
| memory | 12 | DCA @11, ISZ @16 states avg |
| jump | 12 | JMP @10, JMS @11 direct |
| io | 12 | IOT @12 states |
| operate | 6 | OPR (microcoded) @6 states |

**Performance:**
- Target CPI: 10.5 states
- Model CPI: 10.5 states
- At 4 MHz (500ns/state): ~190 KIPS

## Cross-Validation

Method: Validation against IM6100 datasheet timing
- Direct addressing: verified 10-16 states
- Indirect addressing: verified 15-21 states
- OPR fastest at 6 states: verified

## Known Issues

Model uses weighted average of direct/indirect addressing. Programs with
heavy indirect addressing will run slower than model predicts.

## Suggested Next Steps

1. **Harris 6120 model** - faster CMOS successor
2. **Separate direct/indirect profiles** - for more accurate modeling
3. Model is well-validated for typical workloads

## Key Architectural Notes

- First commercial CMOS microprocessor with PDP-8 compatibility
- 12-bit word size (unusual for era - most were 4, 8, or 16-bit)
- Full PDP-8/E instruction set (8 basic instructions)
- Variable timing: 6-22 states depending on instruction and addressing
- Fully static CMOS - can halt indefinitely, low power
- 4K word address space, expandable to 32K with 6102 chip
- Used in DECmate word processors (battery-powered PDP-8)
- State time: 500ns at 4 MHz, 250ns at 8 MHz (6100A)

See CHANGELOG.md for full history of all work on this model.
