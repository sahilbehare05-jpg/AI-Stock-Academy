import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# CONFIGURATION
# ============================================================

STOCKS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "TSLA",
]

PERIOD = "5y"
HORIZON = 3

CONFIDENCE_LEVELS = [
    0.65,
    0.70,
    0.75,
    0.80,
]


FEATURE_COLUMNS = [
    "Return_1D",
    "Return_3D",
    "Return_5D",
    "Return_10D",
    "SMA20_distance",
    "SMA50_distance",
    "EMA20_distance",
    "RSI",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "Volatility10",
    "Volatility20",
    "High_Low_Range",
    "Open_Close_Range",
    "VolumeChange",
    "RelativeVolume",
    "Return_Lag_1",
    "Return_Lag_2",
    "Return_Lag_3",
    "Return_Lag_5",
]


# ============================================================
# DATA + FEATURES
# ============================================================

def prepare_data(symbol):

    history = yf.download(
        symbol,
        period=PERIOD,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(
            f"No data found for {symbol}"
        )

    if isinstance(
        history.columns,
        pd.MultiIndex,
    ):
        history.columns = (
            history.columns
            .get_level_values(0)
        )

    df = history.copy()

    close = df["Close"]

    # Returns
    df["Return_1D"] = close.pct_change(
        1,
        fill_method=None,
    )

    df["Return_3D"] = close.pct_change(
        3,
        fill_method=None,
    )

    df["Return_5D"] = close.pct_change(
        5,
        fill_method=None,
    )

    df["Return_10D"] = close.pct_change(
        10,
        fill_method=None,
    )

    # Moving averages
    sma20 = close.rolling(20).mean()
    sma50 = close.rolling(50).mean()

    ema20 = close.ewm(
        span=20,
        adjust=False,
    ).mean()

    df["SMA20_distance"] = (
        close / sma20 - 1
    )

    df["SMA50_distance"] = (
        close / sma50 - 1
    )

    df["EMA20_distance"] = (
        close / ema20 - 1
    )

    # RSI
    delta = close.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = (
        avg_gain /
        avg_loss.replace(
            0,
            np.nan,
        )
    )

    df["RSI"] = (
        100 -
        (100 / (1 + rs))
    )

    # MACD
    ema12 = close.ewm(
        span=12,
        adjust=False,
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False,
    ).mean()

    macd = ema12 - ema26

    signal = macd.ewm(
        span=9,
        adjust=False,
    ).mean()

    df["MACD"] = macd
    df["MACD_Signal"] = signal
    df["MACD_Histogram"] = (
        macd - signal
    )

    # Volatility
    df["Volatility10"] = (
        df["Return_1D"]
        .rolling(10)
        .std()
    )

    df["Volatility20"] = (
        df["Return_1D"]
        .rolling(20)
        .std()
    )

    # Price ranges
    df["High_Low_Range"] = (
        (
            df["High"] -
            df["Low"]
        ) / close
    )

    df["Open_Close_Range"] = (
        (
            df["Close"] -
            df["Open"]
        ) / df["Open"]
    )

    # Volume
    df["VolumeChange"] = (
        df["Volume"].pct_change(
            fill_method=None
        )
    )

    volume_average = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    df["RelativeVolume"] = (
        df["Volume"] /
        volume_average
    )

    # Lagged returns
    df["Return_Lag_1"] = (
        df["Return_1D"].shift(1)
    )

    df["Return_Lag_2"] = (
        df["Return_1D"].shift(2)
    )

    df["Return_Lag_3"] = (
        df["Return_1D"].shift(3)
    )

    df["Return_Lag_5"] = (
        df["Return_1D"].shift(5)
    )

    # 3-day target
    future_return = (
        close.shift(-HORIZON)
        / close
        - 1
    )

    df["Target"] = (
        future_return > 0
    ).astype(int)

    data = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    if len(data) < 300:
        raise ValueError(
            "Not enough valid observations."
        )

    return data


# ============================================================
# TRAIN MODEL
# ============================================================

def train_and_predict(data):

    split = int(
        len(data) * 0.80
    )

    train = data.iloc[:split]
    test = data.iloc[split:]

    X_train = train[
        FEATURE_COLUMNS
    ]

    y_train = train[
        "Target"
    ]

    X_test = test[
        FEATURE_COLUMNS
    ]

    y_test = test[
        "Target"
    ]

    model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.03,
        max_depth=3,
        min_samples_leaf=5,
        random_state=42,
    )

    model.fit(
        X_train,
        y_train,
    )

    probabilities = model.predict_proba(
        X_test
    )

    return (
        y_test.to_numpy(),
        probabilities,
    )


# ============================================================
# CONFIDENCE EVALUATION
# ============================================================

