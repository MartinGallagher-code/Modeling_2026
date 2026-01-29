# Tesla MHB8080A

**Czechoslovak Intel 8080A clone by Tesla Piestany (1982)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1982 |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| CPI | ~7.5 |
| Performance | ~0.27 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.3% |
| Tests Passing | 15/15 |

## Model Files

- `current/tesla_mhb8080a_validated.py` - Active model
- `validation/tesla_mhb8080a_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tesla_mhb8080a_validated import TeslaMHB8080AModel

model = TeslaMHB8080AModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The Tesla MHB8080A is a Czechoslovak clone of the Intel 8080A, produced by
Tesla Piestany (now part of Slovakia). It was widely used in Czechoslovak
computers including the PMI-80 (a single-board educational computer) and the
PMD 85 (a home/personal computer). Tesla Piestany was one of the major
semiconductor manufacturers in the Eastern Bloc.
