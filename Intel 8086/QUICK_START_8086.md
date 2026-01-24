# Quick Start Guide - IBM PC 8086 CPU Queueing Model

**Version:** 1.0  
**Date:** January 22, 2026  
**Target System:** IBM PC with Intel 8086/8088 CPU @ 4.77 MHz

---

## Key Differences from Other CPUs

### The 8086: First x86 with Pipeline

Unlike the 6502 (sequential) and modern CPUs (20+ stages):
- ✅ **2-stage pipeline** - First x86 with instruction prefetch!
- ✅ **BIU/EU separation** - Bus Interface Unit and Execution Unit work in parallel
- ✅ **6-byte prefetch queue** - Decouples fetch from execute
- ❌ **No cache** - Direct DRAM access
- ❌ **No branch prediction** - Queue flushes on jumps
- ✅ **Variable cycles** - 2 to 162 cycles per instruction!

### What This Means for the Model

The queueing model is intermediate complexity:
- 2 stages that can overlap (BIU fetches while EU executes)
- Queue effectiveness depends on code characteristics
- Jumps/branches flush the queue (major penalty)
- CPI highly dependent on instruction mix and addressing modes

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
1. `ibm_pc_8086_model.json` - Model configuration
2. `ibm_pc_8086_model.py` - Python implementation
3. `QUICK_START_8086.md` - This guide

---

## Quick Start (5 minutes)

### Step 1: Run the Example

```bash
python3 ibm_pc_8086_model.py
```

**Expected Output:**
```
IBM PC 8086 CPU Queueing Model - Example Run

1. BASELINE PERFORMANCE
--------------------------------------------------------------------------------
================================================================================
IBM PC 8086 CPU QUEUEING MODEL - PERFORMANCE REPORT
================================================================================

Overall Performance:
  CPI:        4.5000 cycles/instruction
  IPC:        0.2222 instructions/cycle
  Clock:      4.770 MHz
  Throughput: 1.06 MIPS (million instructions/sec)
  Bottleneck: Execution Unit (EU) - Decode/Execute (ρ = 0.800)
  Queue Eff.: 85.0% (prefetch queue effectiveness)
...
```

### Step 2: Understand the Output

**Key Metrics:**
- **CPI (Cycles Per Instruction)**: Lower is better (typical range: 3.0-8.0)
- **IPC (Instructions Per Cycle)**: Still < 1.0 (simple 2-stage pipeline)
- **Throughput**: Instructions per second (typically 0.8-1.3 MIPS)
- **Queue Efficiency**: How often prefetch queue has instructions ready
- **Bottleneck**: Usually EU (execution slower than fetch)

**Interpretation:**
- CPI = 4.5 means average instruction takes 4.5 clock cycles
- At 4.77 MHz, this gives ~1.06 million instructions/second
- Queue efficiency 85% means queue is effective (15% empty stalls)
- EU bottleneck means execution is slower than fetch

---

## Basic Usage Examples

### Example 1: Compute Baseline Performance

```python
from ibm_pc_8086_model import IBMPC8086Model

# Load model
model = IBMPC8086Model('ibm_pc_8086_model.json')

# Compute performance at 80% utilization
result = model.compute_pipeline_performance()

print(f"CPI: {result.cpi:.3f}")
print(f"Queue Efficiency: {result.queue_efficiency*100:.1f}%")
print(f"Throughput: {result.throughput_ips/1e6:.2f} MIPS")
```

### Example 2: Modify Instruction Mix

```python
# Simulate code with many jumps (poor queue efficiency)
model.update_parameters({
    'p_jump_short': 0.15,      # 15% conditional jumps
    'p_jump_far': 0.05,        # 5% unconditional jumps
    'p_queue_empty': 0.30,     # Queue empty 30% of time
})

result = model.compute_pipeline_performance()
print(f"Branch-heavy CPI: {result.cpi:.3f}")
print(f"Queue Efficiency: {result.queue_efficiency*100:.1f}%")
```

### Example 3: Compare Memory vs Register Operations

```python
# Memory-heavy code
model_mem = IBMPC8086Model('ibm_pc_8086_model.json')
model_mem.update_parameters({
    'p_alu_mem': 0.30,    # 30% memory ALU ops
    'p_mov': 0.35,        # 35% MOV (many to/from memory)
})
cpi_mem = model_mem.compute_pipeline_performance().cpi

# Register-optimized code
model_reg = IBMPC8086Model('ibm_pc_8086_model.json')
model_reg.update_parameters({
    'p_alu_reg': 0.40,    # 40% register ALU ops
    'p_alu_mem': 0.10,    # Only 10% memory ALU ops
    'p_mov': 0.20,        # Fewer MOVs
})
cpi_reg = model_reg.compute_pipeline_performance().cpi

speedup = cpi_mem / cpi_reg
print(f"Register optimization: {speedup:.2f}x faster!")
```

