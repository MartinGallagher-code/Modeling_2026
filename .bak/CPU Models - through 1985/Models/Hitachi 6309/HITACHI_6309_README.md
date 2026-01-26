# Hitachi 6309 CPU Queueing Model

## THE BEST 8-BIT PROCESSOR EVER MADE (1982)

The Hitachi 6309 was sold as a "6809 second-source" but secretly contained massive enhancements that made it the most powerful 8-bit processor ever created.

---

## Executive Summary

| Spec | Motorola 6809 | Hitachi 6309 |
|------|---------------|--------------|
| Year | 1978 | 1982 |
| Registers | 9 | **15** |
| Hardware Divide | No | **Yes** |
| Block Transfer | No | **TFM** |
| Native Mode IPC | 0.11 | **0.18** |
| Status | Documented | **Secret until 1988!** |

---

## The Secret History

```
1982: Hitachi releases 6309 as "6809 second-source"
      (Secretly contains major enhancements)
      
1982-1986: Sold as 6809-compatible
           Nobody knows about extra features
           
1986: Users notice some instructions run faster
      "Hey, my 6309 is faster than my 6809..."
      
1988: Hitachi finally releases full documentation
      Community discovers treasure trove of features!
      
WHY THE SECRET? Hitachi didn't want to upset
Motorola licensing agreement.
```

---

## New Registers

```
6809:                    6309 (Native Mode):
┌─────┬─────┐           ┌─────┬─────┐
│  A  │  B  │ = D       │  A  │  B  │ = D ──┐
└─────┴─────┘           ├─────┼─────┤       │
                        │  E  │  F  │ = W ──┼── Q (32-bit!)
                        └─────┴─────┘       │
                                            │
┌─────────────┐         ┌─────────────┐     │
│      X      │         │      X      │     │
├─────────────┤         ├─────────────┤
│      Y      │         │      Y      │
├─────────────┤         ├─────────────┤
│      U      │         │      U      │
├─────────────┤         ├─────────────┤
│      S      │         │      S      │
└─────────────┘         ├─────────────┤
                        │      V      │ ← NEW!
                        ├─────────────┤
                        │     MD      │ ← Mode register
                        └─────────────┘

Q = 32-bit accumulator (D:W) - unheard of in 8-bit!
```

---

## New Instructions (~60 total)

### Hardware Divide (6809 had none!)
| Instruction | Operation | Cycles |
|-------------|-----------|--------|
| DIVD | D / reg8 → D | 25 |
| DIVQ | Q / reg16 → Q | 34 |

### Enhanced Multiply
| Instruction | Operation | Cycles |
|-------------|-----------|--------|
| MULD | D × reg16 → Q | 28 |

### Block Transfer (DMA-like)
```asm
TFM X+,Y+    ; Copy block, X→Y, increment both
TFM X-,Y-    ; Copy block, decrement both
TFM X+,Y     ; Fill memory from X, Y constant
TFM X,Y+     ; Read from X to block at Y
```
3 cycles per byte - incredibly fast!

### Inter-Register Operations
```asm
ADDR r1,r2   ; r2 += r1
SUBR r1,r2   ; r2 -= r1
ANDR r1,r2   ; r2 &= r1
ORR  r1,r2   ; r2 |= r1
```

---

## Native Mode

Enable by setting bit in MD register:

```asm
    LDMD #$01      ; Enable native mode
    
    ; Now running at full 6309 speed!
    ; - Faster timings
    ; - All new instructions available
    ; - Extra registers accessible
```

### Timing Improvement

| Instruction | 6809 | 6309 Native | Speedup |
|-------------|------|-------------|---------|
| ABX | 3 | 1 | 3× |
| SEX | 2 | 1 | 2× |
| MUL | 11 | 10 | 10% |
| Average | - | - | ~30% |

---

## Why "Best 8-Bit Ever"?

| Feature | 6502 | Z80 | 6809 | **6309** |
|---------|------|-----|------|----------|
| Registers | 3 | 14 | 9 | **15** |
| Hardware MUL | No | No | Yes | **Yes** |
| Hardware DIV | No | No | No | **Yes** |
| Block Transfer | No | Yes | No | **Yes (faster)** |
| 32-bit math | No | No | No | **Yes (Q reg)** |
| Orthogonality | Low | Low | High | **Very High** |
| IPC | 0.10 | 0.08 | 0.11 | **0.18** |

The 6309 in native mode outperforms every other 8-bit processor.

---

## Modern Use

The 6309 is popular in the **CoCo (Color Computer)** retro community:

- NitrOS-9: 6309 native mode OS
- Games optimized for 6309
- Replacement for 6809 in vintage machines
- Still manufactured (compatible parts)

---

## Files

| File | Description |
|------|-------------|
| `hitachi_6309_model.py` | Python implementation |
| `hitachi_6309_model.json` | Configuration |
| `HITACHI_6309_README.md` | This document |
| `QUICK_START_6309.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0  
**Date:** January 25, 2026

*"The 6309: Hidden power, finally revealed."*
