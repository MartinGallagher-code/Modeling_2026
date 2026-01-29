# IM1821VM85A

**Soviet Intel 8085 clone (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 3.0 MHz |
| CPI | ~5.0 |
| Performance | ~0.60 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.5% |
| Tests Passing | 15/15 |

## Model Files

- `current/im1821vm85a_validated.py` - Active model
- `validation/im1821vm85a_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from im1821vm85a_validated import IM1821VM85AModel

model = IM1821VM85AModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The IM1821VM85A is a Soviet clone of the Intel 8085 microprocessor, produced
in 1985. It maintains full instruction set and timing compatibility with
the original. The 8085 improved on the 8080 with a multiplexed address/data
bus, serial I/O, and enhanced interrupt handling. Used in Soviet military
electronics and industrial controllers.
