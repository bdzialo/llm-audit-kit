import csv
from collections import defaultdict
from datetime import datetime


def load_usage(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["input_tokens"] = int(row["input_tokens"])
            row["output_tokens"] = int(row["output_tokens"])
            rows.append(row)
    return rows


def estimate_cost(row, pricing):
    p = pricing.get(row["model"], {})
    return (
        row["input_tokens"] / 1_000_000 * float(p.get("input_per_1m", 0))
        + row["output_tokens"] / 1_000_000 * float(p.get("output_per_1m", 0))
    )


def summarize(rows, pricing):
    by_model = defaultdict(lambda: {"requests": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0})
    by_day = defaultdict(lambda: {"requests": 0, "cost": 0.0})

    for row in rows:
        cost = estimate_cost(row, pricing)
        model = by_model[row["model"]]
        model["requests"] += 1
        model["input_tokens"] += row["input_tokens"]
        model["output_tokens"] += row["output_tokens"]
        model["cost"] += cost

        day = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).date().isoformat()
        by_day[day]["requests"] += 1
        by_day[day]["cost"] += cost

    return dict(by_model), dict(by_day)


def markdown_report(by_model, by_day):
    total = sum(v["cost"] for v in by_model.values())
    lines = [
        "# LLM Usage Audit",
        "",
        f"**Estimated total cost:** ${total:.4f}",
        "",
        "## By model",
        "",
        "| Model | Requests | Input tokens | Output tokens | Estimated cost |",
        "|---|---:|---:|---:|---:|",
    ]
    for model, v in sorted(by_model.items()):
        lines.append(
            f"| {model} | {v['requests']} | {v['input_tokens']:,} | "
            f"{v['output_tokens']:,} | ${v['cost']:.4f} |"
        )

    lines += ["", "## By day", "", "| Day | Requests | Estimated cost |", "|---|---:|---:|"]
    for day, v in sorted(by_day.items()):
        lines.append(f"| {day} | {v['requests']} | ${v['cost']:.4f} |")
    return "\n".join(lines) + "\n"
