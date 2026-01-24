# Apple IIc 6502 CPU Queueing Model - Project Overview

**Author:** Grey-Box Performance Modeling Research  
**Date:** January 22, 2026  
**Version:** 1.0 (6502 variant)  
**Target System:** Apple IIc with MOS 6502 @ 1.023 MHz

---

## What This Is

A **grey-box queueing model** adapted for the classic MOS 6502 microprocessor as used in the Apple IIc. This demonstrates how the grey-box methodology can be applied to vintage, non-pipelined CPUs.

---

## Why the 6502 is Perfect for Learning This Methodology

The 6502 is an ideal teaching platform because:

✅ **Simple architecture** - No pipeline, no cache, no speculation  
✅ **Well-documented** - Complete instruction timing is publicly available  
✅ **Deterministic** - Each instruction has a fixed cycle count  
✅ **Emulators available** - Easy to validate model predictions  
✅ **Historical importance** - Powers Apple II, Commodore 64, NES, Atari 2600  

---

## Files Included

| File | Purpose | Size |
|------|---------|------|
| **README_6502.md** | This overview document | ~12 KB |
| **QUICK_START_6502.md** | Getting started guide | ~18 KB |
| **apple_iic_6502_model.json** | Model configuration | ~8 KB |
| **apple_iic_6502_model.py** | Python implementation | ~25 KB |

---

## Model Architecture

### Visual Representation

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                  APPLE IIc 6502 CPU QUEUEING MODEL                        ║
║                                                                           ║
║  Key Insight: 6502 has NO PIPELINE - instructions execute sequentially   ║
║                                                                           ║
║                    λ (instructions/second)                                ║
║                             ↓                                             ║
║                                                                           ║
║    ┌────────────────────────────────────────────────────────┐            ║
║    │  Stage 1: Fetch (F)                                    │            ║
║    │  • Queue Type: M/M/1                                   │            ║
║    │  • Service Time: ~1 cycle (opcode fetch)               │            ║
║    │  • Purpose: Fetch next instruction byte from memory    │            ║
║    │  • Note: Can have +1 cycle page cross penalty          │            ║
║    └───────────────────────┬────────────────────────────────┘            ║
║                            ↓ λ                                            ║
║    ┌────────────────────────────────────────────────────────┐            ║
║    │  Stage 2: Decode/Execute (D/E)                         │            ║
║    │  • Queue Type: M/M/1                                   │            ║
║    │  • Service Time: 2-7 cycles (instruction dependent)    │            ║
║    │  • Purpose: ALL the work happens here                  │            ║
║    │    - Decode instruction                                │            ║
║    │    - Execute operation                                 │            ║
║    │    - Memory access (if needed)                         │            ║
║    │    - Write result                                      │            ║
║    │  • Bottleneck: Always this stage                       │            ║
║    └───────────────────────┬────────────────────────────────┘            ║
║                            ↓                                              ║
║                   Completed Instructions                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

