# System Identification Preparation for Grey-Box Queueing Models

## 1. Standardize a Measurement Data Format

Create a schema for storing actual CPU measurements. You'll need observed data to identify against. Something like:

```
models/<family>/<processor>/measurements/
├── measured_cpi.json        # Actual CPI from real hardware or cycle-accurate sims
└── instruction_traces.json  # Per-instruction or per-category observed timings
```

Define the format now — even before you have data — so models are ready to consume it. Fields should include workload name, measured CPI, measurement source, conditions (clock speed, memory config), and uncertainty/confidence.

## 2. Separate Physics-Based Terms from Correction Terms

The current models compute CPI as a single weighted sum:

```
CPI = Σ(weight_i × cycles_i)
```

For system identification, you want a structure like:

```
CPI = f(θ_physics) + δ(θ_correction)
```

Where `f` is the grey-box model (queueing theory + instruction timing) and `δ` is the discrepancy term that absorbs model-reality mismatch. To prepare:

- **Add an explicit `corrections` dict** to each model class (initially all zeros)
- **Make `analyze()` return both the base prediction and the corrected prediction** so you can track what the physics model says vs. what the corrected model says
- **Keep correction terms structurally separate** — don't bake them into `base_cycles` values

## 3. Make Parameters Machine-Readable

Right now parameters are hardcoded in `__init__`. For system identification you'll want to:

- **Extract tunable parameters into a flat dict** (e.g., `get_parameters() → dict` and `set_parameters(dict)`)
- **Define parameter bounds** — what range is physically plausible for each parameter
- **Tag which parameters are "fixed" (known from datasheets) vs. "free" (to be identified)**

This lets an optimizer call `model.set_parameters(θ)` → `model.analyze()` → compare to measurement → update θ.

## 4. Add a Residual/Loss Function

Add a method like:

```python
def compute_residuals(self, measurements: dict) -> dict:
    """Returns per-workload residual: predicted - measured"""
```

This is the objective function the system identification algorithm will minimize. Having it built into the model class keeps everything self-contained.

## 5. Concrete Preparation Steps

| Action | Why |
|--------|-----|
| Add `get_parameters()` / `set_parameters()` to `BaseProcessorModel` | Lets optimizers manipulate model parameters programmatically |
| Add `corrections: dict` field initialized to zeros | Separates discrepancy terms from physics |
| Define a `measurements/` JSON schema | Standardizes observed data before you collect it |
| Add parameter bounds metadata | Constrains identification to physically meaningful values |
| Log both raw and corrected CPI in `analyze()` results | Lets you track how much correction is doing vs. the base model |

## 6. Choice of Identification Method

The model structure (weighted sum + queueing) is differentiable and relatively low-dimensional per processor, so there are good options:

- **Least squares** (scipy.optimize.least_squares) — simplest, works well for small parameter sets
- **Bayesian calibration** (e.g., PyMC, emcee) — gives uncertainty estimates on parameters
- **Gaussian process discrepancy** (Kennedy & O'Hagan framework) — the gold standard for grey-box model calibration with systematic discrepancy terms

The Kennedy & O'Hagan approach is particularly well-suited here since the goal is to explicitly model the discrepancy between the grey-box physics model and reality.

## 7. Getting Timing Data from Real Systems

### Physical Hardware

For real chips, the classic technique is a **calibration loop** — run a known number of instructions and measure wall-clock time externally, or use an on-chip timer if one exists. The challenge varies by era:

- **1970s chips (6502, Z80, 8080)**: No on-chip timers. Toggle a GPIO pin before/after a test loop and measure with an oscilloscope or logic analyzer. Many hobbyists still have this hardware.
- **1980s chips (68000, 8086, etc.)**: Some systems have programmable interval timers (e.g., Intel 8253/8254 on PC-compatible systems). Read timer counts before/after.
- **Late 1980s–90s (ARM, 486, etc.)**: Often have cycle counters or performance counters built in.

### Emulators (More Practical for 196 Processors)

Cycle-accurate emulators are likely the best bet for broad coverage:

- **MAME** — covers many arcade/custom chips (Namco, Fujitsu MB884x) and has cycle-accurate cores for Z80, 6502, 68000, etc.
- **perfect6502**, **Visual6502** — transistor-level simulation for MOS 6502
- **UAE** (68000), **dosbox** (x86), **StarScream** (68000)
- Many of these expose cycle counts programmatically or can be instrumented

### Test Program Structure

For each processor, write a small test program that:

1. Runs a tight loop of N identical instructions (to measure that category)
2. Reports the total cycle count (via timer, pin toggle, or emulator hook)
3. Repeats for each instruction category in the model

Example — 6502 ALU timing test (256 iterations of ADC):

```asm
; 6502 ALU timing test
    LDX #$00
loop:
    ADC #$01      ; instruction under test
    ADC #$01
    ADC #$01
    ADC #$01      ; unrolled to reduce loop overhead
    INX
    BNE loop
; total = 256 × (4 × ADC_cycles + INX_cycles + BNE_cycles)
```

Subtract the known loop overhead to isolate the instruction timing.

### Recommended Pipeline Architecture

**Layer 1: Test Program Templates (per-architecture)**
Assembly test programs for each ISA family. Architecture-specific by necessity — a Z80 test looks nothing like an ARM test. Roughly 8–10 ISA family templates needed to cover all 19 directories.

**Layer 2: Measurement Harness (Python)**
A Python driver that:
- Launches an emulator (or connects to hardware)
- Feeds it the test program
- Captures the cycle count output
- Writes results into the `measurements/` JSON format

**Layer 3: Feedback Loop (Python)**
Takes measurement JSON + model, runs system identification to update correction terms.

### Where to Start

Pick **one well-emulated processor** (6502 or Z80 — excellent emulator support, simple ISA, large community) and build the full pipeline end-to-end:

1. Write test ASM for each instruction category
2. Run it in a cycle-accurate emulator
3. Capture results into a JSON file
4. Feed that into the model's correction terms

Once that works for one processor, generalize.

---

## 8. Benchmark-Based Calibration (Preferred Approach)

Rather than writing custom test programs for each architecture, a more practical approach is to calibrate models against **known benchmark results**. Many published results already exist for these processors, and benchmarks are standardized and reproducible.

### Advantages Over Custom Test Code

- **Published results already exist** — for many of the 196 processors, someone has already run Dhrystone, Whetstone, or similar benchmarks. Measurement data can be bootstrapped without touching hardware.
- **Reproducibility** — benchmarks have standardized source code and run conditions. A user who wants to verify on their own hardware downloads the same benchmark everyone else uses.
- **Lower barrier** — "run Dhrystone on your system and paste the result" is far simpler than "assemble this custom test ROM, flash it, hook up a logic analyzer."
- **Cross-validation** — if the model predicts Dhrystone MIPS and the published number is known, that's an immediate sanity check.

### Relevant Benchmarks by Era

| Era | Relevant Benchmarks |
|-----|-------------------|
| 1970s–early 80s | Gibson mix, instruction mix studies, published cycle counts from datasheets |
| Mid 1980s | Dhrystone (1984), Whetstone (1972 but widely used in 80s), Livermore Loops |
| Late 1980s–90s | SPEC CPU89/92/95, Dhrystone 2.1, CoreMark (retroactively portable), LINPACK |

For the oldest processors, "benchmarks" are really just published instruction mixes and documented cycle counts — which maps directly to the existing category-weight model structure.

### How the Model Would Work

The model defines a **benchmark profile** — essentially a workload profile that matches the known instruction mix of a benchmark — and predicts the benchmark score. The user provides the actual score, and the system identification loop minimizes the gap.

**Workflow:**

1. Model ships with benchmark profiles (e.g., `dhrystone_2_1`, `whetstone`)
2. Model predicts: "this processor should get ~1.2 Dhrystone MIPS"
3. User provides actual result (from published data or their own run)
4. Discrepancy term adjusts to close the gap

**User-facing interface:**

```python
model = Intel8086Model()

# Model tells user what benchmarks it supports
print(model.supported_benchmarks())
# → ['dhrystone_2_1', 'whetstone', 'gibson_mix']

# Model gives instructions for running the benchmark
print(model.benchmark_instructions('dhrystone_2_1'))
# → "Download Dhrystone 2.1 from ... Compile with ... Run with N=10000 iterations.
#    Report the DMIPS value."

# User feeds back the actual result
model.submit_benchmark_result('dhrystone_2_1', dmips=0.28)

# Model updates correction terms
model.calibrate()
```

### Data Storage

Benchmark results would be stored alongside the model:

```
models/<family>/<processor>/measurements/
├── benchmarks.json           # Actual benchmark scores (user-provided or published)
└── calibration_log.json      # History of calibration runs and parameter changes
```

Example `benchmarks.json`:

```json
{
  "processor": "Intel 8086",
  "benchmarks": [
    {
      "name": "dhrystone_2_1",
      "score": 0.28,
      "unit": "DMIPS",
      "source": "published",
      "reference": "https://example.com/8086-benchmarks",
      "conditions": {
        "clock_mhz": 5.0,
        "memory": "no wait states"
      }
    }
  ]
}
```

---

## 9. Generalization to Other Subsystem Models

The grey-box + system identification framework is not limited to CPU instruction timing. It generalizes to any physical subsystem where you have:

1. A **physics-based model** (the "grey box") that gives a first-principles estimate
2. **Measurable outputs** you can compare against
3. **Tunable parameters** or correction terms

The `get_parameters()` / `set_parameters()` / `compute_residuals()` pattern works regardless of what the parameters represent — only the physics model and the benchmark change.

### Socket-to-Socket Bandwidth

For modeling bandwidth between two CPU sockets on a motherboard:

- **Grey-box model**: Bus protocol specs — clock rate, bus width, encoding overhead, arbitration latency, transfer burst sizes
- **Discrepancy term absorbs**: Chipset inefficiencies, contention from other bus masters, firmware/BIOS overhead, protocol-level stalls
- **Measurement**: Standard memory/bandwidth benchmarks (STREAM, Intel MLC, lmbench)

### Other Subsystems That Fit This Pattern

| Subsystem | Grey-Box Physics | Discrepancy Absorbs | Measurement Tools |
|-----------|-----------------|---------------------|-------------------|
| **Memory hierarchy** | Cache size, line size, associativity, DRAM timings | Prefetcher behavior, TLB effects, bank conflicts | lmbench, STREAM, Intel MLC |
| **I/O bus throughput** (ISA, PCI, AGP) | Bus clock, width, protocol overhead | Arbitration delays, bridge latency, driver overhead | hdparm, dd, custom DMA tests |
| **Coprocessor interface** (8087, 68881) | Coprocessor instruction cycles, handshake protocol | Bus contention during operand transfer, synchronization stalls | FP benchmark suites, Whetstone |
| **Multi-processor communication** (early SMP) | Shared bus bandwidth, cache coherence protocol | Snooping overhead, false sharing, OS scheduler effects | SPLASH benchmarks, custom ping-pong latency tests |
| **Disk I/O subsystems** | Seek time, rotational latency, transfer rate | Controller firmware, OS buffering, filesystem overhead | Bonnie++, fio, IOzone |
| **Network interfaces** | Line rate, MTU, protocol overhead | Driver overhead, interrupt coalescing, OS stack latency | iperf, netperf |

### What Stays the Same Across All Models

The calibration infrastructure is reusable:

```python
class BaseSubsystemModel:
    def get_parameters(self) -> dict: ...
    def set_parameters(self, params: dict): ...
    def predict(self, workload: str) -> dict: ...
    def compute_residuals(self, measurements: dict) -> dict: ...
    def calibrate(self, measurements: dict): ...
    def supported_benchmarks(self) -> list: ...
    def benchmark_instructions(self, name: str) -> str: ...
```

Only the internals of `predict()` change — the outer loop of "predict → measure → compute residual → update parameters" is identical. This means the system identification tooling, measurement JSON schema, and calibration pipeline built for CPU models can be reused directly for any new subsystem.

---

## 10. Priority

The most impactful things to do first:

1. **Add `get_parameters()`/`set_parameters()` to the base class**
2. **Define the measurement data format**

Everything else flows from having those two pieces in place.