---

## Collecting Real System Data

### Using Cycle-Accurate Emulators

#### DOSBox (With Cycle Counting Patch)
```bash
# DOSBox-X has better cycle counting
# Download: https://dosbox-x.com/

# In dosbox-x.conf:
[cpu]
core=normal
cputype=8086
cycles=fixed 4770

# Run program and check cycles in debugger
```

#### PCem (Most Accurate)
```
1. Download PCem: https://pcem-emulator.co.uk/
2. Configure IBM PC 5150 with 8088
3. Load your program
4. Use built-in debugger for cycle counting
5. Extremely accurate timing simulation
```

#### 8086tiny (Lightweight)
```bash
# Tiny 8086 emulator with cycle counting
git clone https://github.com/adriancable/8086tiny
cd 8086tiny
./8086tiny program.com

# Add instrumentation to count cycles
```

### Using Real Hardware (Advanced)

```
Equipment needed:
- IBM PC, XT, or compatible
- Logic analyzer
- Test program on floppy disk

Method:
1. Attach logic analyzer to 8088 CLK pin
2. Set trigger on program start/end
3. Count clock cycles between triggers
4. Divide by instruction count from disassembly
```

### Using Disassembly (Static Analysis)

```bash
# Disassemble DOS .COM or .EXE file
ndisasm -b 16 program.com > program.asm

# Or use debug.exe on real DOS
DEBUG program.com
-u 100 200  (unassemble from 100h to 200h)

# Count instruction types
grep "mov" program.asm | wc -l
grep "add\|sub\|and\|or\|xor" program.asm | wc -l
grep "jmp\|je\|jne\|jz" program.asm | wc -l
```

---

## Parameter Guide

### Known Parameters (From 8086 Datasheet)

| Parameter | Value | Source | Description |
|-----------|-------|--------|-------------|
| `cycles_bus_access` | 4 cycles | Datasheet | Bus cycle for 16-bit word read |
| `cycles_alu_reg` | 3 cycles | Datasheet | Register ALU ops (ADD, SUB, etc.) |
| `prefetch_queue_size` | 6 bytes | Datasheet | Instruction prefetch queue |
| `clock_freq_hz` | 4,770,000 | Hardware | IBM PC clock frequency |

### Unknown Parameters (Calibrate from Measurements)

| Parameter | Typical Range | Calibration Source |
|-----------|---------------|--------------------|
| `p_mov` | 0.20 - 0.35 | Instruction profiling |
| `p_alu_reg` | 0.15 - 0.30 | Instruction profiling |
| `p_alu_mem` | 0.10 - 0.25 | Instruction profiling |
| `p_jump_short` | 0.05 - 0.15 | Execution profiling |
| `p_call_ret` | 0.04 - 0.12 | Instruction profiling |
| `p_queue_empty` | 0.10 - 0.30 | Execution profiling |
| `cycles_mov` | 2.0 - 17.0 | Weighted by addressing modes |
| `cycles_alu_mem` | 9.0 - 25.0 | Weighted by addressing modes |
| `cycles_mul` | 70.0 - 130.0 | Weighted by data size |

### How to Extract Instruction Mix

**Method 1: Disassemble Program**
```bash
# Disassemble
ndisasm -b 16 program.com > program.asm

# Count each instruction type
grep "mov" program.asm | wc -l      # MOV instructions
grep "add\|sub" program.asm | wc -l  # ALU operations
grep "call\|ret" program.asm | wc -l # Procedure calls
grep "j[a-z]" program.asm | wc -l   # Jumps

# Calculate fractions
total=$(grep -c "^\s*[0-9A-F]" program.asm)
p_mov=$(echo "scale=4; $mov_count / $total" | bc)
```

**Method 2: Emulator Instruction Trace**
```python
# If emulator supports instruction tracing
# Example: DOSBox-X debug mode

# Parse trace output
with open('trace.txt') as f:
    instructions = []
    for line in f:
        # Extract instruction mnemonic
        parts = line.split()
        if len(parts) > 2:
            instructions.append(parts[2].upper())

from collections import Counter
counts = Counter(instructions)

# Group by category
mov_ops = counts['MOV']
alu_reg = counts['ADD'] + counts['SUB'] + counts['AND'] + counts['OR']
jumps = sum(counts[j] for j in ['JMP', 'JE', 'JNE', 'JZ', 'JNZ'])

total = sum(counts.values())
p_mov = mov_ops / total
p_alu_reg = alu_reg / total
p_jump_short = jumps / total
```

