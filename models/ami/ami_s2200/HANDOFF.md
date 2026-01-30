# AMI S2200 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: < 5%
- **Last Updated**: 2026-01-29

## Historical Significance

The AMI S2200 (1972) is an S2000 variant with expanded ROM:
- Same instruction timing as S2000 (CPI 8.0)
- More ROM for larger calculator programs
- PMOS technology, 200 kHz

## Current Model Summary

| Category | Cycles |
|----------|--------|
| alu | 6 |
| data_transfer | 7 |
| memory | 9 |
| io | 10 |
| control | 8 |

**Performance:**
- Target CPI: 8.0
- Clock: 200 kHz
- At 200 kHz: ~25,000 IPS

See CHANGELOG.md for full history.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
