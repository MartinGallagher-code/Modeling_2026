# NEC V60

**Japan's first major 32-bit microprocessor, new proprietary ISA (1986)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1986 |
| Data Width | 32-bit |
| Clock | 16 MHz |
| CPI | ~3.0 cycles |
| Performance | ~5.33 MIPS |
| Transistors | ~375,000 |
| Address Space | 4 GB (32-bit) |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.67% |
| Tests Passing | 7/7 |

## Model Files

- `current/nec_v60_validated.py` - Active model
- `validation/nec_v60_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from nec_v60_validated import NecV60Model

model = NecV60Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The NEC V60 was Japan's first major 32-bit microprocessor, featuring a
completely new instruction set architecture (not x86 compatible like
NEC's V20/V30). With ~375,000 transistors at 16 MHz, it included on-chip
floating point and string manipulation instructions. It was used in NEC
workstations and embedded systems. The V60 represented NEC's ambition to
create an independent processor architecture competitive with Western
designs like the Motorola 68020 and Intel 80386.
