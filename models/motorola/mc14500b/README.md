# Motorola MC14500B

1-bit Industrial Control Unit (1976)

- Datapath: 1-bit
- Clock: 1 MHz @ 5V (4 MHz @ 15V)
- Transistors: ~500
- Instructions: 16 (all execute in 1 cycle)
- Use: Ladder/relay logic replacement, industrial control

## Model

Path: `motorola/mc14500b/current/mc14500b_validated.py`

```python
from motorola.mc14500b.current.mc14500b_validated import Mc14500bModel

m = Mc14500bModel()
res = m.analyze('typical')
print(m.name, res.cpi, int(res.ips), res.bottleneck)
# MC14500B 1.0 1000000 logic

v = m.validate()
print(f"Tests: {v['passed']}/{v['total']}")
```

Workloads: `typical`, `logic_heavy`, `control`, `io`.

CPI = 1.0 for all workloads (fixed single-cycle timing).

## Sources

- [MC14500B Handbook (1977)](http://www.bitsavers.org/components/motorola/14500/MC14500B_Industrial_Control_Unit_Handbook_1977.pdf)
- [Ken Shirriff reverse-engineering](http://www.righto.com/2021/02/a-one-bit-processor-explained-reverse.html)
- [WikiChip](https://en.wikichip.org/wiki/motorola/mc14500/mc14500b)
