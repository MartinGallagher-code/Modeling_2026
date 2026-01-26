# Contributing to Modeling_2026

Thank you for your interest in contributing to the Modeling_2026 CPU performance modeling project!

---

## Ways to Contribute

### 1. Add New Processor Models

We're actively seeking models for:

**High Priority:**
- Intel Pentium Pro (1995) - First out-of-order x86
- AMD Athlon (1999) - AMD's breakthrough
- ARM7TDMI (1994) - Ubiquitous ARM core
- MIPS R3000/R4000 - PlayStation, N64

**Medium Priority:**
- Pentium II/III/4
- PowerPC 603/604/G3/G4
- ARM9, ARM11, Cortex series
- Console processors (PS1, PS2, N64)

### 2. Improve Existing Models

- Accuracy improvements with better validation data
- Additional documentation
- Bug fixes

### 3. Provide Validation Data

Real hardware measurements are extremely valuable:
- Benchmark results from actual hardware
- Cycle counts from specific code sequences
- Memory bandwidth measurements

### 4. Documentation

- Improve existing documentation
- Add cross-references between related processors
- Historical context and market information

---

## Model Requirements

Each processor model must include:

### Required Files

```
ProcessorName/
├── processor_model.py      # Python implementation
├── processor_model.json    # Configuration
├── PROCESSOR_README.md     # Full documentation
├── QUICK_START.md          # Quick reference
└── PROJECT_SUMMARY.md      # Executive summary
```

### Quality Standards

1. **Accuracy**: < 5% error vs published benchmarks
2. **Documentation**: Complete technical documentation
3. **Code Quality**: Clean, commented Python code
4. **Validation**: At least one validation source cited
5. **Consistency**: Follow existing model structure

---

## Getting Started

### 1. Study Existing Models

Start by examining a model similar to what you want to create:

- **Simple 8-bit**: See `Intel 8080` or `MOS 6502`
- **16-bit with prefetch**: See `Intel 8086`
- **32-bit CISC**: See `Motorola 68020` or `Intel 80386`
- **RISC**: See `MIPS R2000` or `ARM1`
- **Superscalar**: See `Intel Pentium`

### 2. Gather Information

Required information:
- Pipeline structure (stages, depths)
- Instruction timing (cycles per instruction type)
- Cache configuration (if any)
- Clock frequency range
- Published performance numbers (MIPS, benchmarks)

Sources:
- Manufacturer datasheets
- Technical reference manuals
- Academic papers
- Retro computing community documentation

### 3. Implement the Model

Use the template in `METHODOLOGY.md`:

```python
class NewProcessorQueueModel:
    def __init__(self, config_file):
        # Load configuration
        pass
    
    def predict_ipc(self, arrival_rate):
        # Implement queueing model
        pass
    
    def calibrate(self, measured_ipc):
        # Calibration logic
        pass
```

### 4. Validate

- Compare predicted IPC to published values
- Check that error is < 5%
- Verify bottleneck identification is reasonable

### 5. Document

Write complete documentation including:
- Technical specifications
- Architectural features
- Historical context
- Validation results

---

## Code Style

### Python

- Python 3.8+ compatible
- Use type hints
- Document all public methods
- Follow PEP 8 style guide

### JSON Configuration

- Use descriptive parameter names
- Include units in comments
- Organize by category (architecture, timing, etc.)

### Markdown Documentation

- Use consistent heading structure
- Include tables for specifications
- Add diagrams where helpful (ASCII art is fine)

---

## Submitting Changes

### For Small Fixes

1. Fork the repository
2. Make your changes
3. Submit a pull request with clear description

### For New Models

1. Fork the repository
2. Create a new directory for the processor
3. Implement all required files
4. Validate against at least one benchmark
5. Submit a pull request with:
   - Description of the processor
   - Validation results
   - Data sources cited

---

## Questions?

If you're unsure about anything:

1. Check existing models for examples
2. Read `METHODOLOGY.md` for technical details
3. Open an issue to discuss before starting major work

---

## Recognition

Contributors will be acknowledged in:
- The main README
- Individual model documentation
- Any publications resulting from this work

---

Thank you for helping build a comprehensive CPU performance modeling resource!
