# MCY7880

**Polish Intel 8080A clone (1979)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1979 |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| CPI | ~5.5 |
| Performance | ~0.364 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/mcy7880_validated.py` - Active model
- `validation/mcy7880_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from mcy7880_validated import MCY7880Model

model = MCY7880Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The MCY7880 was a Polish clone of the Intel 8080A produced by CEMI (Centrum
Naukowo-Produkcyjne Elektroniki) in 1979. It was fully compatible with the
original 8080A instruction set and timing. It was used in Polish computer
systems including the Meritum and Elwro 800 Junior.