---

## 8086-Specific Considerations

### Effective Address (EA) Calculation

The 8086 adds cycles for memory address calculation:

```
Direct:           [1234h]         +0 cycles
Register:         [BX]            +5 cycles
Base+Index:       [BX+SI]         +7 cycles
Base+Index+Disp:  [BX+SI+10h]     +11 cycles
```

**Example:**
```assembly
MOV AX, [BX]        ; 8+5 = 13 cycles
MOV AX, [BX+SI]     ; 8+7 = 15 cycles
MOV AX, [BX+SI+10h] ; 8+11 = 19 cycles
```

**For accurate modeling**, weight by addressing mode usage:
```python
# If 40% use [BX], 30% use [BX+SI], 30% use [BX+SI+disp]:
cycles_mov = 0.40 * (8+5) + 0.30 * (8+7) + 0.30 * (8+11) = 14.0
```

### Prefetch Queue Behavior

The 6-byte queue is critical to performance:

**Queue Effectiveness Scenarios:**

1. **Sequential Code** (80-90% effective)
   - BIU keeps queue full
   - EU rarely waits
   - Best performance

2. **Some Branches** (50-70% effective)
   - Occasional queue flushes
   - Moderate performance

3. **Branch-Heavy** (20-40% effective)
   - Frequent queue flushes
   - Poor performance

**Measuring Queue Empty Rate:**
```python
# From execution profile or emulator
# Count cycles where EU stalls waiting for instruction

total_cycles = execution_time * clock_freq
eu_stall_cycles = count_stall_events()

p_queue_empty = eu_stall_cycles / total_cycles
```

### Jump Penalties

Jumps flush the prefetch queue:

**Conditional Jump:**
- Not taken: 4 cycles (no flush, instruction already in queue)
- Taken: 16 cycles (flush queue, refetch from jump target)

**Unconditional Jump (JMP):**
- Short: 15 cycles
- Near: 15 cycles
- Far: 15 cycles (different segment)

**Impact on CPI:**
```python
# 10% jumps with 50% taken rate
jump_overhead = 0.10 * (0.50 * 16 + 0.50 * 4) = 1.0 cycles per instruction
```

### String Operations (REP Prefix)

String operations are special:

```assembly
REP MOVSB   ; 9 + 17*CX cycles
REP STOSB   ; 9 + 10*CX cycles
```

If your code has string operations:
```python
# Average CX value (loop count)
avg_cx = 50  # Example: copying 50 bytes

# Cycles per string instruction
cycles_rep_movsb = 9 + 17 * avg_cx  # = 859 cycles!

# This dominates CPI if common
```

### Multiply/Divide Performance

These are VERY expensive:

```
MUL byte:  70-77 cycles
MUL word:  118-133 cycles
DIV byte:  80-90 cycles
DIV word:  144-162 cycles
```

**Impact Example:**
```python
# If 2% of instructions are MUL/DIV:
# Average 100 cycles each
# Adds: 0.02 * 100 = 2.0 cycles to overall CPI!
```

---

## Validation Checklist

### ✅ Before Calibration

- [ ] 8086 instruction reference available
- [ ] Program to analyze (DOS .COM or .EXE)
- [ ] Emulator or real hardware for testing
- [ ] Understanding of addressing modes

### ✅ During Calibration

- [ ] Measured CPI is reasonable (3.0 - 8.0 typical)
- [ ] Instruction mix fractions sum to 1.0
- [ ] Queue empty rate is 0.0-0.5
- [ ] Model converges within 20 iterations
- [ ] Final error < 5%

### ✅ After Calibration

- [ ] Predicted CPI matches measured within tolerance
- [ ] Queue efficiency matches expectations (60-90% typical)
- [ ] Bottleneck is reasonable (usually EU)
- [ ] Sensitivity analysis shows expected trends:
  - More memory ops → Higher CPI ✓
  - More jumps → Higher CPI ✓
  - More MUL/DIV → Much higher CPI ✓

---

## Common 8086 Benchmarks

### Dhrystone (8086 port)
- **Characteristics**: Integer computation benchmark
- **Typical CPI**: 4.5-5.5
- **Instruction mix**: Balanced ALU, memory, calls

### Norton SI (System Information)
- **Characteristics**: Mixed workload
- **Typical CPI**: 4.0-5.0
- **Instruction mix**: Memory-intensive

