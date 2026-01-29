# RCA CDP1806

**Final COSMAC variant (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 5 MHz |
| CPI | ~8.0 cycles |
| Performance | ~625 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 8/8 |

## Model Files

- `current/cdp1806_validated.py` - Active model
- `validation/cdp1806_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from cdp1806_validated import Cdp1806Model

model = Cdp1806Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

Final and fastest COSMAC variant. Enhanced with faster clock (up to 5 MHz),
additional instructions, and improved bus timing. Fully backward compatible
with 1802/1804/1805 instruction set. Approximately 33% faster than original 1802.

## COSMAC Family Comparison

| Processor | Year | CPI | Performance |
|-----------|------|-----|-------------|
| CDP1802 | 1976 | 12.0 | ~167 KIPS |
| CDP1804 | 1980 | 10.0 | ~200 KIPS |
| CDP1806 | 1985 | 8.0 | ~625 KIPS |
