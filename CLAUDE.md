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
├── CHANGELOG.md                        # Cumulative history (append-only)
└── HANDOFF.md                          # Current state + next steps
```

## Working on Models

### Before Making Changes

1. **Read CHANGELOG.md first** - understand the full history of work on this model
2. **Read HANDOFF.md** - see current state and suggested next steps
3. **Read the current model** in `current/[processor]_validated.py`
4. **Read the validation file** in `validation/[processor]_validation.json` to understand current accuracy
5. **Check the architecture docs** in `docs/` for processor specifications

### Making Changes

1. **Test before and after** - always run the model to see current CPI/IPC before editing
2. **Make incremental changes** - adjust one parameter at a time when calibrating
3. **Document your reasoning** - you will record this in CHANGELOG.md

### After Making Changes

1. **Append to CHANGELOG.md** - add a new dated entry (never delete old entries)
2. **Update HANDOFF.md** - rewrite to reflect current state and next steps
3. **Update validation JSON** with new accuracy metrics
4. **Update README.md** validation status if accuracy improved significantly

## Model Documentation Files

Each model has two documentation files with distinct purposes:

| File | Purpose | Update Style |
|------|---------|--------------|
| `CHANGELOG.md` | Complete history of all work | **Append-only** - never delete |
| `HANDOFF.md` | Current state + next steps | **Rewrite** - keep focused |

### Why Two Files?

- **CHANGELOG.md** preserves institutional knowledge - everything ever learned, tried, or discovered about a model, including failed approaches
- **HANDOFF.md** stays concise and actionable - what you need to know right now to continue work

---

## CHANGELOG.md Requirements

**CRITICAL: This file is append-only. Never delete or modify previous entries.**

The changelog is a cumulative record of ALL work ever done on a model across ALL sessions. It captures:
- What was tried (successful and unsuccessful)
- What was learned about the processor
- Parameter values that worked or didn't work
- Architectural insights discovered
- Reference sources found

### CHANGELOG.md Template

```markdown
# [Processor] Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## [YYYY-MM-DD] - [Brief description]

**Session goal:** [What we were trying to achieve]

**Starting state:**
- CPI: X.XX (X% error)
- Key issues: [What was wrong]

**Changes attempted:**

1. [Change description]
   - Parameter: `name` changed from X to Y
   - Reasoning: [Why this change was made]
   - Result: [Did it help? By how much?]

2. [Another change]
   - ...

**What didn't work:**
- [Approach tried that failed or made things worse]
- [Parameter value that seemed logical but hurt accuracy]
- [Why it didn't work, if known]

**What we learned:**
- [Architectural insight about the processor]
- [Modeling insight that could apply to similar processors]
- [Useful reference found]

**Final state:**
- CPI: X.XX (X% error)
- Validation: [PASSED/FAILED]

**References used:**
- [URLs, datasheets, papers consulted]

---
```

---

## HANDOFF.md Requirements

HANDOFF.md captures the current state and immediate next steps. It can be rewritten each session to stay focused and actionable.

### HANDOFF.md Template

```markdown
# [Processor] Model Handoff

## Current Status
- **Validation**: [PASSED/FAILED]
- **CPI Error**: [X.X%]
- **Last Updated**: [YYYY-MM-DD]

## Current Model Summary
- [Key parameters and their values]
- [Architecture type being modeled]

## Known Issues
- [Any remaining problems or inaccuracies]
- [Workloads that don't validate well]

## Suggested Next Steps
- [What should be done in future sessions]
- [Specific improvements to investigate]
- [Questions that need research]

## Key Architectural Notes
- [Important processor characteristics that affect modeling]
- [Non-obvious behaviors to remember]
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
