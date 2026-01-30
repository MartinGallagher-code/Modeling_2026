# AMI S2000 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: < 5%
- **Last Updated**: 2026-01-29

## Historical Significance

The AMI S2000 (1971) was one of the earliest calculator chips:
- Predates the Intel 4004 in some applications
- PMOS technology, 200 kHz clock
- Very slow but pioneering for electronic calculators
- Foundation for S2150, S2200, S2400 variants

## Current Model Summary

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 6 | ADD, SUB operations |
| data_transfer | 7 | Register transfers |
| memory | 9 | Load/store operations |
| io | 10 | Display/keyboard operations |
| control | 8 | Branch, jump |

**Performance:**
- Target CPI: 8.0
- Clock: 200 kHz
- At 200 kHz: ~25,000 IPS

## Known Issues
None.

See CHANGELOG.md for full history.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
