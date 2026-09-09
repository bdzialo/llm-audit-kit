import argparse
import json

from .audit import load_usage, summarize, markdown_report


def main():
    parser = argparse.ArgumentParser(description="Offline LLM usage/cost auditor")
    parser.add_argument("csv")
    parser.add_argument("--pricing", default="pricing.json")
    parser.add_argument("--report", default="report.md")
    args = parser.parse_args()

    with open(args.pricing, encoding="utf-8") as f:
        pricing = json.load(f)
    rows = load_usage(args.csv)
    by_model, by_day = summarize(rows, pricing)
    report = markdown_report(by_model, by_day)

    with open(args.report, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)


if __name__ == "__main__":
    main()
