# Quick Start Guide - Apple IIc 6502 CPU Queueing Model

**Version:** 1.0  
**Date:** January 22, 2026  
**Target System:** Apple IIc with MOS 6502 CPU @ 1.023 MHz

---

## Key Differences from Modern CPUs

### The 6502 is NOT a Pipelined CPU

Unlike modern processors, the 6502:
- ❌ **No instruction pipeline** - instructions execute sequentially
- ❌ **No cache** - all memory access goes directly to DRAM
- ❌ **No branch prediction** - branches always cause control flow changes
- ❌ **No out-of-order execution** - strictly sequential
- ✅ **Simple and deterministic** - cycle counts are well-documented

### What This Means for the Model

The queueing model is greatly simplified:
- Only 2 stages: Fetch → Decode/Execute
- CPI is determined almost entirely by instruction mix
- No complex cache miss modeling needed
- Performance is highly predictable

---

## Installation and Setup

### Prerequisites
```bash
# Python 3.8+
python3 --version

# Required packages
pip3 install numpy
```

### Files Required
1. `apple_iic_6502_model.json` - Model configuration
2. `apple_iic_6502_model.py` - Python implementation
3. `QUICK_START_6502.md` - This guide

---

## Quick Start (5 minutes)

### Step 1: Run the Example

```bash
python3 apple_iic_6502_model.py
```

**Expected Output:**
```
Apple IIc 6502 CPU Queueing Model - Example Run

1. BASELINE PERFORMANCE
--------------------------------------------------------------------------------
================================================================================
APPLE IIc 6502 CPU QUEUEING MODEL - PERFORMANCE REPORT
================================================================================

Overall Performance:
  CPI:        3.5000 cycles/instruction
  IPC:        0.2857 instructions/cycle
  Clock:      1.023 MHz
  Throughput: 292.3 KIPS (thousand instructions/sec)
  Bottleneck: Decode/Execute (D/E) (ρ = 0.800)
...
```

### Step 2: Understand the Output

**Key Metrics:**
- **CPI (Cycles Per Instruction)**: Lower is better (typical range: 2.5-4.5)
- **IPC (Instructions Per Cycle)**: Always < 1.0 for 6502 (no pipeline!)
- **Throughput**: Instructions per second (typically 250-350 KIPS)
- **Bottleneck**: Almost always the Decode/Execute stage

**Interpretation:**
- CPI = 3.5 means average instruction takes 3.5 clock cycles
- At 1.023 MHz, this gives ~292,000 instructions/second
- The Decode/Execute stage dominates (it does all the real work)

---

## Basic Usage Examples

### Example 1: Compute Baseline Performance

```python
from apple_iic_6502_model import AppleIIc6502Model

# Load model
model = AppleIIc6502Model('apple_iic_6502_model.json')

# Compute performance at 80% utilization
result = model.compute_pipeline_performance()

print(f"CPI: {result.cpi:.3f}")
print(f"Throughput: {result.throughput_ips/1000:.1f} KIPS")
```

### Example 2: Modify Instruction Mix

```python
# Simulate a compute-heavy program (less memory access)
model.update_parameters({
    'p_load': 0.20,        # Fewer loads
    'p_store': 0.10,       # Fewer stores
    'p_alu_simple': 0.50,  # More ALU operations
})

result = model.compute_pipeline_performance()
print(f"Compute-bound CPI: {result.cpi:.3f}")
```

### Example 3: Analyze Sensitivity

```python
# Which instruction types matter most?
sensitivities = model.full_sensitivity_analysis()

for param, sens in sensitivities.items():
    print(f"{param}: Elasticity = {sens['elasticity']:+.4f}")
```

**Interpretation:**
- **Positive elasticity**: More of this instruction type → Higher CPI (slower)
- **Negative elasticity**: More of this instruction type → Lower CPI (faster)
- **Large |elasticity|**: This parameter strongly affects performance

---

## Collecting Real System Data

### Using Cycle-Accurate Emulators

#### AppleWin (Recommended for Windows)
```
1. Download AppleWin: https://github.com/AppleWin/AppleWin
2. Load your program (disk image or binary)
3. Enable cycle counting in debugger
4. Run program and record total cycles
5. Disassemble to count instruction types
```

#### OpenEmulator (Mac/Linux)
```
1. Download OpenEmulator: https://openemulator.github.io/
2. Load Apple IIc ROM and your program
3. Use built-in debugger to count cycles
4. Export execution trace for analysis
```

#### MAME (Multi-platform, very accurate)
```bash
# Run Apple IIc emulation with debugger
mame apple2c -debug

# Use debugger commands:
# - Step through execution
# - Count cycles
# - Trace instruction execution
```

### Using Real Hardware (Advanced)

