# Use the validated model
from current.intel_4004_validated import Intel4004Model, WORKLOADS_4004

# Create model
model = Intel4004Model()

# Analyze performance
result = model.analyze("compute")

print(f"IPS: {result.ips:,.0f}")        # ~74,074
print(f"kIPS: {result.kips:.2f}")       # ~74.07
print(f"MIPS: {result.mips:.4f}")       # ~0.0741
print(f"CPI: {result.cpi_clocks:.1f}")  # ~10.0
print(f"Validation: {result.validation_status}")  # PASS
