"""Verify the tool-usage vs success correlation and compute its 95% CI
(Fisher z) directly from results.json, so the paper reports accurate numbers.
"""
import json
import math
from pathlib import Path

data = json.loads((Path(__file__).parent / "results.json").read_text())
print(f"Total runs: {len(data)}")

# Show available keys once
print("Keys:", sorted(data[0].keys()))

score_map = {"EXCELLENT": 2, "PASS": 1, "FAIL": 0}


def status_of(r):
    for k in ("status", "result", "grade"):
        if k in r:
            return str(r[k]).upper()
    return ""


def toolcalls_of(r):
    for k in ("tool_call_count", "tool_calls", "toolCalls", "num_tool_calls"):
        if k in r and isinstance(r[k], (int, float)):
            return float(r[k])
        if k in r and isinstance(r[k], list):
            return float(len(r[k]))
    return None


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return float("nan"), n
    return sxy / math.sqrt(sxx * syy), n


def fisher_ci(r, n, alpha=0.05):
    if abs(r) >= 1 or n <= 3:
        return (float("nan"), float("nan"))
    z = math.atanh(r)
    se = 1 / math.sqrt(n - 3)
    zc = 1.959963985  # 97.5th percentile
    lo, hi = z - zc * se, z + zc * se
    return math.tanh(lo), math.tanh(hi)


def two_sided_p(r, n):
    # t-test for Pearson r
    if abs(r) >= 1 or n <= 2:
        return float("nan")
    t = r * math.sqrt((n - 2) / (1 - r * r))
    # Normal approx is rough; use survival via incomplete beta-free approx.
    # For reporting we rely on the established p; here print t and df.
    return t


tool = []
binary = []  # success: EXCELLENT/PASS = 1, FAIL = 0
points = []  # score 0/1/2
for r in data:
    tc = toolcalls_of(r)
    st = status_of(r)
    if tc is None or st not in score_map:
        continue
    tool.append(tc)
    points.append(score_map[st])
    binary.append(1.0 if st in ("EXCELLENT", "PASS") else 0.0)

for label, ys in (("tool_calls vs SCORE(0/1/2)", points),
                  ("tool_calls vs SUCCESS(binary)", binary)):
    r, n = pearson(tool, ys)
    lo, hi = fisher_ci(r, n)
    t = two_sided_p(r, n)
    print(f"\n{label}: n={n}")
    print(f"  Pearson r = {r:.3f}")
    print(f"  95% CI (Fisher z) = [{lo:.3f}, {hi:.3f}]")
    print(f"  t({n-2}) = {t:.3f}")
