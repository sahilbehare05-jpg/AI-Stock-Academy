import numpy as np
import yfinance as yf

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from app.ml.prediction import create_features


STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]

# ---------------------------------------------------------
# VOLATILITY FEATURES
# ---------------------------------------------------------

FEATURE_COLUMNS = [
    "Volatility_10",
    "Volatility_20",
    "High_Low_Range",
    "Open_Close_Range",
]

CONFIDENCE_LEVELS = [
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
    0.75,
    0.80,
]

INITIAL_TRAINING = 500
TEST_BLOCK = 60


# ---------------------------------------------------------
# DOWNLOAD DATA
# ---------------------------------------------------------

def prepare_data(symbol):

    data = yf.download(
        symbol,
        period="5y",
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(
            f"No data downloaded for {symbol}"
        )

    df = create_features(data)

    df = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    return df


# ---------------------------------------------------------
# WALK-FORWARD CONFIDENCE TEST
# ---------------------------------------------------------

def evaluate_stock(symbol):

    df = prepare_data(symbol)

    X = df[FEATURE_COLUMNS]
    y = df["Target"]

    all_predictions = []
    all_actuals = []
    all_probabilities = []

    start = INITIAL_TRAINING

    while start < len(df):

        test_end = min(
            start + TEST_BLOCK,
            len(df)
        )

        X_train = X.iloc[:start]
        y_train = y.iloc[:start]

        X_test = X.iloc[start:test_end]
        y_test = y.iloc[start:test_end]

        if len(X_test) == 0:
            break

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=42,
            n_jobs=-1,
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(
            X_test
        ).max(axis=1)

        all_predictions.extend(
            predictions
        )

        all_actuals.extend(
            y_test.values
        )

        all_probabilities.extend(
            probabilities
        )

        start = test_end

    all_predictions = np.array(
        all_predictions
    )

    all_actuals = np.array(
        all_actuals
    )

    all_probabilities = np.array(
        all_probabilities
    )

    results = {}

    # -----------------------------------------------------
    # TEST EACH CONFIDENCE LEVEL
    # -----------------------------------------------------

    for threshold in CONFIDENCE_LEVELS:

        mask = (
            all_probabilities >= threshold
        )

        prediction_count = int(
            mask.sum()
        )

        coverage = (
            prediction_count
            / len(all_actuals)
            * 100
        )

        if prediction_count == 0:

            results[threshold] = {
                "accuracy": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
                "coverage": 0,
                "predictions": 0,
            }

            continue

        selected_predictions = (
            all_predictions[mask]
        )

        selected_actuals = (
            all_actuals[mask]
        )

        accuracy = accuracy_score(
            selected_actuals,
            selected_predictions
        )

        precision = precision_score(
            selected_actuals,
            selected_predictions,
            zero_division=0
        )

        recall = recall_score(
            selected_actuals,
            selected_predictions,
            zero_division=0
        )

        f1 = f1_score(
            selected_actuals,
            selected_predictions,
            zero_division=0
        )

        results[threshold] = {
            "accuracy": accuracy * 100,
            "precision": precision * 100,
            "recall": recall * 100,
            "f1": f1 * 100,
            "coverage": coverage,
            "predictions": prediction_count,
        }

    return results


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

print("=" * 70)
print("VOLATILITY + CONFIDENCE EXPERIMENT")
print("=" * 70)

print()
print(
    "Stocks:",
    ", ".join(STOCKS)
)
print("Period: 5y")
print("Prediction horizon: 3 days")
print("Initial training:", INITIAL_TRAINING)
print("Test block:", TEST_BLOCK)
print("Validation: Walk-forward chronological")
print()
print("Features:")
for feature in FEATURE_COLUMNS:
    print("  -", feature)

print()
print("=" * 70)


all_results = {
    threshold: []
    for threshold in CONFIDENCE_LEVELS
}


# ---------------------------------------------------------
# TEST STOCKS
# ---------------------------------------------------------

for symbol in STOCKS:

    print()
    print(
        f"Testing {symbol}..."
    )

    try:

        results = evaluate_stock(
            symbol
        )

        for threshold, result in results.items():

            all_results[threshold].append(
                result
            )

            print(
                f"  {int(threshold * 100)}% confidence → "
                f"Accuracy={result['accuracy']:.2f}% | "
                f"Precision={result['precision']:.2f}% | "
                f"Recall={result['recall']:.2f}% | "
                f"F1={result['f1']:.2f}% | "
                f"Coverage={result['coverage']:.2f}% | "
                f"N={result['predictions']}"
            )

    except Exception as e:

        print(
            f"  ERROR: {e}"
        )


# ---------------------------------------------------------
# AVERAGES
# ---------------------------------------------------------

print()
print("=" * 70)
print("AVERAGE PERFORMANCE BY CONFIDENCE")
print("=" * 70)


averages = {}

for threshold, results in all_results.items():

    if not results:
        continue

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

    # Overall coverage based on total
    # predictions / total observations
    total_predictions = sum(
        r["predictions"]
        for r in results
    )

    # Every stock has approximately the same
    # number of walk-forward predictions.
    total_observations = sum(
        int(
            r["predictions"]
            / (r["coverage"] / 100)
        )
        for r in results
        if r["coverage"] > 0
    )

    overall_coverage = (
        total_predictions
        / total_observations
        * 100
        if total_observations > 0
        else 0
    )

    averages[threshold] = {
        "accuracy": avg_accuracy,
        "precision": avg_precision,
        "recall": avg_recall,
        "f1": avg_f1,
        "coverage": overall_coverage,
        "predictions": total_predictions,
    }

    print()
    print(
        f"{int(threshold * 100)}% confidence:"
    )

    print(
        f"  Average Accuracy: "
        f"{avg_accuracy:.2f}%"
    )

    print(
        f"  Average Precision: "
        f"{avg_precision:.2f}%"
    )

    print(
        f"  Average Recall: "
        f"{avg_recall:.2f}%"
    )

    print(
        f"  Average F1: "
        f"{avg_f1:.2f}%"
    )

    print(
        f"  Overall Coverage: "
        f"{overall_coverage:.2f}%"
    )

    print(
        f"  Predictions Made: "
        f"{total_predictions}"
    )


# ---------------------------------------------------------
# BEST WITH MINIMUM COVERAGE
# ---------------------------------------------------------

eligible = {
    threshold: result
    for threshold, result in averages.items()
    if result["coverage"] >= 10
}


if eligible:

    best = max(
        eligible.items(),
        key=lambda x: x[1]["f1"]
    )

    print()
    print("=" * 70)
    print("BEST RESULT WITH >=10% COVERAGE")
    print("=" * 70)

    print(
        f"Confidence: "
        f"{int(best[0] * 100)}%"
    )

    print(
        f"Average Accuracy: "
        f"{best[1]['accuracy']:.2f}%"
    )

    print(
        f"Average Precision: "
        f"{best[1]['precision']:.2f}%"
    )

    print(
        f"Average Recall: "
        f"{best[1]['recall']:.2f}%"
    )

    print(
        f"Average F1: "
        f"{best[1]['f1']:.2f}%"
    )

    print(
        f"Coverage: "
        f"{best[1]['coverage']:.2f}%"
    )


print()
print("=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)