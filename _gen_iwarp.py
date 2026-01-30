import os, json
BASE = os.path.dirname(os.path.abspath(__file__))
def w(p, c):
    fp = os.path.join(BASE, p)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w") as f: f.write(c)

MODEL = """#!/usr/bin/env python3
\"\"\"
Intel iWarp Grey-Box Queueing Model
Target CPI: 1.5 (VLIW dual-issue, 1985)
\"\"\"

"""
print("generator approach too complex")