### Simple Loop (Synthetic)
```assembly
        MOV CX, 1000h     ; 4 cycles
LOOP_:  INC AX            ; 2 cycles
        DEC CX            ; 2 cycles
        JNZ LOOP_         ; 16 cycles (taken), 4 (not taken)
        
; Per iteration: 2 + 2 + 16 = 20 cycles / 3 instructions = 6.67 CPI
; Last iteration: 2 + 2 + 4 = 8 cycles / 3 instructions = 2.67 CPI
```

### Turbo Pascal Program
- **Characteristics**: Compiler-generated code
- **Typical CPI**: 5.0-6.0
- **Instruction mix**: Good register use, some memory access

---

## Troubleshooting

### Issue: Model predicts much lower CPI than measured

**Possible Causes:**
- Underestimating queue empty rate
- Missing procedure call overhead
- Not accounting for interrupt latency
- Memory wait states not modeled (8088 8-bit bus)

**Solutions:**
```python
# Increase queue empty rate (more jumps)
model.update_parameters({'p_queue_empty': 0.25})

# Increase CALL/RET overhead
model.update_parameters({'cycles_call_ret': 24})

# If using 8088 (8-bit bus), increase memory access time
model.update_parameters({'cycles_mov': 8.0})  # More memory penalty
```

### Issue: Model predicts much higher CPI than measured

**Possible Causes:**
- Overestimating expensive instructions
- Too pessimistic queue empty estimate
- Register-heavy code (underestimated)

**Solutions:**
```python
# Reduce memory operation cycles
model.update_parameters({'cycles_alu_mem': 11.0})

# Increase register operations
model.update_parameters({
    'p_alu_reg': 0.30,
    'p_alu_mem': 0.10
})

# Better queue efficiency (more sequential code)
model.update_parameters({'p_queue_empty': 0.08})
```

### Issue: Calibration oscillates, doesn't converge

**Cause:** Learning rate too high

**Solution:**
```python
model.calibration_config['learning_rate'] = 0.08  # Lower learning rate
```

---

## Example Calibration Workflow

### Step 1: Get Test Program

```assembly
; Simple test: sum.asm
        .model small
        .code
        org 100h
start:
        mov cx, 100         ; Loop 100 times
        xor ax, ax          ; Clear sum
loop_:
        add ax, cx          ; Add to sum
        dec cx              ; Decrement counter
        jnz loop_           ; Loop if not zero
        
        mov ah, 4Ch         ; DOS exit
        int 21h
end start
```

Assemble with:
```bash
masm sum.asm;
link sum;
exe2bin sum.exe sum.com
```

### Step 2: Measure in Emulator

```
Using DOSBox-X or PCem:
1. Load sum.com
2. Enable cycle counting
3. Run program
4. Record total cycles

Example result: 4,200 cycles for 100 iterations
```

### Step 3: Count Instructions

```
From disassembly:
- MOV CX, 100:  1 instruction (4 cycles) - once
- XOR AX, AX:   1 instruction (3 cycles) - once
- ADD AX, CX:   100 instructions (3 cycles each)
- DEC CX:       100 instructions (2 cycles each)
- JNZ:          99 taken (16 cyc) + 1 not taken (4 cyc)

Total cycles = 4 + 3 + (100*3) + (100*2) + (99*16) + 4 = 2,091

Wait, measured was 4,200! Why double?
→ Queue flushes on JNZ cause more delay
→ Instruction fetch overhead
```

### Step 4: Calculate Instruction Mix

```python
total_instructions = 1 + 1 + 100 + 100 + 100  # = 302
mov_count = 1
xor_count = 1
add_count = 100
dec_count = 100  
jnz_count = 100

instruction_mix = {
    'mov_fraction': 1 / 302,          # ~0.0033
    'alu_reg_fraction': 201 / 302,    # ~0.665 (XOR, ADD, DEC)
    'jump_short_fraction': 100 / 302, # ~0.331
    'queue_empty_rate': 0.20          # Estimate 20% from jumps
}

measured_cpi = 4200 / 302  # = 13.9 cycles/instruction
```

### Step 5: Calibrate

```python
model = IBMPC8086Model('ibm_pc_8086_model.json')

result = model.calibrate(
    measured_cpi=13.9,
    measured_instruction_mix=instruction_mix,
    tolerance_percent=5.0
)

print(f"Error: {result.error_percent:.2f}%")
```

---

## 8086 vs 8088 Differences

### IBM PC Uses 8088!

The IBM PC actually uses the 8088, not 8086:

| Feature | 8086 | 8088 (IBM PC) |
|---------|------|---------------|
| External Bus | 16-bit | **8-bit** |
| Bus Cycles | 4 T-states | 4 T-states |
| Memory Read | 2 bytes | **1 byte** |
| Queue Fill Rate | Faster | **Slower** |
| Performance | Better | **~70% of 8086** |

