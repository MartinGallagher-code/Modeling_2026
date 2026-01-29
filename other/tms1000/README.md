# TI TMS1000

**First commercially available single-chip microcontroller (1974)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1974 |
| Data Width | 4-bit |
| Clock | 300 kHz (typical) |
| CPI | 6.0 (fixed) |
| Performance | ~50 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 10/10 |

## Model Files

- `current/tms1000_validated.py` - Active model
- `validation/tms1000_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tms1000_validated import Tms1000Model

model = Tms1000Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

All 43 base instructions execute in exactly 6 clock cycles. The model is
trivially accurate due to this fixed timing. Harvard architecture with
4-bit data path and BCD arithmetic support.
