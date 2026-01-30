# K580IK51

**Soviet 8051-compatible microcontroller (1980s)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1986 |
| Data Width | 8-bit |
| Clock | 6.0 MHz |
| CPI | ~2.0 |
| Performance | ~3.0 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 16/16 |

## Model Files

- `current/k580ik51_validated.py` - Active model
- `validation/k580ik51_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from k580ik51_validated import K580IK51Model

model = K580IK51Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The K580IK51 is a Soviet clone of the Intel 8051 microcontroller. It features
on-chip RAM, ROM, timers, serial port, and bit-addressable memory, making it
suitable for embedded control applications. Most instructions execute in 1-2
machine cycles, giving it a low CPI of approximately 2.0. It was widely used in
Soviet industrial control and embedded systems.