```
Equipment needed:
- Apple IIc computer
- Logic analyzer or oscilloscope
- Test program in ROM or disk

Method:
1. Attach logic analyzer to CPU clock pin
2. Attach to address/data bus (optional)
3. Run known test program
4. Count clock cycles between start/end markers
5. Divide by instruction count
```

### Using Disassembly (Static Analysis)

```bash
# Disassemble a program
da65 -o output.asm program.bin

# Count instruction types manually or with script:
grep "LDA" output.asm | wc -l   # Count loads
grep "STA" output.asm | wc -l   # Count stores
grep "ADC" output.asm | wc -l   # Count adds
# etc.

# Look up cycle counts in 6502 reference manual
# Calculate weighted average CPI
```

---

## Parameter Guide

### Known Parameters (From 6502 Datasheet)

| Parameter | Value | Source | Description |
|-----------|-------|--------|-------------|
| `cycles_fetch_base` | 1 cycle | Datasheet | Base opcode fetch time |
| `cycles_alu_simple` | 2 cycles | Datasheet | Simple ALU ops (ADC, CMP, etc.) |
| `cycles_alu_rmw` | 6 cycles | Datasheet | Read-Modify-Write (INC, DEC, etc.) |
| `cycles_branch_taken` | 3.5 cycles | Datasheet | Taken branch (with page cross) |
| `cycles_branch_not_taken` | 2 cycles | Datasheet | Not-taken branch |
| `penalty_page_cross` | 1 cycle | Datasheet | Page boundary crossing penalty |
| `clock_freq_hz` | 1,023,000 | Hardware | Apple IIc clock frequency |

### Unknown Parameters (Calibrate from Measurements)

| Parameter | Typical Range | Calibration Source |
|-----------|---------------|--------------------|
| `p_load` | 0.20 - 0.35 | Instruction profiling |
| `p_store` | 0.10 - 0.20 | Instruction profiling |
| `p_alu_simple` | 0.25 - 0.40 | Instruction profiling |
| `p_alu_rmw` | 0.03 - 0.10 | Instruction profiling |
| `p_branch_taken` | 0.03 - 0.10 | Execution profiling |
| `p_branch_not_taken` | 0.03 - 0.10 | Execution profiling |
| `p_jmp_jsr` | 0.02 - 0.08 | Instruction profiling |
| `cycles_load` | 3.0 - 4.5 | Weighted by addressing modes |
| `cycles_store` | 3.5 - 5.0 | Weighted by addressing modes |
| `p_page_cross` | 0.02 - 0.15 | Execution profiling |

### How to Extract Instruction Mix

**Method 1: Disassemble Program**
```bash
# Disassemble
da65 program.bin > program.asm

# Count each instruction type
cat program.asm | grep -E "^\s+[A-F0-9]+\s+[A-F0-9]+\s+LDA" | wc -l
cat program.asm | grep -E "^\s+[A-F0-9]+\s+[A-F0-9]+\s+STA" | wc -l
# ... etc for each type

# Calculate fractions
total_instructions = sum of all counts
p_load = load_count / total_instructions
p_store = store_count / total_instructions
# ... etc
```

**Method 2: Emulator Instruction Trace**
```python
# If your emulator can export instruction trace
# Parse the trace file and count instruction types

with open('trace.txt') as f:
    instructions = [line.split()[2] for line in f]  # Extract opcode

from collections import Counter
counts = Counter(instructions)

# Group by type
loads = counts['LDA'] + counts['LDX'] + counts['LDY']
stores = counts['STA'] + counts['STX'] + counts['STY']
# ... etc

total = sum(counts.values())
p_load = loads / total
p_store = stores / total
```

**Method 3: Statistical Sampling**
```
For very large programs:
1. Run in emulator with random sampling
2. Every N cycles, record current instruction
3. Build histogram of instruction types
4. Calculate fractions from histogram
```

---

## 6502-Specific Considerations

### Addressing Mode Cycle Counts

Different addressing modes have different cycle counts:

```
LDA Immediate    #$00     2 cycles
LDA Zero Page    $00      3 cycles
LDA Zero Page,X  $00,X    4 cycles
LDA Absolute     $1234    4 cycles
LDA Absolute,X   $1234,X  4+ cycles (5 if page crossed)
LDA Absolute,Y   $1234,Y  4+ cycles (5 if page crossed)
LDA (Indirect,X) ($00,X)  6 cycles
LDA (Indirect),Y ($00),Y  5+ cycles (6 if page crossed)
```

**For accurate modeling**, weight by addressing mode usage:
```python
# Example: If 40% zero page, 30% absolute, 30% absolute indexed:
cycles_load = 0.40 * 3 + 0.30 * 4 + 0.30 * 4.5 = 3.55 cycles
```

### Page Boundary Crossing

Page boundaries occur every 256 bytes ($00-$FF, $100-$1FF, etc.)

