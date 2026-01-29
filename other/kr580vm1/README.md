# KR580VM1

**Soviet Intel 8080 extension with 128KB bank-switched memory (1980)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 2.5 MHz |
| CPI | ~8.0 |
| Performance | ~312 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | <1% |
| Tests Passing | 15/15 |

## Model Files

- `current/kr580vm1_validated.py` - Active model
- `validation/kr580vm1_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from kr580vm1_validated import KR580VM1Model

model = KR580VM1Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The KR580VM1 is NOT a direct Intel 8080 clone. It extends the 8080 ISA with
bank-switching capability, doubling the addressable memory from 64KB to 128KB.
This makes it unique among Eastern Bloc 8080-derived processors. The base
instruction timing matches the 8080, but bank-switch operations add overhead,
resulting in a slightly higher typical CPI of 8.0 compared to the 8080's 7.5.