def evaluate_confidence(
    y_true,
    probabilities,
    threshold,
):

    confidence = np.max(
        probabilities,
        axis=1,
    )

    predictions = np.argmax(
        probabilities,
        axis=1,
    )

    selected = (
        confidence >= threshold
    )

    count = int(
        selected.sum()
    )

    total = len(
        y_true
    )

    coverage = (
        count / total * 100
    )

    if count == 0:
        return None

    actual = y_true[
        selected
    ]

    predicted = predictions[
        selected
    ]

    return {
        "accuracy": accuracy_score(
            actual,
            predicted,
        ) * 100,

        "precision": precision_score(
            actual,
            predicted,
            zero_division=0,
        ) * 100,

        "recall": recall_score(
            actual,
            predicted,
            zero_division=0,
        ) * 100,

        "f1": f1_score(
            actual,
            predicted,
            zero_division=0,
        ) * 100,

        "coverage": coverage,

        "predictions": count,

        "total": total,
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n================================================"
)

print(
    "MULTI-STOCK CONFIDENCE VALIDATION"
)

print(
    "================================================\n"
)

print(
    f"Stocks: {', '.join(STOCKS)}"
)

print(
    f"Period: {PERIOD}"
)

print(
    f"Prediction horizon: {HORIZON} days"
)

print(
    "Model: Gradient Boosting"
)

print(
    "Validation: 80/20 chronological"
)

print(
    "\n================================================\n"
)


all_results = []


for symbol in STOCKS:

    print(
        f"Testing {symbol}..."
    )

    try:

        data = prepare_data(
            symbol
        )

        y_test, probabilities = (
            train_and_predict(data)
        )

        for threshold in CONFIDENCE_LEVELS:

            result = evaluate_confidence(
                y_test,
                probabilities,
                threshold,
            )

            if result is not None:

                all_results.append({
                    "symbol": symbol,
                    "threshold": threshold,
                    **result,
                })

                print(
                    f"  {threshold * 100:.0f}% "
                    f"confidence → "
                    f"Accuracy="
                    f"{result['accuracy']:.2f}% | "
                    f"Precision="
                    f"{result['precision']:.2f}% | "
                    f"Recall="
                    f"{result['recall']:.2f}% | "
                    f"F1="
                    f"{result['f1']:.2f}% | "
                    f"Coverage="
                    f"{result['coverage']:.2f}% | "
                    f"N="
                    f"{result['predictions']}"
                )

    except Exception as e:

        print(
            f"  ERROR: {e}"
        )


# ============================================================
# AVERAGES
# ============================================================

print(
    "\n================================================"
)

print(
    "AVERAGE PERFORMANCE BY CONFIDENCE"
)

print(
    "================================================\n"
)


for threshold in CONFIDENCE_LEVELS:

    results = [
        r
        for r in all_results
        if r["threshold"] == threshold
    ]

    if not results:
        continue

    avg_accuracy = np.mean([
        r["accuracy"]
        for r in results
    ])

    avg_precision = np.mean([
        r["precision"]
        for r in results
    ])

    avg_recall = np.mean([
        r["recall"]
        for r in results
    ])

    avg_f1 = np.mean([
        r["f1"]
        for r in results
    ])

    avg_coverage = np.mean([
        r["coverage"]
        for r in results
    ])

    total_predictions = sum(
        r["predictions"]
        for r in results
    )

    total_cases = sum(
        r["total"]
        for r in results
    )

    overall_coverage = (
        total_predictions /
        total_cases *
        100
    )

    print(
        f"{threshold * 100:.0f}% confidence:"
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

    print()


# ============================================================
# BEST BALANCED RESULT
# ============================================================

valid = []

for threshold in CONFIDENCE_LEVELS:

    results = [
        r
        for r in all_results
        if r["threshold"] == threshold
    ]

    if not results:
        continue

    avg_accuracy = np.mean([
        r["accuracy"]
        for r in results
    ])

    avg_f1 = np.mean([
        r["f1"]
        for r in results
    ])

    total_predictions = sum(
        r["predictions"]
        for r in results
    )

    total_cases = sum(
        r["total"]
        for r in results
    )

    coverage = (
        total_predictions /
        total_cases *
        100
    )

    # Require at least 10% coverage.
    if coverage >= 10:

        valid.append({
            "threshold": threshold,
            "accuracy": avg_accuracy,
            "f1": avg_f1,
            "coverage": coverage,
        })


if valid:

    best = max(
        valid,
        key=lambda x: (
            x["accuracy"],
            x["f1"],
        ),
    )

    print(
        "================================================"
    )

    print(
        "BEST RESULT WITH >=10% COVERAGE"
    )

    print(
        "================================================"
    )

    print(
        f"Confidence: "
        f"{best['threshold'] * 100:.0f}%"
    )

    print(
        f"Average Accuracy: "
        f"{best['accuracy']:.2f}%"
    )

    print(
        f"Average F1: "
        f"{best['f1']:.2f}%"
    )

    print(
        f"Coverage: "
        f"{best['coverage']:.2f}%"
    )


print(
    "\nExperiment complete."
)