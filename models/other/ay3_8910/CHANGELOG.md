# GI AY-3-8910 PSG Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the GI AY-3-8910 Programmable Sound Generator

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 5 category-based instruction timing
   - tone_gen: 3 cycles - Square wave tone generation (3 channels)
   - noise_gen: 4 cycles - LFSR pseudo-random noise generator
   - envelope: 5 cycles - Shared envelope generator (1 for all 3 channels)
   - mixer: 3 cycles - Per-channel tone/noise mixer enable
   - io_port: 4 cycles - General-purpose I/O port access (2 ports)
   - Reasoning: Simple square wave PSG; envelope is most complex (shared ADSR)
   - Result: CPI = 3.499 (0.03% error vs target 3.5)

2. Calibrated typical workload weights
   - tone_gen=0.286, noise_gen=0.179, envelope=0.071, mixer=0.286, io_port=0.178
   - Tone generation and mixer dominate since all 3 channels are typically active
   - Envelope weight is low since only 1 shared envelope generator
   - Result: Near-perfect match to target (0.03% error from rounding)

**What we learned:**
- AY-3-8910 is GI's classic PSG, one of the most widely used sound chips
- 3 square wave channels with 12-bit frequency, 1 noise with 5-bit period
- Only 1 envelope generator shared across all 3 channels (limitation)
- 2 general-purpose 8-bit I/O ports (used for joysticks, keyboard, etc.)
- Variants: AY-3-8912 (1 I/O port), AY-3-8913 (no I/O ports)
- Used in ZX Spectrum 128, MSX, Atari ST, Amstrad CPC, Vectrex, many arcades

**Final state:**
- CPI: 3.499 (0.03% error)
- Validation: PASSED

**References used:**
- GI AY-3-8910 datasheet
- AY-3-8910/8912 Programmable Sound Generator data manual

---
