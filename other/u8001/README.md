# VEB U8001

**First 16-bit microprocessor in the Eastern Bloc - Zilog Z8001 clone (1984)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Data Width | 16-bit |
| Clock | 4.0 MHz |
| CPI | ~5.5 |
| Performance | ~0.73 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/u8001_validated.py` - Active model
- `validation/u8001_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from u8001_validated import U8001Model

model = U8001Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The VEB U8001 was the first 16-bit microprocessor produced in the Eastern Bloc,
manufactured by VEB Mikroelektronik Erfurt in 1984. It is a clone of the Zilog
Z8001 with segmented memory management supporting 8MB of addressable memory.
It features 16 general-purpose 16-bit registers and hardware multiply/divide.
Used in East German industrial systems and military applications.
