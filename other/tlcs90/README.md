# Toshiba TLCS-90

**8-bit Z80-like Microcontroller (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 6 MHz |
| CPI | ~5.0 (Z80-like) |
| Performance | ~1.2 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 2.0% |
| Tests Passing | 8/8 |

## Model Files

- `current/tlcs90_validated.py` - Active model
- `validation/tlcs90_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tlcs90_validated import Tlcs90Model

model = Tlcs90Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The TLCS-90 was Toshiba's Z80-compatible MCU designed for applications
needing Z80 software compatibility with integrated peripherals. Features
block transfer/search instructions and runs at 6 MHz, faster than the
original Z80's 4 MHz.
