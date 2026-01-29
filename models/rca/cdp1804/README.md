# RCA CDP1804

**COSMAC variant with on-chip timer (1980)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 2 MHz |
| CPI | ~10.0 cycles |
| Performance | ~200 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 8/8 |

## Model Files

- `current/cdp1804_validated.py` - Active model
- `validation/cdp1804_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from cdp1804_validated import Cdp1804Model

model = Cdp1804Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

Enhanced COSMAC with on-chip counter/timer. Compatible with 1802 instruction set
but approximately 17% faster due to process improvements. Timer provides interrupt
generation capability not available in base 1802.

## Comparison with 1802

| Feature | CDP1802 | CDP1804 |
|---------|---------|---------|
| CPI | 12.0 | 10.0 |
| On-chip Timer | No | Yes |
| Performance | ~167 KIPS | ~200 KIPS |
