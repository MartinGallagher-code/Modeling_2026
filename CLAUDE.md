# Claude Code Instructions for Modeling_2026

## Project Purpose

This repository contains grey-box queueing models for 61+ historical microprocessors (1971-1989). Each model predicts processor performance (CPI, IPC, IPS) using category-based instruction timing and M/M/1 queueing theory.

**Goal**: Achieve <5% CPI prediction error for each model compared to documented/expected values.

## Repository Structure

```
Modeling_2026/
├── CLAUDE.md                 # This file
├── index.json                # Master index of all processors
├── common/                   # Shared base classes and utilities
├── intel/                    # Intel processor models
├── motorola/                 # Motorola processor models
├── mos_wdc/                  # MOS Technology & WDC models
├── zilog/                    # Zilog processor models
└── other/                    # Other manufacturers
```

Each processor has:
```
[processor]/
├── README.md                           # Quick reference, validation status
├── current/
│   └── [processor]_validated.py        # Active model (edit this)
├── validation/
│   └── [processor]_validation.json     # Validation data and accuracy metrics
├── docs/                               # Architecture documentation
└── HANDOFF.md                          # Session handoff notes (create if missing)
```

## Working on Models

### Before Making Changes

1. **Read the current model** in `current/[processor]_validated.py`
2. **Read the validation file** in `validation/[processor]_validation.json` to understand current accuracy
3. **Read HANDOFF.md** if it exists - it contains context from previous sessions
4. **Check the architecture docs** in `docs/` for processor specifications

### Making Changes

1. **Test before and after** - always run the model to see current CPI/IPC before editing
2. **Make incremental changes** - adjust one parameter at a time when calibrating
3. **Document your reasoning** - update HANDOFF.md with what you changed and why

### After Making Changes

1. **Update validation JSON** with new accuracy metrics
2. **Update README.md** validation status if accuracy improved significantly
3. **Update HANDOFF.md** with session notes (see below)

## HANDOFF.md Requirements

Every model should have a `HANDOFF.md` file that captures session context. Create one if it doesn't exist.

### HANDOFF.md Template

```markdown
# [Processor] Model Handoff

## Current Status
- **Validation**: [PASSED/FAILED]
- **CPI Error**: [X.X%]
- **Last Updated**: [YYYY-MM-DD]

## Change Log

### [YYYY-MM-DD] - [Brief description]
**Changes made:**
- [List specific parameter changes]
- [List algorithm changes]

**Reasoning:**
- [Why these changes were made]

**Results:**
- CPI before: X.XX
- CPI after: X.XX
- Error reduced from X% to X%

**What didn't work:**
- [Approaches tried that didn't improve accuracy]
- [Parameters adjusted that made things worse]

---

## Known Issues
- [Any remaining problems or inaccuracies]

## Suggested Next Steps
- [What should be done in future sessions]
- [Specific improvements to investigate]

## Key Architectural Notes
- [Important processor characteristics that affect modeling]
- [Non-obvious behaviors discovered during calibration]
```

## Common Model Parameters to Check

When a model has high error, check these common issues:

### Clock Speed
- Verify `clock_mhz` matches datasheet (not marketing speed)

### Cache/Memory
- `icache_hit_rate`, `dcache_hit_rate` - typically 0.90-0.98
- `memory_latency` - cycles to access main memory

### Branch Handling
- `has_delayed_branch` - many RISC processors have this
- `branch_delay_slots` - number of delay slots (1-3 typical)
- `branch_penalty` - cycles lost on misprediction

### Multi-cycle Instructions
- Multiply/divide cycles are often too high in templates
- Check if operations are pipelined (throughput vs latency)

### Superscalar/VLIW
- `dual_issue` or `superscalar` - can issue multiple instructions
- Efficiency factors for realistic utilization

### Workload Profiles
- Ensure profiles match processor's intended use case
- Scientific CPUs need more FP weight
- Microcontrollers need more I/O weight

## Validation Targets

| Error Range | Status |
|-------------|--------|
| <5% | PASSED - Good accuracy |
| 5-15% | MARGINAL - May need tuning |
| >15% | FAILED - Needs investigation |

## Testing a Model

```python
import sys
sys.path.insert(0, '[family]/[processor]/current')
from [processor]_validated import [Processor]Model

model = [Processor]Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```

## Reference Sources

When researching processor specifications:
- Original datasheets (check docs/ folder first)
- WikiChip: https://en.wikichip.org/
- Wikipedia technical articles
- CPU-World: https://www.cpu-world.com/
- Bitsavers: https://bitsavers.org/

## Important Notes

- **Don't over-engineer** - simple parameter adjustments often work better than algorithmic changes
- **Trust the architecture** - if a processor had delayed branches, model them
- **Consider the era** - 1970s processors are simpler than 1980s RISC machines
- **Check units** - MHz vs cycles vs nanoseconds can cause confusion
