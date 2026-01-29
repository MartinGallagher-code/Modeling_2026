# VEB U808

**First East German microprocessor - Intel 8008 clone (1978)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1978 |
| Data Width | 8-bit |
| Clock | 0.5 MHz |
| CPI | ~10.0 |
| Performance | ~50 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 14/14 |

## Model Files

- `current/u808_validated.py` - Active model
- `validation/u808_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from u808_validated import U808Model

model = U808Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The VEB U808 was the first microprocessor produced in East Germany (DDR),
manufactured by VEB Mikroelektronik Erfurt in 1978. It is a clone of the
Intel 8008, the world's first 8-bit microprocessor. The U808 has identical
instruction timing to the 8008 with its 8-bit data bus and 14-bit address
bus supporting 16KB of memory. It was used in early East German industrial
controllers and educational systems.
