"""Feature Drift Radar - dependency-free CSV distribution shift detector."""
from __future__ import annotations
import argparse, csv, json, math, statistics
from collections import Counter
from pathlib import Path

def load_csv(path: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def numeric(values: list[str]) -> bool:
    try:
        [float(v) for v in values if v != ""]
        return bool([v for v in values if v != ""])
    except ValueError:
        return False

def proportions(values: list[str], categories: list[str] | None = None) -> dict[str, float]:
    count = Counter(v if v != "" else "<missing>" for v in values)
    keys = categories or sorted(count)
    total = max(len(values), 1)
    return {k: count.get(k, 0) / total for k in keys}

def js_distance(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    def kl(p, q):
        return sum(x * math.log2(x / y) for x, y in zip(p, q) if x > 0 and y > 0)
    p = [a.get(k, 0.0) for k in keys]; q = [b.get(k, 0.0) for k in keys]
    m = [(x + y) / 2 for x, y in zip(p, q)]
    return math.sqrt((kl(p, m) + kl(q, m)) / 2)

def psi(reference: list[float], current: list[float], bins: int = 10) -> float:
    ordered = sorted(reference)
    edges = sorted({ordered[min(len(ordered)-1, int(len(ordered) * i / bins))] for i in range(1, bins)})
    def bucket(value):
        return sum(value > edge for edge in edges)
    ref_counts = Counter(bucket(v) for v in reference)
    cur_counts = Counter(bucket(v) for v in current)
    score = 0.0
    for i in range(len(edges) + 1):
        p = max(ref_counts[i] / len(reference), 1e-6)
        q = max(cur_counts[i] / max(len(current), 1), 1e-6)
        score += (q - p) * math.log(q / p)
    return score

def status(score: float, kind: str) -> str:
    threshold = 0.25 if kind == "numeric" else 0.15
    if score >= threshold: return "drift"
    if score >= threshold * 0.5: return "watch"
    return "stable"

def analyse(reference: list[dict[str, str]], current: list[dict[str, str]], bins: int = 10) -> list[dict]:
    shared = set(reference[0]) & set(current[0])
    report = []
    for column in sorted(shared):
        ref = [row.get(column, "") for row in reference]
        cur = [row.get(column, "") for row in current]
        if numeric(ref) and numeric(cur):
            score, kind = psi([float(x) for x in ref if x != ""], [float(x) for x in cur if x != ""], bins), "numeric"
        else:
            categories = sorted(set(ref) | set(cur) | {"<missing>"})
            score, kind = js_distance(proportions(ref, categories), proportions(cur, categories)), "categorical"
        report.append({"feature": column, "type": kind, "score": round(score, 4), "status": status(score, kind)})
    return report

def main():
    parser = argparse.ArgumentParser(description="Compare reference and current CSV distributions.")
    parser.add_argument("reference"); parser.add_argument("current")
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--report", help="Optional JSON output path")
    args = parser.parse_args()
    report = analyse(load_csv(args.reference), load_csv(args.current), args.bins)
    print(f"{'Feature':22} {'Type':12} {'Score':>8}  Status")
    print("-" * 55)
    for item in report:
        print(f"{item['feature'][:22]:22} {item['type']:12} {item['score']:8.4f}  {item['status']}")
    alerts = sum(x["status"] == "drift" for x in report)
    print(f"\n{len(report)} features analysed · {alerts} drift alert{'s' if alerts != 1 else ''}")
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"Report saved to {args.report}")

if __name__ == "__main__":
    main()
