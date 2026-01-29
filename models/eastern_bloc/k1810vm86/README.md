# K1810VM86

**Soviet Intel 8086 clone (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 16-bit |
| Clock | 5.0 MHz |
| CPI | ~6.5 |
| Performance | ~0.77 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 16/16 |

## Model Files

- `current/k1810vm86_validated.py` - Active model
- `validation/k1810vm86_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from k1810vm86_validated import K1810VM86Model

model = K1810VM86Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The K1810VM86 is a Soviet clone of the Intel 8086, produced in 1985. It was
used in the ES-1841, a Soviet IBM PC compatible computer, and various other
Soviet personal computers. The processor maintains full instruction set and
timing compatibility with the original Intel 8086, including the 6-byte
instruction prefetch queue and segment-based memory model.