Instructions that can cross page boundaries:
- Absolute indexed addressing (,X or ,Y)
- Indirect indexed addressing ((zp),Y)
- Taken branches that cross pages

**Measuring page cross rate:**
```
Method 1: Count instructions with indexed modes
Method 2: Analyze data access patterns
Method 3: Emulator instrumentation
```

Typical values:
- Well-optimized code: 5-8% page crosses
- Average code: 10-15% page crosses
- Poorly optimized: 20%+ page crosses

### Branch Behavior

The 6502 has no branch prediction - all branches are resolved immediately.

**Taken branch timing:**
- Same page: 3 cycles
- Page cross: 4 cycles

**Not-taken branch:** 2 cycles

**Measuring branch behavior:**
```python
# From emulator trace or disassembly
total_branches = count_all_branch_instructions()
taken_branches = count_branches_that_jump()

p_branch_taken = taken_branches / total_branches
p_branch_not_taken = 1 - p_branch_taken
```

### RMW (Read-Modify-Write) Operations

These are expensive on 6502:
- INC, DEC: 5-6 cycles
- ASL, LSR, ROL, ROR: 5-6 cycles

They require:
1. Read from memory
2. Modify value
3. Write back to memory

**Impact on CPI:**
- 10% RMW ops → CPI increases by ~0.3-0.4 cycles

---

## Validation Checklist

### ✅ Before Calibration

- [ ] 6502 instruction set reference available
- [ ] Cycle count table available (see below)
- [ ] Program to analyze (binary or source)
- [ ] Emulator or real hardware for testing

### ✅ During Calibration

- [ ] Measured CPI is reasonable (2.5 - 4.5 typical)
- [ ] Instruction mix fractions sum to 1.0
- [ ] Each instruction type fraction is 0.0-1.0
- [ ] Model converges within 20 iterations
- [ ] Final error < 5% (ideally < 3%)

### ✅ After Calibration

- [ ] Predicted CPI matches measured CPI within tolerance
- [ ] Calibrated cycle counts are within known bounds
- [ ] Sensitivity analysis shows expected trends:
  - More loads/stores → Higher CPI ✓
  - More simple ALU ops → Lower CPI ✓
  - More RMW ops → Higher CPI ✓
- [ ] Model predicts correctly on different programs

---

## Common 6502 Benchmarks

### Dhrystone (6502 port)
- **Characteristics**: Mixed integer operations
- **Typical CPI**: 3.2-3.6
- **Instruction mix**: 30% loads, 20% stores, 35% ALU

### Whetstone (if available)
- **Characteristics**: Floating-point (software)
- **Typical CPI**: 4.0-4.5
- **Instruction mix**: Heavy on loads/stores and subroutines

### Apple II BASIC Interpreter
- **Characteristics**: Interpreter overhead
- **Typical CPI**: 3.8-4.2
- **Instruction mix**: Many subroutine calls, table lookups

### Simple Loop (Synthetic)
```assembly
        LDA #$00      ; 2 cycles
LOOP    CLC           ; 2 cycles
        ADC #$01      ; 2 cycles
        CMP #$FF      ; 2 cycles
        BNE LOOP      ; 3 cycles (taken)
        RTS           ; 6 cycles

; Per iteration: 2 + 2 + 2 + 2 + 3 = 11 cycles / 5 instructions = 2.2 CPI
```

---

## Troubleshooting

### Issue: Model predicts CPI much lower than measured

**Possible Causes:**
- Underestimating page boundary crosses
- Missing subroutine call overhead
- Not accounting for interrupt handling
- Incorrect instruction mix (too many fast instructions)

**Solutions:**
```python
# Increase page cross rate
model.update_parameters({'p_page_cross': 0.12})

# Increase subroutine overhead
model.update_parameters({'cycles_jmp_jsr': 5.5})

# Recalibrate with adjusted mix
```

### Issue: Model predicts CPI much higher than measured

**Possible Causes:**
- Overestimating expensive instructions (RMW, indexed)
- Too pessimistic page cross estimate
- Incorrect cycle counts for addressing modes

**Solutions:**
```python
# Reduce RMW fraction
model.update_parameters({'p_alu_rmw': 0.04})

# Reduce average load cycles (more zero page)
model.update_parameters({'cycles_load': 3.2})
```

### Issue: Calibration doesn't converge

**Cause:** Model structure doesn't match program behavior

**Solutions:**
1. Double-check instruction mix (must sum to 1.0)
2. Verify cycle counts are within bounds
3. Increase max iterations
4. Try different programs for calibration

---

## Example Calibration Workflow

### Step 1: Get a Test Program

