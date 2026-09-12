from app.services.model_performance_service import get_model_performance

stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "TSLA",
]

print("\n===== MULTI-STOCK MODEL BENCHMARK =====\n")

results = []

for symbol in stocks:
    print(f"Testing {symbol}...")

    result = get_model_performance(
        symbol,
        "2y",
    )

    rf = result["model_comparison"]["random_forest"]
    gb = result["model_comparison"]["gradient_boosting"]

    results.append({
        "symbol": symbol,
        "random_forest": rf["accuracy"],
        "gradient_boosting": gb["accuracy"],
    })

print("\n===== RESULTS =====\n")

for result in results:
    print(
        f"{result['symbol']}: "
        f"RF={result['random_forest']}% | "
        f"GB={result['gradient_boosting']}%"
    )

rf_average = sum(
    r["random_forest"] for r in results
) / len(results)

gb_average = sum(
    r["gradient_boosting"] for r in results
) / len(results)

print("\n===== AVERAGE =====")
print(f"Random Forest Average: {rf_average:.2f}%")
print(f"Gradient Boosting Average: {gb_average:.2f}%")