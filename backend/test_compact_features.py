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
# FEATURE GROUPS
# ---------------------------------------------------------

PRICE_RETURNS = [
    "Close",
    "Return_1D",
    "Return_3D",
    "Return_5D",
    "Return_10D",
]

VOLATILITY = [
    "Volatility_10",
    "Volatility_20",
    "High_Low_Range",
    "Open_Close_Range",
]

VOLUME = [
    "Volume",
    "Volume_Change",
    "Relative_Volume",
]

COMBINED = (
    PRICE_RETURNS
    + VOLATILITY
    + VOLUME
)


FEATURE_GROUPS = {
    "Price + Returns": PRICE_RETURNS,
    "Volatility": VOLATILITY,
    "Volume": VOLUME,
    "Price + Returns + Volatility + Volume": COMBINED,
}


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

INITIAL_TRAINING = 500
TEST_BLOCK = 60


# ---------------------------------------------------------
# DOWNLOAD + FEATURES
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

    return df


# ---------------------------------------------------------
# WALK-FORWARD EVALUATION
# ---------------------------------------------------------

def evaluate_model(df, feature_columns):

    required_columns = feature_columns + ["Target"]

    data = df.dropna(
        subset=required_columns
    ).copy()

    X = data[feature_columns]
    y = data["Target"]

    predictions = []
    actuals = []

    start = INITIAL_TRAINING

    while start < len(data):

        train_end = start

        test_end = min(
            start + TEST_BLOCK,
            len(data)
        )

        X_train = X.iloc[:train_end]
        y_train = y.iloc[:train_end]

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

        pred = model.predict(X_test)

        predictions.extend(pred)
        actuals.extend(y_test)

        start = test_end

    if len(actuals) == 0:
        raise ValueError(
            "No test predictions were generated."
        )

    accuracy = accuracy_score(
        actuals,
        predictions
    )

    precision = precision_score(
        actuals,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        actuals,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        actuals,
        predictions,
        zero_division=0
    )

    return {
        "accuracy": accuracy * 100,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
        "predictions": len(predictions),
    }


# ---------------------------------------------------------
# MAIN EXPERIMENT
# ---------------------------------------------------------

print("=" * 70)
print("COMPACT FEATURE COMBINATION EXPERIMENT")
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
print("=" * 70)


results = {
    group: []
    for group in FEATURE_GROUPS
}


# ---------------------------------------------------------
# TEST EACH STOCK
# ---------------------------------------------------------

for symbol in STOCKS:

    print()
    print("=" * 70)
    print(f"STOCK: {symbol}")
    print("=" * 70)

    print("Downloading data...")

    df = prepare_data(symbol)

    print(
        f"Rows downloaded/created: {len(df)}"
    )

    for group_name, features in FEATURE_GROUPS.items():

        print()
        print(
            f"Testing {group_name}..."
        )

        try:

            result = evaluate_model(
                df,
                features
            )

            results[group_name].append(
                result
            )

            print(
                f"  Features: {len(features)}"
            )

            print(
                f"  Accuracy={result['accuracy']:.2f}% | "
                f"Precision={result['precision']:.2f}% | "
                f"Recall={result['recall']:.2f}% | "
                f"F1={result['f1']:.2f}% | "
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
print("AVERAGE PERFORMANCE BY FEATURE GROUP")
print("=" * 70)

averages = {}

for group_name, group_results in results.items():

    if not group_results:
        continue

    avg_accuracy = np.mean(
        [r["accuracy"] for r in group_results]
    )

    avg_precision = np.mean(
        [r["precision"] for r in group_results]
    )

    avg_recall = np.mean(
        [r["recall"] for r in group_results]
    )

    avg_f1 = np.mean(
        [r["f1"] for r in group_results]
    )

    averages[group_name] = {
        "accuracy": avg_accuracy,
        "precision": avg_precision,
        "recall": avg_recall,
        "f1": avg_f1,
    }

    print()
    print(f"{group_name}:")
    print(
        f"  Accuracy  = {avg_accuracy:.2f}%"
    )
    print(
        f"  Precision = {avg_precision:.2f}%"
    )
    print(
        f"  Recall    = {avg_recall:.2f}%"
    )
    print(
        f"  F1        = {avg_f1:.2f}%"
    )


# ---------------------------------------------------------
# BEST BY ACCURACY
# ---------------------------------------------------------

if averages:

    best_accuracy = max(
        averages.items(),
        key=lambda x: x[1]["accuracy"]
    )

    print()
    print("=" * 70)
    print("BEST FEATURE GROUP BY ACCURACY")
    print("=" * 70)

    print(
        f"Feature Group: {best_accuracy[0]}"
    )

    print(
        f"Accuracy: "
        f"{best_accuracy[1]['accuracy']:.2f}%"
    )

    print(
        f"F1 Score: "
        f"{best_accuracy[1]['f1']:.2f}%"
    )


# ---------------------------------------------------------
# BEST BY F1
# ---------------------------------------------------------

if averages:

    best_f1 = max(
        averages.items(),
        key=lambda x: x[1]["f1"]
    )

    print()
    print("=" * 70)
    print("BEST FEATURE GROUP BY F1")
    print("=" * 70)

    print(
        f"Feature Group: {best_f1[0]}"
    )

    print(
        f"Accuracy: "
        f"{best_f1[1]['accuracy']:.2f}%"
    )

    print(
        f"F1 Score: "
        f"{best_f1[1]['f1']:.2f}%"
    )


print()
print("=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)