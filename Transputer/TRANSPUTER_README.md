# INMOS Transputer CPU Queueing Model

## Executive Summary

The INMOS Transputer (1985, T800 in 1987) was the **first microprocessor designed from scratch for parallel computing**. With 4 on-chip communication links, hardware process scheduling, and 1µs context switches, it enabled massive parallelism. The Transputer was revolutionary technology that ultimately lost to commodity clusters.

**Key Finding:** The Transputer proves that architectural innovation can be ahead of its time. Its concepts of hardware-supported concurrency and message passing are now mainstream (in GPUs, network processors, and multicore designs), but INMOS didn't survive to see it.

---

## Technical Specifications

| Specification | T414 | T800 |
|---------------|------|------|
| Year | 1985 | 1987 |
| Word Size | 32 bits | 32 bits |
| Clock | 20 MHz | 20-30 MHz |
| On-chip RAM | **2 KB** | **4 KB** |
| FPU | No | **Yes** |
| Links | **4** | **4** |
| Link Speed | 10 Mbps | 20 Mbps |

---

## Revolutionary Features

### 4 Communication Links
```
Each Transputer has 4 serial links:
- Bidirectional
- DMA-driven
- 20 Mbps each (T800)
- Connect to other Transputers

Build any topology:
- Pipeline
- Array (2D, 3D)
- Tree
- Hypercube
```

### Hardware Process Scheduler
```
Built into the processor:
- Two priority levels
- Round-robin within priority
- 1 microsecond context switch!
- Hardware timer interrupts

Compare to software scheduling:
  Unix context switch: ~100µs
  Transputer: ~1µs (100× faster!)
```

### Designed for Occam
```
Occam: Parallel programming language

PAR        -- Parallel execution
  process1
  process2
  process3

SEQ        -- Sequential execution
  statement1
  statement2

channel ! data  -- Send on channel
channel ? data  -- Receive on channel

Transputer has HARDWARE support for channels!
```

---

## Stack Architecture

### Only 3 Registers!
```
A (Areg): Top of stack
B (Breg): Second
C (Creg): Third

Most operations use A and B:
  ADD   ; A := A + B, B := C
  
Workspace in on-chip RAM for variables.
```

### Why Stack-Based?
```
Benefits:
- Small instruction encoding
- Fast on-chip workspace
- Natural for Occam

Trade-off:
- Less efficient for some operations
- Harder to compile other languages
```

---

## Parallel Machines

### Meiko Computing Surface
```
Up to 1024 Transputers
Configurable topology
Used for:
- Weather modeling
- Physics simulation
- Financial modeling
```

### Famous Installations
| System | Transputers | Use |
|--------|-------------|-----|
| Meiko | 1024+ | HPC |
| Parsytec | 64-16384 | Scientific |
| Atari ATW800 | 1 | Workstation |

---

## Why It Failed

### The Problem
```
1. Commodity killed it:
   - Networks got fast (Ethernet → Gigabit)
   - Standard CPUs got cheap and fast
   - Clusters of PCs matched performance
   
2. Ecosystem issues:
   - Occam not mainstream
   - C compilers mediocre
   - Limited software
   
3. INMOS troubles:
   - Acquired by SGS-Thomson
   - Development slowed
   - Lost momentum
```

### The Irony
```
Transputer concepts are NOW mainstream:

- GPU: Thousands of parallel units
- Network processors: Parallel packet handling
- Multicore: Multiple CPUs with communication
- Message passing: Standard in distributed systems

INMOS was 20 years too early.
```

---

## Performance

### Single Transputer
```
T800 @ 20 MHz:
- Integer: ~10 MIPS
- Float: ~1.5 MFLOPS
- On-chip RAM: 50ns access
```

### Parallel Scaling
```
  1 Transputer:   10 MIPS
  4 Transputers:  ~38 MIPS (95% efficient)
 16 Transputers: ~140 MIPS (88% efficient)
 64 Transputers: ~500 MIPS (78% efficient)

Near-linear scaling for well-structured problems!
```

---

## Usage

```python
from transputer_model import TransputerQueueModel

model = TransputerQueueModel('transputer_model.json')
ipc, _ = model.predict_ipc(0.40)
print(f"IPC: {ipc:.4f}")

# See parallel scaling
for n in [1, 4, 16, 64]:
    scaling = model.parallel_scaling(n)
    print(f"{n} Transputers: {scaling['effective_mips']:.0f} MIPS")
```

---

## Legacy

### What Transputer Pioneered
1. Hardware-supported parallelism
2. On-chip communication links
3. Fast context switching
4. CSP-based programming (channels)

### Modern Echoes
- NVIDIA CUDA: Massive parallelism
- Go language: CSP-inspired channels
- MPI: Message passing standard
- Network processors: Packet-level parallelism

---

## Conclusion

The Transputer was revolutionary - the first processor designed from scratch for parallel computing. Its concepts of hardware-supported concurrency and message passing were 20 years ahead of their time. INMOS didn't survive, but Transputer ideas live on in GPUs, multicore processors, and modern concurrent programming.

**Lesson:** Being right isn't enough. The Transputer was technically correct but economically outcompeted by commodity hardware.

---

**Version:** 1.0 | **Date:** January 24, 2026
