import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Offline LLM usage/cost auditor")
    parser.add_argument("csv")
    parser.add_argument("--pricing", default="pricing.json")
    parser.add_argument("--report", default="llm-audit-report.md")
    args = parser.parse_args()

    with open(args.pricing, encoding="utf-8") as f:
        pricing = json.load(f)

    models = defaultdict(lambda: [0, 0, 0, 0.0])
    days = defaultdict(lambda: [0, 0.0])

    with open(args.csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            model = row["model"]
            input_tokens = int(row["input_tokens"])
            output_tokens = int(row["output_tokens"])
            price = pricing.get(model, {})
            cost = input_tokens / 1_000_000 * float(price.get("input_per_1m", 0))
            cost += output_tokens / 1_000_000 * float(price.get("output_per_1m", 0))

            model_stats = models[model]
            model_stats[0] += 1
            model_stats[1] += input_tokens
            model_stats[2] += output_tokens
            model_stats[3] += cost

            day = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).date().isoformat()
            days[day][0] += 1
            days[day][1] += cost

    total = sum(stats[3] for stats in models.values())
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
    for model, stats in sorted(models.items()):
        lines.append(
            f"| {model} | {stats[0]} | {stats[1]:,} | {stats[2]:,} | ${stats[3]:.4f} |"
        )

    lines += ["", "## By day", "", "| Day | Requests | Estimated cost |", "|---|---:|---:|"]
    for day, stats in sorted(days.items()):
        lines.append(f"| {day} | {stats[0]} | ${stats[1]:.4f} |")

    with open(args.report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {args.report}")


if __name__ == "__main__":
    main()
