# GI AY-3-8900 (STIC) Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.3%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: Programmable sprite processor (1978)
- Clock: 3.58 MHz, ~6000 transistors
- 4 instruction categories: sprite_engine(7c), background(5c), collision(4c), sync(3c)
- M/M/1 queueing with 6% overhead factor
- Workload-specific utilizations: typical=0.75, idle=0.45, sprite_heavy=0.85
- Predicted typical CPI: 6.136 (target: 6.0)

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| typical | 6.136 | 0.1630 | 583,442 |
| sprite_heavy | 7.504 | 0.1333 | 477,079 |
| background_scroll | 5.841 | 0.1712 | 612,909 |
| idle | 4.249 | 0.2354 | 842,587 |

## Known Issues
- Uses domain-specific workloads rather than standard compute/memory/control
- Sprite-heavy workload may show unrealistic CPI under extreme load

## Suggested Next Steps
- No urgent changes needed - model passes validation at 2.3% error
- Could investigate real Intellivision game workload profiles for further validation

## Key Architectural Notes
- Intellivision Standard Television Interface Chip (STIC)
- 8 hardware sprites with collision detection
- Background tiles from GRAM/GROM
- Bus handoff with CP1610 CPU during VBLANK

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.16%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
