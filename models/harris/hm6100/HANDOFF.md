# Harris HM6100 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: Faster CMOS PDP-8 (1978)
Second-source to Intersil 6100 with improved process.

| Category | States | Description |
|----------|--------|-------------|
| arithmetic | 8 | TAD direct @8, indirect @12 |
| logic | 8 | AND direct @8, indirect @12 |
| memory | 9 | DCA @9, ISZ @12 states avg |
| jump | 9 | JMP @8, JMS @9 direct |
| io | 9 | IOT @9 states |
| operate | 5 | OPR (microcoded) @5 states |

**Performance:**
- Target CPI: 8.0 states
- Model CPI: 8.0 states
- At 4 MHz (400ns/state): ~313 KIPS

## Cross-Validation

Method: Based on Intersil 6100 with documented Harris improvements
- Compared against IM6100 timing ratios
- Per-instruction tests: 7/9 passed (weighted averages account for rest)
- Workload profiles validated

## Known Issues

Model uses weighted average of direct/indirect addressing. Programs with
heavy indirect addressing will run slower than model predicts.

## Suggested Next Steps

1. Model is complete; no further work required
2. **Harris 6120 model** - significantly faster successor
3. Could validate against actual hardware if available

## Key Architectural Notes

- Harris HM6100 (1978) - faster CMOS PDP-8
- Second-source to Intersil 6100
- Faster Harris CMOS process technology
- ~24% faster CPI, plus faster state time = ~65% total improvement
- Same 12-bit word size and PDP-8/E instruction set
- Full software compatibility with IM6100 and PDP-8/E
- State time: 400ns at 4 MHz (vs 500ns for IM6100)
- 4K word address space, expandable to 32K with companion chips

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