```assembly
; Simple test program: counter.asm
        .org $8000
        
START   LDA #$00        ; Initialize counter
        STA $00
        
LOOP    LDA $00         ; Load counter
        CLC
        ADC #$01        ; Increment
        STA $00         ; Store back
        CMP #$FF        ; Check limit
        BNE LOOP        ; Loop if not done
        
        RTS             ; Return
```

### Step 2: Measure on Real System or Emulator

```bash
# In AppleWin debugger or MAME:
# 1. Load program at $8000
# 2. Set breakpoint at START and at RTS
# 3. Run and record cycle count
# Example: 1,020,000 cycles for 255 iterations

# Calculate:
cycles_total = 1,020,000
iterations = 255
cycles_per_iteration = 1,020,000 / 255 = 4,000
instructions_per_iteration = 7  (count from disassembly)
CPI = 4,000 / (255 * 7) = 2.24 (if you count all instructions)

# Or count each instruction with its cycles:
# LDA #$00: 2 cycles (once)
# STA $00: 3 cycles (once + 255 times in loop)
# LDA $00: 3 cycles (255 times)
# CLC: 2 cycles (255 times)
# ADC #$01: 2 cycles (255 times)
# CMP #$FF: 2 cycles (255 times)
# BNE: 3 cycles (254 times, taken), 2 cycles (once, not taken)
# RTS: 6 cycles (once)
```

### Step 3: Extract Instruction Mix

```python
# For this simple program
total_instructions = 2 + 256 * 7  # Initial + loop iterations
load_count = 1 + 255  # LDA #$00 + LDA $00 in loop
store_count = 1 + 255  # STA $00
alu_count = 255 + 255 + 255  # CLC + ADC + CMP
branch_count = 255  # BNE

instruction_mix = {
    'load_fraction': load_count / total_instructions,      # ~0.14
    'store_fraction': store_count / total_instructions,     # ~0.14
    'alu_simple_fraction': alu_count / total_instructions,  # ~0.43
    'branch_taken_fraction': 254 / total_instructions,      # ~0.14
    'branch_not_taken_fraction': 1 / total_instructions,    # ~0.0006
    'jmp_jsr_fraction': 1 / total_instructions,             # ~0.0006
    'alu_rmw_fraction': 0.0,
}
```

### Step 4: Calibrate Model

```python
model = AppleIIc6502Model('apple_iic_6502_model.json')

result = model.calibrate(
    measured_cpi=2.24,  # From measurement
    measured_instruction_mix=instruction_mix,
    tolerance_percent=3.0
)

print(f"Error: {result.error_percent:.2f}%")
```

---

## 6502 Instruction Cycle Reference

Quick reference for common instructions:

### Data Movement
| Instruction | Addressing Mode | Cycles |
|-------------|----------------|--------|
| LDA #$00 | Immediate | 2 |
| LDA $00 | Zero Page | 3 |
| LDA $00,X | Zero Page,X | 4 |
| LDA $1234 | Absolute | 4 |
| LDA $1234,X | Absolute,X | 4* |
| STA $00 | Zero Page | 3 |
| STA $1234 | Absolute | 4 |

*Add 1 cycle if page boundary is crossed

### Arithmetic/Logic
| Instruction | Addressing Mode | Cycles |
|-------------|----------------|--------|
| ADC #$00 | Immediate | 2 |
| ADC $00 | Zero Page | 3 |
| ADC $1234 | Absolute | 4 |
| INC $00 | Zero Page | 5 |
| INC $1234 | Absolute | 6 |
| DEC $00 | Zero Page | 5 |

### Branches
| Instruction | Condition | Cycles |
|-------------|----------|--------|
| BEQ | Not taken | 2 |
| BEQ | Taken, same page | 3 |
| BEQ | Taken, page cross | 4 |

### Control Flow
| Instruction | Operation | Cycles |
|-------------|----------|--------|
| JMP $1234 | Absolute | 3 |
| JMP ($1234) | Indirect | 5 |
| JSR $1234 | Subroutine call | 6 |
| RTS | Return | 6 |

---

## Next Steps

1. **✅ Start simple**: Run the example and understand baseline
2. **📊 Collect data**: Use emulator or disassembly to get instruction mix
3. **🎯 Calibrate**: Match model to your specific programs
4. **🔬 Analyze**: Use sensitivity analysis to understand bottlenecks
5. **📈 Validate**: Test on multiple programs to ensure accuracy

---

## References

- **6502 Datasheet**: http://www.6502.org/documents/datasheets/mos/
- **6502 Instruction Set**: http://www.6502.org/tutorials/6502opcodes.html
- **AppleWin Emulator**: https://github.com/AppleWin/AppleWin
- **MAME Apple IIc**: https://docs.mamedev.org/
- **da65 Disassembler**: Part of cc65 toolkit

---

**Version:** 1.0  
**Last Updated:** January 22, 2026  
**Target:** Apple IIc (MOS 6502 @ 1.023 MHz)