Key Differences from Modern CPUs:
─────────────────────────────────
• NO instruction overlap (truly sequential execution)
• NO cache hierarchy (direct DRAM access, but fast enough at 1 MHz)
• NO branch prediction (all branches resolved immediately)
• NO speculative execution (only execute what's needed)
• CPI varies widely: 2-7 cycles per instruction
• Average CPI typically 3.0-4.5 depending on instruction mix
```

---

## Key Architecture Facts

### MOS 6502 Specifications

| Feature | Value |
|---------|-------|
| Clock Speed | 1.023 MHz (Apple IIc) |
| Data Bus | 8-bit |
| Address Bus | 16-bit (64 KB address space) |
| Registers | A (accumulator), X, Y (index), S (stack), P (status) |
| Pipeline Depth | 1 (no pipeline!) |
| Cache | None |
| Instruction Set | ~56 instructions, 13 addressing modes |
| Cycles/Instruction | 2-7 cycles (most common: 2-4) |

### What Makes the 6502 Different

**Sequential Execution:**
```
Modern CPU (pipelined):
Time:  T0    T1    T2    T3    T4    T5
       Fetch Decode Execute Memory WriteBack
             Fetch  Decode  Execute Memory   (overlapped)
                    Fetch   Decode  Execute
                           
6502 (non-pipelined):
Time:  T0    T1    T2    T3    T4    T5
       [Inst 1: 3 cycles    ]
                            [Inst 2: 2 cyc]
                                           [Inst 3...]
```

No overlap = Simple to model!

---

## Example Use Cases

### 1. Understanding Apple II BASIC Performance

```python
from apple_iic_6502_model import AppleIIc6502Model

model = AppleIIc6502Model('apple_iic_6502_model.json')

# BASIC interpreter has lots of indirection and subroutine calls
model.update_parameters({
    'p_load': 0.30,           # Heavy on loads
    'p_store': 0.15,          # Some stores
    'p_jmp_jsr': 0.10,        # Many subroutine calls
    'p_alu_simple': 0.25,
    'cycles_jmp_jsr': 5.5     # Average of JSR (6) and JMP (3)
})

result = model.compute_pipeline_performance()
print(f"BASIC CPI: {result.cpi:.2f}")
print(f"Throughput: {result.throughput_ips/1000:.1f} KIPS")
```

**Expected output:** CPI ≈ 3.8-4.2, throughput ≈ 240-270 KIPS

### 2. Comparing Different Code Styles

```python
# Assembly code with heavy zero-page usage (fast)
model_optimized = AppleIIc6502Model('apple_iic_6502_model.json')
model_optimized.update_parameters({
    'cycles_load': 3.0,      # More zero-page addressing
    'cycles_store': 3.2,
    'p_page_cross': 0.03     # Good data locality
})

# Assembly code with absolute addressing (slower)
model_unoptimized = AppleIIc6502Model('apple_iic_6502_model.json')
model_unoptimized.update_parameters({
    'cycles_load': 4.2,      # More absolute addressing
    'cycles_store': 4.8,
    'p_page_cross': 0.15     # Poor data locality
})

cpi_opt = model_optimized.compute_pipeline_performance().cpi
cpi_unopt = model_unoptimized.compute_pipeline_performance().cpi

speedup = cpi_unopt / cpi_opt
print(f"Optimized code is {speedup:.2f}x faster!")
```

### 3. Game Performance Analysis

```python
# Typical game loop: lots of memory access, some RMW for sprites
model_game = AppleIIc6502Model('apple_iic_6502_model.json')
model_game.update_parameters({
    'p_load': 0.35,          # Reading sprite data, game state
    'p_store': 0.20,         # Writing to screen memory
    'p_alu_rmw': 0.08,       # Sprite manipulation (INC, DEC, shifts)
    'p_alu_simple': 0.22,    # Position calculations
    'p_branch_taken': 0.08,  # Game logic branches
})

result = model_game.compute_pipeline_performance()
print(f"Game loop CPI: {result.cpi:.2f}")
print(f"Frame budget at 60 FPS: {1_023_000 / 60:.0f} cycles/frame")
print(f"Instructions per frame: {result.throughput_ips / 60:.0f}")
```

---

## Calibration Workflow

### Step-by-Step Process

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Choose Test Program                                       │
│    • Apple II software (BASIC, DOS, game)                    │
│    • Your own 6502 assembly code                             │
│    • Synthetic benchmark (loop, Dhrystone)                   │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. Measure Actual Performance                                │
│    Method A: Cycle-accurate emulator (AppleWin, MAME)       │
│    Method B: Real hardware with oscilloscope                 │
│    Method C: Theoretical calculation from disassembly        │
│                                                              │
│    Output: Total cycles, total instructions → CPI           │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. Extract Instruction Mix                                   │
│    Method A: Disassemble and count manually                  │
│    Method B: Emulator instruction trace                      │
│    Method C: Statistical sampling                            │
│                                                              │
│    Output: Fraction of each instruction type                │
│            p_load, p_store, p_alu_simple, etc.              │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ 4. Run Model Calibration                                     │
│    model.calibrate(                                          │
│        measured_cpi=3.8,                                     │
│        measured_instruction_mix={...},                       │
│        tolerance_percent=5.0                                 │
│    )                                                         │
│                                                              │
│    Model adjusts cycle counts to match measurement          │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ 5. Validate Results                                          │
│    • Error < 5%? ✓                                          │
│    • Sensitivities make sense? ✓                            │
│    • Test on different programs                              │
│    • Document calibrated parameters                          │
└──────────────────────────────────────────────────────────────┘
```

---

## What You Can Learn

### For Computer Architecture Students

1. **Sequential vs. Pipelined Execution**
   - See the difference between 6502 (no pipeline) and modern CPUs
   - Understand why CPI varies so much (2-7 cycles)
   - Learn how addressing modes affect performance

2. **Instruction Set Efficiency**
   - Compare 6502 (CISC-like) to modern RISC
   - Understand variable-length instruction encoding
   - See trade-offs: code density vs. decode complexity

3. **Memory System Design**
   - No cache, but didn't need it at 1 MHz!
   - Page boundary effects (256-byte pages)
   - Zero-page as "fast registers" (special addressing mode)

### For Performance Modelers

1. **Grey-Box Methodology Applied**
   - Known: Instruction cycle counts (from datasheet)
   - Grey: Instruction mix (from profiling)
   - Unknown: Average cycles per category (calibrated)

2. **Model Simplification**
   - 6502 model is much simpler than modern CPU
   - Yet captures essential performance characteristics
   - Shows minimum viable complexity

3. **Validation Against Ground Truth**
   - Cycle-accurate emulators provide "perfect" measurements
   - Can validate model to <1% error
   - Learn which simplifications matter

---

## Comparison: 6502 vs. Modern CPU Model

| Aspect | 6502 Model | Modern CPU Model |
|--------|------------|------------------|
| Pipeline Stages | 2 (Fetch, Decode/Execute) | 5+ (IF, ID, EX, MEM, WB) |
| Stage Overlap | None (sequential) | Full (pipelined) |
| Cache Modeling | Not needed | Critical (L1/L2/L3) |
| Branch Prediction | Not needed | Critical |
| CPI Range | 2-7 (instruction dependent) | 0.5-1.5 (average) |
| Bottleneck | Always Decode/Execute | Varies by workload |
| Model Complexity | Low | High |
| Calibration Difficulty | Easy | Moderate |
| Validation | Very accurate (<1%) | Good (2-5%) |

**Key Insight:** Starting with 6502 helps you understand the methodology without overwhelming complexity!

---

## Success Metrics

### Target Accuracy

| Metric | Target | Acceptable |
|--------|--------|------------|
| CPI prediction error | < 3% | < 5% |
| Throughput error | < 50 KIPS | < 100 KIPS |
| Relative comparison | Correct ranking | Within 10% |

### Example Validation

```python
# Known test case: Simple loop
# Theoretical CPI can be calculated exactly:
#   LDA $00: 3 cycles
#   CLC: 2 cycles  
#   ADC #$01: 2 cycles
#   STA $00: 3 cycles
#   CMP #$FF: 2 cycles
#   BNE (taken): 3 cycles
#   Total: 15 cycles / 6 instructions = 2.5 CPI

model = AppleIIc6502Model('apple_iic_6502_model.json')
# Set parameters for this specific mix...
result = model.compute_pipeline_performance()

error = abs(result.cpi - 2.5) / 2.5 * 100
assert error < 5%, f"Error {error:.1f}% exceeds 5% threshold"
```

---

## Tools and Resources

### Recommended Emulators

1. **AppleWin** (Windows, Wine on Linux)
   - Best cycle accuracy
   - Built-in debugger with cycle counting
   - https://github.com/AppleWin/AppleWin

2. **MAME** (Multi-platform)
   - Extremely accurate
   - Full system emulation
   - Command-line debugger
   - `mame apple2c -debug`

3. **OpenEmulator** (Mac/Linux)
   - Open source
   - Good debugging features
   - https://openemulator.github.io/

### Development Tools

1. **cc65** - C compiler and assembler for 6502
   - Includes `da65` disassembler
   - https://cc65.github.io/

2. **Visual 6502** - Transistor-level simulation
   - See actual chip operation
   - http://visual6502.org/

3. **6502 Reference** - Complete documentation
   - http://www.6502.org/

---

## Example Projects

### Project 1: Compare BASIC vs. Assembly

**Objective:** Quantify the performance difference

```python
# BASIC program characteristics
cpi_basic = calibrate_for_basic_program()

# Hand-optimized assembly equivalent
cpi_asm = calibrate_for_assembly_version()

speedup = cpi_basic / cpi_asm
print(f"Assembly is {speedup:.1f}x faster than BASIC")
# Expected: 5-10x speedup
```

### Project 2: Optimize Data Structures

**Objective:** Measure impact of data placement

```python
# Poor layout: data scattered, page crosses
model_poor = setup_poor_layout()
cpi_poor = model_poor.compute_pipeline_performance().cpi

# Good layout: zero-page, no page crosses
model_good = setup_good_layout()
cpi_good = model_good.compute_pipeline_performance().cpi

improvement = (cpi_poor - cpi_good) / cpi_poor * 100
print(f"Layout optimization: {improvement:.1f}% faster")
# Expected: 10-20% improvement
```

### Project 3: Game Loop Optimization

**Objective:** Find bottlenecks in game code

```python
# Baseline game loop
baseline = calibrate_game_loop()

# Try optimizations:
# 1. Unroll loops (less branching)
# 2. Use zero-page for hot variables
# 3. Optimize sprite routines

# Measure impact of each optimization
print(f"Loop unrolling: {measure_optimization_1():.1f}% faster")
print(f"Zero-page usage: {measure_optimization_2():.1f}% faster")
print(f"Sprite routine: {measure_optimization_3():.1f}% faster")
```

---

## Limitations

### What This Model Does NOT Capture

1. **Interrupts** - IRQ/NMI handling overhead not modeled
2. **I/O Wait States** - Assumes all memory is same speed
3. **DMA** - No modeling of DRAM refresh or DMA contention
4. **Temperature Effects** - Real hardware can have timing variations
5. **Undocumented Instructions** - Only official opcodes modeled

### When Model Accuracy Breaks Down

- Programs with heavy interrupt usage (>10% of time)
- Code that intentionally creates timing loops
- Hardware-specific quirks (different 6502 variants)
- Mixed with co-processors (if Apple IIc has expansion cards)

---

## Next Steps

### Quick Start (Today)

1. Run the example: `python3 apple_iic_6502_model.py`
2. Read `QUICK_START_6502.md`
3. Try modifying parameters and observe results

### Intermediate (This Week)

1. Get an emulator (AppleWin or MAME)
2. Load a simple 6502 program
3. Measure its performance
4. Calibrate the model to match

### Advanced (This Month)

1. Analyze a complete Apple II program
2. Optimize the code based on model insights
3. Validate optimizations on real hardware or emulator
4. Document your findings

### Research Direction (PhD Level)

1. Extend model to other 6502 variants (65C02, 65816)
2. Add interrupt modeling
3. Model multi-chip systems (6502 + custom chips)
4. Compare to other 8-bit CPUs (Z80, 8080)
5. Publish methodology paper

---

## Why This Matters

### Historical Perspective

The 6502 powered the personal computer revolution:
- **Apple II**: First widely successful personal computer
- **Commodore 64**: Best-selling single computer model ever
- **NES**: Revolutionized home video gaming
- **BBC Micro**: Introduced programming to UK children

Understanding its performance helps us appreciate:
- How programmers achieved amazing results with limited resources
- The evolution of computer architecture
- Trade-offs between simplicity and performance

### Educational Value

The 6502 is perfect for teaching because:
- Simple enough to understand completely
- Complex enough to be interesting
- Well-documented with 50+ years of literature
- Can actually run code and measure results
- Directly connects to computing history

### Relevance Today

These skills transfer to:
- Embedded systems (8051, ARM Cortex-M)
- Performance analysis of modern CPUs
- Understanding architectural trade-offs
- Grey-box modeling methodology
- Computer architecture research

---

## Contact and Contributions

This is an educational project demonstrating grey-box performance modeling applied to a classic CPU architecture.

**Questions?** Refer to:
1. `QUICK_START_6502.md` for practical guide
2. 6502 documentation at http://www.6502.org/
3. Original simple CPU documentation for methodology

**Found an issue?** Check that:
1. Instruction mix fractions sum to 1.0
2. Cycle counts are within documented ranges
3. Model parameters are within bounds
4. Python 3.8+ and numpy are installed

---

## Acknowledgments

- **MOS Technology** - Original 6502 designers
- **6502.org** - Comprehensive documentation archive
- **Visual 6502** - Transistor-level simulation project
- **Emulator developers** - AppleWin, MAME, OpenEmulator teams
- **Retrocomputing community** - Keeping the 6502 alive

Built on the foundation of the grey-box CPU modeling methodology to demonstrate how classical queueing theory can model even vintage computer architectures.

---

**Version:** 1.0  
**Date:** January 22, 2026  
**License:** Educational Use  
**Target:** Apple IIc (MOS 6502 @ 1.023 MHz)

---

*"The 6502 was arguably one of the most important chips in the history of computing. Not the fastest, not the most powerful, but the right chip at the right time that made personal computing accessible to everyone."*
