# Harris HM6100

**Faster CMOS PDP-8 (1978)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1978 |
| Data Width | 12-bit |
| Clock | 4 MHz |
| CPI | ~8.0 states |
| Performance | ~313 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 10/10 |

## Model Files

- `current/hm6100_validated.py` - Active model
- `validation/hm6100_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from hm6100_validated import Hm6100Model

model = Hm6100Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} states, IPS: {result.ips:,.0f}")
```

## Notes

Faster CMOS implementation of the PDP-8/E instruction set. Harris second-sourced
the Intersil 6100 with improved process technology, achieving approximately 24%
faster operation. Full software compatibility with Intersil 6100 and PDP-8/E.

## Comparison with Intersil 6100

| Feature | Intersil 6100 | Harris HM6100 |
|---------|---------------|---------------|
| Year | 1975 | 1978 |
| CPI | 10.5 states | 8.0 states |
| State Time | 500ns | 400ns |
| Performance | ~190 KIPS | ~313 KIPS |
| Improvement | - | ~65% faster |
