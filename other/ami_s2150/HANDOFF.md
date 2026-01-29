# AMI S2150 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: < 5%
- **Last Updated**: 2026-01-29

## Historical Significance

The AMI S2150 (1972) is an S2000 variant:
- Same instruction timing as S2000 (CPI 8.0)
- Minor enhancements over base model
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
