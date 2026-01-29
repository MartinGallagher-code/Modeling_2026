# Toshiba TLCS-12A

**Improved TLCS-12, 12-bit NMOS minicomputer processor (1975)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1975 |
| Data Width | 12-bit |
| Clock | 2 MHz |
| CPI | ~6.0 cycles |
| Performance | ~333 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 4.17% |
| Tests Passing | 6/6 |

## Model Files

- `current/tlcs12a_validated.py` - Active model
- `validation/tlcs12a_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tlcs12a_validated import Tlcs12aModel

model = Tlcs12aModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The TLCS-12A was Toshiba's improved version of the TLCS-12 minicomputer
processor, using faster NMOS technology instead of the original PMOS.
This provided approximately 25% speed improvement (CPI 6.0 vs 8.0)
while maintaining software compatibility. The 12-bit word size was
common in minicomputers of the era.

## Comparison with TLCS-12

| Feature | TLCS-12 | TLCS-12A |
|---------|---------|----------|
| Technology | PMOS | NMOS |
| CPI | 8.0 | 6.0 |
| Speed Improvement | - | ~25% faster |
