# K1810VM88

**Soviet Intel 8088 clone (1980s)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1986 |
| Data Width | 8/16-bit |
| Clock | 5.0 MHz |
| CPI | ~5.0 |
| Performance | ~1.0 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 16/16 |

## Model Files

- `current/k1810vm88_validated.py` - Active model
- `validation/k1810vm88_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from k1810vm88_validated import K1810VM88Model

model = K1810VM88Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The K1810VM88 is a Soviet clone of the Intel 8088, the 8-bit external bus
variant of the 8086. Like the original 8088 used in the IBM PC, it features
a 16-bit internal architecture with an 8-bit external data bus and a 4-byte
instruction prefetch queue. It was used in Soviet IBM PC/XT compatible computers.
