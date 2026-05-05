"""Inspect APEX_FLOW_DATA embedded in the Stacked Architecture HTML."""
import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open(r"C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Stacked-Architecture-Narrated.html", encoding="utf-8") as f:
    s = f.read()

start_idx = s.find("APEX_FLOW_DATA = {")
eq = s.find("=", start_idx)
json_start = s.find("{", eq)
depth = 0
i = json_start
in_str = False
esc = False
while i < len(s):
    ch = s[i]
    if esc:
        esc = False
    elif ch == "\\":
        esc = True
    elif ch == '"' and not esc:
        in_str = not in_str
    elif not in_str:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
    i += 1
raw = s[json_start:i+1]
print(f"Block length: {len(raw)}")
data = json.loads(raw)
print(f"Total scenarios in flow data: {len(data)}")
first_key = list(data.keys())[0]
print(f"First key: {first_key!r}")
first_val = data[first_key]
print(f"  · Total steps for first scenario: {len(first_val)}")
first_step_key = list(first_val.keys())[0]
first_step = first_val[first_step_key]
print(f"  · First step ({first_step_key!r}):")
for k, v in first_step.items():
    v_str = str(v)
    if len(v_str) > 120:
        v_str = v_str[:120] + "..."
    print(f"    - {k}: {v_str}")

print()
print("All step keys for first scenario:")
for sk in list(first_val.keys()):
    print(f"  - {sk}")

print()
print("All scenario keys (first 35):")
for k in list(data.keys())[:40]:
    print(f"  - {k}")
print(f"... (showing 40 of {len(data)})")
