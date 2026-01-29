# KR581IK1

**Soviet WD MCP-1600 clone - control/microcode chip (1983)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1983 |
| Data Width | 16-bit |
| Clock | 2.5 MHz |
| CPI | ~8.0 |
| Performance | ~0.31 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.9% |
| Tests Passing | 14/14 |

## Model Files

- `current/kr581ik1_validated.py` - Active model
- `validation/kr581ik1_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from kr581ik1_validated import KR581IK1Model

model = KR581IK1Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The KR581IK1 is part 1 (control/microcode) of a Soviet clone of the Western
Digital MCP-1600 chipset. Used together with KR581IK2 (data path), it forms
a complete PDP-11 compatible CPU. This chipset was used in the Elektronika-60
series of Soviet minicomputers, which were LSI-11 compatible.
