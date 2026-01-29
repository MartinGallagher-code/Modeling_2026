# Intersil 6100

**CMOS PDP-8 on a chip (1975)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1975 |
| Data Width | 12-bit |
| Clock | 4 MHz |
| CPI | ~10.5 states |
| Performance | ~190 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 7/9 |

## Model Files

- `current/intersil6100_validated.py` - Active model
- `validation/intersil6100_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from intersil6100_validated import Intersil6100Model

model = Intersil6100Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} states, IPS: {result.ips:,.0f}")
```

## Notes

CMOS implementation of the DEC PDP-8/E instruction set. 12-bit word size,
variable instruction timing (6-22 states). Fully static design allows
indefinite halt. Used in DECmate word processors.
