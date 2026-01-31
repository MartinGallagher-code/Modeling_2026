#!/usr/bin/env python3
"""
Measurement Data Format for System Identification
===================================================

Provides standardized schemas, loading, saving, and validation for
actual CPU measurement data. This module defines the data format that
models consume during system identification / calibration.

Two measurement types are supported:

1. **measured_cpi.json** - Workload-level CPI measurements from real
   hardware, cycle-accurate emulators, or published benchmarks.

2. **instruction_traces.json** - Per-instruction or per-category
   observed cycle timings from datasheets or direct measurement.

Storage location:
    models/<family>/<processor>/measurements/
        measured_cpi.json
        instruction_traces.json
        benchmarks.json

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class MeasurementConditions:
    """Environmental conditions under which a measurement was taken."""
    clock_mhz: float
    memory_config: str = ""          # e.g. "no wait states", "1 wait state"
    cache_enabled: Optional[bool] = None
    temperature_c: Optional[float] = None
    supply_voltage_v: Optional[float] = None
    notes: str = ""


@dataclass
class CPIMeasurement:
    """A single workload-level CPI observation."""
    workload: str                     # Must match a model workload profile name
    measured_cpi: float
    source: str                       # "hardware", "emulator", "published", "datasheet"
    source_detail: str = ""           # URL, paper citation, emulator name, etc.
    conditions: Optional[Dict[str, Any]] = None
    uncertainty: Optional[float] = None   # ± absolute uncertainty on CPI
    confidence: str = "medium"        # "low", "medium", "high"
    date_measured: str = ""           # ISO-8601 date
    notes: str = ""


@dataclass
class InstructionTiming:
    """A single per-instruction timing observation."""
    mnemonic: str                     # e.g. "ADC", "LD r,r'", "NOP"
    category: str                     # Model instruction category this maps to
    measured_cycles: float
    bytes: Optional[int] = None       # Instruction length in bytes
    t_states: Optional[int] = None    # T-states (for Z80-family)
    source: str = "datasheet"         # "datasheet", "emulator", "hardware"
    source_detail: str = ""
    addressing_mode: str = ""         # e.g. "immediate", "register", "indirect"
    condition: str = ""               # e.g. "branch taken", "branch not taken"
    notes: str = ""


@dataclass
class BenchmarkResult:
    """A benchmark score observation."""
    benchmark: str                    # e.g. "dhrystone_2_1", "whetstone", "gibson_mix"
    score: float
    unit: str                         # e.g. "DMIPS", "MWIPS", "MIPS", "KIPS"
    source: str = "published"         # "published", "measured", "estimated"
    source_detail: str = ""
    conditions: Optional[Dict[str, Any]] = None
    date_measured: str = ""
    notes: str = ""


@dataclass
class MeasuredCPIFile:
    """Schema for measured_cpi.json."""
    processor: str
    manufacturer: str = ""
    year: Optional[int] = None
    schema_version: str = "1.0"
    measurements: List[Dict[str, Any]] = field(default_factory=list)

    def add_measurement(self, m: CPIMeasurement):
        self.measurements.append(asdict(m))

    def get_measurement(self, workload: str) -> Optional[Dict[str, Any]]:
        """Get the best measurement for a workload (highest confidence)."""
        matches = [m for m in self.measurements if m["workload"] == workload]
        if not matches:
            return None
        # Prefer high > medium > low confidence
        rank = {"high": 3, "medium": 2, "low": 1}
        return max(matches, key=lambda m: rank.get(m.get("confidence", "medium"), 0))


@dataclass
class InstructionTracesFile:
    """Schema for instruction_traces.json."""
    processor: str
    manufacturer: str = ""
    year: Optional[int] = None
    schema_version: str = "1.0"
    source: str = ""                  # Primary source for the timings
    timings: List[Dict[str, Any]] = field(default_factory=list)

    def add_timing(self, t: InstructionTiming):
        self.timings.append(asdict(t))

    def get_category_timings(self, category: str) -> List[Dict[str, Any]]:
        """Get all timings for a given model category."""
        return [t for t in self.timings if t["category"] == category]

    def category_average(self, category: str) -> Optional[float]:
        """Average measured cycles for a category."""
        timings = self.get_category_timings(category)
        if not timings:
            return None
        return sum(t["measured_cycles"] for t in timings) / len(timings)


@dataclass
class BenchmarksFile:
    """Schema for benchmarks.json."""
    processor: str
    manufacturer: str = ""
    year: Optional[int] = None
    schema_version: str = "1.0"
    benchmarks: List[Dict[str, Any]] = field(default_factory=list)

    def add_result(self, b: BenchmarkResult):
        self.benchmarks.append(asdict(b))

    def get_benchmark(self, name: str) -> Optional[Dict[str, Any]]:
        """Get result for a named benchmark."""
        for b in self.benchmarks:
            if b["benchmark"] == name:
                return b
        return None


# ---------------------------------------------------------------------------
# I/O functions
# ---------------------------------------------------------------------------

def _measurements_dir(model_dir: str) -> Path:
    """Return the measurements/ subdirectory for a model, creating it if needed."""
    p = Path(model_dir) / "measurements"
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_measured_cpi(model_dir: str, data: MeasuredCPIFile) -> str:
    """Save measured CPI data to JSON.  Returns the file path."""
    path = _measurements_dir(model_dir) / "measured_cpi.json"
    with open(path, "w") as f:
        json.dump(asdict(data), f, indent=2)
    return str(path)


def load_measured_cpi(model_dir: str) -> Optional[MeasuredCPIFile]:
    """Load measured CPI data from JSON.  Returns None if file missing."""
    path = Path(model_dir) / "measurements" / "measured_cpi.json"
    if not path.exists():
        return None
    with open(path) as f:
        d = json.load(f)
    return MeasuredCPIFile(
        processor=d["processor"],
        manufacturer=d.get("manufacturer", ""),
        year=d.get("year"),
        schema_version=d.get("schema_version", "1.0"),
        measurements=d.get("measurements", []),
    )


def save_instruction_traces(model_dir: str, data: InstructionTracesFile) -> str:
    """Save instruction trace data to JSON.  Returns the file path."""
    path = _measurements_dir(model_dir) / "instruction_traces.json"
    with open(path, "w") as f:
        json.dump(asdict(data), f, indent=2)
    return str(path)


def load_instruction_traces(model_dir: str) -> Optional[InstructionTracesFile]:
    """Load instruction trace data from JSON.  Returns None if file missing."""
    path = Path(model_dir) / "measurements" / "instruction_traces.json"
    if not path.exists():
        return None
    with open(path) as f:
        d = json.load(f)
    return InstructionTracesFile(
        processor=d["processor"],
        manufacturer=d.get("manufacturer", ""),
        year=d.get("year"),
        schema_version=d.get("schema_version", "1.0"),
        source=d.get("source", ""),
        timings=d.get("timings", []),
    )


def save_benchmarks(model_dir: str, data: BenchmarksFile) -> str:
    """Save benchmark results to JSON.  Returns the file path."""
    path = _measurements_dir(model_dir) / "benchmarks.json"
    with open(path, "w") as f:
        json.dump(asdict(data), f, indent=2)
    return str(path)


def load_benchmarks(model_dir: str) -> Optional[BenchmarksFile]:
    """Load benchmark results from JSON.  Returns None if file missing."""
    path = Path(model_dir) / "measurements" / "benchmarks.json"
    if not path.exists():
        return None
    with open(path) as f:
        d = json.load(f)
    return BenchmarksFile(
        processor=d["processor"],
        manufacturer=d.get("manufacturer", ""),
        year=d.get("year"),
        schema_version=d.get("schema_version", "1.0"),
        benchmarks=d.get("benchmarks", []),
    )


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_measured_cpi(data: MeasuredCPIFile) -> List[str]:
    """Validate a MeasuredCPIFile, returning a list of error strings (empty = valid)."""
    errors = []
    if not data.processor:
        errors.append("processor name is required")
    for i, m in enumerate(data.measurements):
        if "workload" not in m or not m["workload"]:
            errors.append(f"measurement[{i}]: workload name is required")
        if "measured_cpi" not in m:
            errors.append(f"measurement[{i}]: measured_cpi is required")
        elif not isinstance(m["measured_cpi"], (int, float)) or m["measured_cpi"] <= 0:
            errors.append(f"measurement[{i}]: measured_cpi must be a positive number")
        if "source" not in m or not m["source"]:
            errors.append(f"measurement[{i}]: source is required")
        elif m["source"] not in ("hardware", "emulator", "published", "datasheet", "published_benchmark", "estimated"):
            errors.append(f"measurement[{i}]: source must be one of: hardware, emulator, published, datasheet, published_benchmark, estimated")
        conf = m.get("confidence", "medium")
        if conf not in ("low", "medium", "high"):
            errors.append(f"measurement[{i}]: confidence must be low, medium, or high")
    return errors


def validate_instruction_traces(data: InstructionTracesFile) -> List[str]:
    """Validate an InstructionTracesFile, returning a list of error strings."""
    errors = []
    if not data.processor:
        errors.append("processor name is required")
    for i, t in enumerate(data.timings):
        if "mnemonic" not in t or not t["mnemonic"]:
            errors.append(f"timing[{i}]: mnemonic is required")
        if "category" not in t or not t["category"]:
            errors.append(f"timing[{i}]: category is required")
        if "measured_cycles" not in t:
            errors.append(f"timing[{i}]: measured_cycles is required")
        elif not isinstance(t["measured_cycles"], (int, float)) or t["measured_cycles"] <= 0:
            errors.append(f"timing[{i}]: measured_cycles must be a positive number")
    return errors


def validate_benchmarks(data: BenchmarksFile) -> List[str]:
    """Validate a BenchmarksFile, returning a list of error strings."""
    errors = []
    if not data.processor:
        errors.append("processor name is required")
    for i, b in enumerate(data.benchmarks):
        if "benchmark" not in b or not b["benchmark"]:
            errors.append(f"benchmark[{i}]: benchmark name is required")
        if "score" not in b:
            errors.append(f"benchmark[{i}]: score is required")
        elif not isinstance(b["score"], (int, float)):
            errors.append(f"benchmark[{i}]: score must be a number")
        if "unit" not in b or not b["unit"]:
            errors.append(f"benchmark[{i}]: unit is required")
    return errors


# ---------------------------------------------------------------------------
# Convenience: compute residuals against a model
# ---------------------------------------------------------------------------

def compute_cpi_residuals(model, measured: MeasuredCPIFile) -> Dict[str, float]:
    """
    Compare model predictions to measurements.

    Returns dict mapping workload name → (predicted_cpi - measured_cpi).
    Positive residual means model over-predicts.
    """
    residuals = {}
    for m in measured.measurements:
        workload = m["workload"]
        try:
            result = model.analyze(workload)
            residuals[workload] = result.cpi - m["measured_cpi"]
        except Exception:
            pass  # skip workloads the model doesn't support
    return residuals
