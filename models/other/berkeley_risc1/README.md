# Berkeley RISC I

**First RISC processor (UC Berkeley, 1982)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1982 |
| Data Width | 32-bit |
| Clock | 4 MHz |
| CPI | ~1.3 |
| Performance | ~3 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 7/7 |

## Model Files

- `current/berkeley_risc1_validated.py` - Active model
- `validation/berkeley_risc1_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from berkeley_risc1_validated import BerkeleyRisc1Model

model = BerkeleyRisc1Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The first RISC processor, designed by Patterson and Sequin at UC Berkeley.
Features 2-stage pipeline, 78 registers with 6 overlapping windows, and
delayed branches. Direct ancestor of Sun SPARC architecture.
