# LLM Audit Kit

**Offline LLM usage and cost reporting for developers.**

LLM Audit Kit turns a simple CSV of model usage into a readable Markdown cost report. It is designed for teams that want visibility into LLM spending without uploading prompts, logs, credentials, or customer data to another service.

## Why use it?

- 🔒 **Offline by design** — no network calls and no telemetry
- 📊 **Model + daily breakdowns** — requests, input tokens, output tokens, estimated cost
- 🧩 **Simple CSV input** — easy to export from your own tooling
- 💵 **Local pricing config** — update model prices without changing code
- ⚡ **Tiny dependency-free runner** — works with standard Python
- 🤖 **GitHub Action included** — run audits in CI

## CSV format

Required columns:

```csv
timestamp,model,input_tokens,output_tokens
2026-09-01T12:00:00Z,gpt-4.1-mini,1200,300
```

## GitHub Action

The repository itself is a reusable GitHub Action. Add this to a workflow:

```yaml
name: LLM Audit

on:
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bdzialo/llm-audit-kit@main
        with:
          usage_csv: usage.csv
          pricing_json: pricing.json
          report: llm-audit-report.md
      - uses: actions/upload-artifact@v4
        with:
          name: llm-audit-report
          path: llm-audit-report.md
```

The action reads the files locally on the runner. It does not send usage data to an external service.

## Local CLI

The full Python CLI is also included in the release package.

```bash
python -m llm_audit.cli usage.csv --report report.md
```

With a custom pricing file:

```bash
python -m llm_audit.cli usage.csv --pricing pricing.json --report report.md
```

## Output

The generated Markdown report includes:

- estimated total cost
- requests and token totals by model
- estimated cost by model
- requests and estimated cost by day

Unknown models are reported with an estimated cost of `$0` until you add their pricing to the local JSON configuration.

## Privacy & safety

LLM Audit Kit intentionally avoids API keys, hosted services, telemetry, and network access. Keep your source logs and generated reports under your normal repository/data access controls.

**Important:** cost estimates depend on the pricing values you provide and are not financial accounting records.

## License

MIT

## Roadmap

- More provider/model pricing examples
- Optional JSON and CSV report formats
- Better validation and friendly error messages
- Packaging as an installable Python CLI
- Community-contributed integrations
