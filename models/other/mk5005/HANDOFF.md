# Mostek MK5005 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 4-bit serial PMOS calculator-on-a-chip (1972)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 8 | Serial 4-bit ADD, SUB |
| bcd | 10 | Multi-digit BCD, decimal correct |
| shift | 6 | Shift register rotate |
| control | 7 | Branch, conditional skip |
| display | 12 | Display scan, segment output |

**Performance:**
- Target CPI: 9.0
- Model CPI: 9.0
- At 200 kHz: ~22 KIPS

## Known Issues

None - model validates at target CPI.

## Suggested Next Steps

1. **MK5017/MK5020 variants** - Model later Mostek calculator chips
2. **Display refresh modeling** - Display multiplexing overhead analysis
3. **Comparison with TMS0800** - Cross-validate against TI's similar-era calculator chip

## Key Architectural Notes

- One of the earliest calculator-on-a-chip designs
- 4-bit serial BCD data path
- Shift-register based architecture
- Integrated keyboard scanning and display multiplexing
- PMOS technology (~3,000 transistors)
- High cycle counts reflect slow early PMOS technology
- Display dominates workload at 30% of typical execution

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
