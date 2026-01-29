# AMI S2400 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: < 5%
- **Last Updated**: 2026-01-29

## Historical Significance

The AMI S2400 (1973) is an improved S2000:
- Faster clock: 300 kHz (up from 200 kHz)
- Improved instruction timing (CPI 7.0 vs 8.0)
- Better integration for advanced calculators

## Current Model Summary

| Category | Cycles |
|----------|--------|
| alu | 5 |
| data_transfer | 6 |
| memory | 8 |
| io | 9 |
| control | 7 |

**Performance:**
- Target CPI: 7.0
- Clock: 300 kHz
- At 300 kHz: ~42,857 IPS

See CHANGELOG.md for full history.
