import numpy as np
import yfinance as yf

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from app.ml.prediction import create_features


STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]

FEATURE_COLUMNS = [
    "Close",
    "Volume",

    "Return_1D",
    "Return_3D",
    "Return_5D",
    "Return_10D",

    "SMA_10",
    "SMA_20",
    "SMA_50",

    "EMA_10",
    "EMA_20",
    "EMA_50",

    "SMA20_distance",
    "SMA50_distance",
    "EMA20_distance",

    "RSI_14",

    "MACD",
    "MACD_Signal",
    "MACD_Histogram",

    "BB_Position",

    "Volatility_10",
    "Volatility_20",

    "High_Low_Range",
    "Open_Close_Range",

    "Volume_Change",
    "Relative_Volume",

    "Return_Lag_1",
    "Return_Lag_2",
    "Return_Lag_3",
    "Return_Lag_5",
]


def prepare_data(symbol):

    data = yf.download(
        symbol,
        period="5y",
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No data downloaded for {symbol}")

    df = create_features(data)

    df = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    return df


def evaluate_stock(symbol):

    df = prepare_data(symbol)

    X = df[FEATURE_COLUMNS]
    y = df["Target"]

    split = int(len(df) * 0.80)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    return {
        "accuracy": accuracy * 100,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
        "training": len(X_train),
        "testing": len(X_test),
        "valid": len(df),
    }


print("=" * 70)
print("PRODUCTION RANDOM FOREST VALIDATION")
print("=" * 70)

print()
print("Stocks:", ", ".join(STOCKS))
print("Period: 5y")
print("Prediction horizon: 3 days")
print("Validation: 80/20 chronological")
print()
print(f"Features: {len(FEATURE_COLUMNS)}")
print()
print("Production model:")
print("  Random Forest")
print("  n_estimators = 100")
print("  max_depth = 6")
print("  random_state = 42")
print()
print("=" * 70)


results = []

for symbol in STOCKS:

    print(f"\nTesting {symbol}...")

    try:

        result = evaluate_stock(symbol)

        results.append(result)

        print(
            f"  Valid observations: {result['valid']}"
        )

        print(
            f"  Accuracy={result['accuracy']:.2f}% | "
            f"Precision={result['precision']:.2f}% | "
            f"Recall={result['recall']:.2f}% | "
            f"F1={result['f1']:.2f}% | "
            f"Training={result['training']} | "
            f"Testing={result['testing']}"
        )

    except Exception as e:

        print(f"  ERROR: {e}")


if results:

    avg_accuracy = np.mean(
        [r["accuracy"] for r in results]
    )

    avg_precision = np.mean(
        [r["precision"] for r in results]
    )

    avg_recall = np.mean(
        [r["recall"] for r in results]
    )

    avg_f1 = np.mean(
        [r["f1"] for r in results]
    )

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    for symbol, result in zip(
        STOCKS,
        results
    ):

        print(
            f"{symbol}: "
            f"Accuracy={result['accuracy']:.2f}% | "
            f"Precision={result['precision']:.2f}% | "
            f"Recall={result['recall']:.2f}% | "
            f"F1={result['f1']:.2f}%"
        )

    print()
    print("=" * 70)
    print("AVERAGE PERFORMANCE")
    print("=" * 70)

    print(
        f"Accuracy:  {avg_accuracy:.2f}%"
    )

    print(
        f"Precision: {avg_precision:.2f}%"
    )

    print(
        f"Recall:    {avg_recall:.2f}%"
    )

    print(
        f"F1 Score:  {avg_f1:.2f}%"
    )

    print()
    print("=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)