**Modeling 8088:**
```python
# Adjust for 8-bit bus (slower memory access)
model.update_parameters({
    'cycles_bus_access': 4,      # Same T-states
    'p_queue_empty': 0.25,       # Queue empties more often
    'cycles_mov': 8.0,           # Memory access slower (estimate)
})
```

---

## Advanced Topics

### Effective Address Calculation

Full EA calculation timing:

```
[disp]              = 6 cycles
[BX]                = 5 cycles
[BP]                = 5 cycles
[SI]                = 5 cycles
[DI]                = 5 cycles
[BX+SI]             = 7 cycles
[BX+DI]             = 8 cycles
[BP+SI]             = 8 cycles
[BP+DI]             = 7 cycles
[BX+SI+disp]        = 11 cycles
[BX+DI+disp]        = 12 cycles
[BP+SI+disp]        = 12 cycles
[BP+DI+disp]        = 11 cycles
```

### Segment Register Overhead

Segment override prefixes add cycles:
```assembly
MOV AX, [BX]        ; 13 cycles (default DS)
MOV AX, ES:[BX]     ; 15 cycles (ES override, +2)
```

### Interrupt Latency

Hardware interrupts take time:
```
INT instruction:    51 cycles
IRET:              24 cycles

If 1 interrupt per 1000 instructions:
Overhead = 75 / 1000 = 0.075 cycles per instruction
```

---

## Next Steps

1. **✅ Start simple**: Run the example and understand baseline
2. **📊 Collect data**: Use emulator or disassembly
3. **🎯 Calibrate**: Match model to your programs
4. **🔬 Analyze**: Use sensitivity analysis
5. **📈 Optimize**: Identify bottlenecks and improve code

---

## 8086 Instruction Cycle Reference

Quick reference for common instructions:

### Data Movement (MOV, PUSH, POP)
| Instruction | Cycles | Notes |
|-------------|--------|-------|
| MOV reg, reg | 2 | Fastest |
| MOV reg, mem | 8+EA | Memory read |
| MOV mem, reg | 9+EA | Memory write |
| MOV reg, imm | 4 | Immediate |
| PUSH reg | 11 | Stack push |
| POP reg | 8 | Stack pop |
| XCHG AX, reg | 3 | AX special case |
| XCHG reg, reg | 4 | General |

### Arithmetic/Logic (ADD, SUB, AND, OR, XOR)
| Instruction | Cycles | Notes |
|-------------|--------|-------|
| ADD reg, reg | 3 | Register only |
| ADD reg, mem | 9+EA | Memory source |
| ADD mem, reg | 16+EA | Memory destination |
| INC reg | 2 | Fast increment |
| INC mem | 15+EA | Memory increment |
| MUL reg8 | 70-77 | Byte multiply |
| MUL reg16 | 118-133 | Word multiply |
| DIV reg8 | 80-90 | Byte divide |
| DIV reg16 | 144-162 | Word divide |

### Control Transfer (JMP, Jcc, CALL, RET)
| Instruction | Cycles | Notes |
|-------------|--------|-------|
| JMP short | 15 | -128 to +127 |
| JMP near | 15 | Within segment |
| JMP far | 15 | Different segment |
| Jcc not taken | 4 | Conditional, prediction wrong |
| Jcc taken | 16 | Conditional, branch taken |
| LOOP (taken) | 17 | Decrement CX, jump if ≠0 |
| LOOP (not taken) | 5 | CX = 0 |
| CALL near | 19 | Within segment |
| CALL far | 28 | Different segment |
| RET near | 8 | Return near |
| RET far | 18 | Return far |

### String Operations
| Instruction | Cycles | Notes |
|-------------|--------|-------|
| MOVSB | 18 | Move byte |
| MOVSW | 18 | Move word |
| CMPSB | 22 | Compare byte |
| SCASB | 15 | Scan byte |
| LODSB | 12 | Load byte |
| STOSB | 11 | Store byte |
| REP MOVSB | 9+17×CX | Repeat move |
| REP STOSB | 9+10×CX | Repeat store |

---

## References

- **Intel 8086 Family User's Manual**: Official documentation
- **IBM PC Technical Reference**: Hardware specifications
- **The 8086/8088 Primer**: Peter Norton's guide
- **DOSBox-X**: https://dosbox-x.com/
- **PCem**: https://pcem-emulator.co.uk/
- **8086tiny**: https://github.com/adriancable/8086tiny

---

**Version:** 1.0  
**Last Updated:** January 22, 2026  
**Target:** IBM PC (Intel 8088 @ 4.77 MHz) and compatibles
