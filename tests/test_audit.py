from llm_audit.audit import estimate_cost, summarize


def test_cost():
    row = {"model": "x", "input_tokens": 1_000_000, "output_tokens": 500_000}
    pricing = {"x": {"input_per_1m": 2, "output_per_1m": 4}}
    assert estimate_cost(row, pricing) == 4.0


def test_summary():
    rows = [
        {"timestamp": "2026-09-01T00:00:00Z", "model": "x", "input_tokens": 100, "output_tokens": 50}
    ]
    pricing = {"x": {"input_per_1m": 1, "output_per_1m": 2}}
    models, days = summarize(rows, pricing)
    assert models["x"]["requests"] == 1
    assert days["2026-09-01"]["requests"] == 1
