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

SYMBOL = "AAPL"
PERIOD = "5y"
HORIZON = 3

CONFIDENCE_LEVELS = [
    0.50,
    0.55,
    0.60,
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
# DOWNLOAD DATA
# ============================================================

def download_data():

    history = yf.download(
        SYMBOL,
        period=PERIOD,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(
            f"No data found for {SYMBOL}"
        )

    if isinstance(
        history.columns,
        pd.MultiIndex,
    ):
        history.columns = (
            history.columns
            .get_level_values(0)
        )

    return history


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(history):

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

    avg_gain = gain.rolling(
        14
    ).mean()

    avg_loss = loss.rolling(
        14
    ).mean()

    rs = (
        avg_gain /
        avg_loss.replace(
            0,
            np.nan,
        )
    )

    df["RSI"] = (
        100 -
        (
            100 /
            (1 + rs)
        )
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

    return df


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

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

def train_model(data):

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
        len(train),
        len(test),
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

    predicted_class = np.argmax(
        probabilities,
        axis=1,
    )

    selected = (
        confidence >= threshold
    )

    selected_count = int(
        selected.sum()
    )

    total_count = len(
        y_true
    )

    coverage = (
        selected_count /
        total_count
        * 100
    )

    if selected_count == 0:

        return {
            "threshold": threshold * 100,
            "accuracy": None,
            "precision": None,
            "recall": None,
            "f1": None,
            "coverage": 0,
            "predictions": 0,
        }

    y_selected = y_true[
        selected
    ]

    prediction_selected = (
        predicted_class[selected]
    )

    accuracy = accuracy_score(
        y_selected,
        prediction_selected,
    ) * 100

    precision = precision_score(
        y_selected,
        prediction_selected,
        zero_division=0,
    ) * 100

    recall = recall_score(
        y_selected,
        prediction_selected,
        zero_division=0,
    ) * 100

    f1 = f1_score(
        y_selected,
        prediction_selected,
        zero_division=0,
    ) * 100

    return {
        "threshold": threshold * 100,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "coverage": coverage,
        "predictions": selected_count,
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n=============================================="
)

print(
    "CONFIDENCE + COVERAGE EXPERIMENT"
)

print(
    "==============================================\n"
)

print(
    f"Stock: {SYMBOL}"
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
    "Validation: 80/20 chronological\n"
)

print(
    "Downloading data..."
)

history = download_data()

print(
    f"Downloaded rows: {len(history)}"
)

print(
    "Creating features..."
)

df = create_features(
    history
)

data = prepare_data(
    df
)

print(
    f"Valid rows: {len(data)}"
)

print(
    f"Features: {len(FEATURE_COLUMNS)}"
)

print(
    "\nTraining model..."
)

(
    y_test,
    probabilities,
    train_count,
    test_count,
) = train_model(
    data
)

print(
    f"Training samples: {train_count}"
)

print(
    f"Testing samples: {test_count}"
)


# ============================================================
# ALL PREDICTIONS BASELINE
# ============================================================

all_predictions = np.argmax(
    probabilities,
    axis=1,
)

all_accuracy = accuracy_score(
    y_test,
    all_predictions,
) * 100

print(
    "\n=============================================="
)

print(
    "BASELINE — ALL PREDICTIONS"
)

print(
    "=============================================="
)

print(
    f"Accuracy: {all_accuracy:.2f}%"
)


# ============================================================
# CONFIDENCE RESULTS
# ============================================================

results = []

print(
    "\n=============================================="
)

print(
    "CONFIDENCE RESULTS"
)

print(
    "==============================================\n"
)


for threshold in CONFIDENCE_LEVELS:

    result = evaluate_confidence(
        y_test,
        probabilities,
        threshold,
    )

    results.append(
        result
    )

    if result["accuracy"] is None:

        print(
            f"{threshold * 100:.0f}% confidence: "
            "No predictions"
        )

    else:

        print(
            f"{threshold * 100:.0f}% confidence: "
            f"Accuracy={result['accuracy']:.2f}% | "
            f"Precision={result['precision']:.2f}% | "
            f"Recall={result['recall']:.2f}% | "
            f"F1={result['f1']:.2f}% | "
            f"Coverage={result['coverage']:.2f}% | "
            f"Predictions={result['predictions']}"
        )


# ============================================================
# BEST ACCURACY WITH REASONABLE COVERAGE
# ============================================================

valid_results = [
    r for r in results
    if r["accuracy"] is not None
    and r["coverage"] >= 20
]


if valid_results:

    best = max(
        valid_results,
        key=lambda x: x["accuracy"],
    )

    print(
        "\n=============================================="
    )

    print(
        "BEST RESULT WITH >=20% COVERAGE"
    )

    print(
        "=============================================="
    )

    print(
        f"Confidence threshold: "
        f"{best['threshold']:.0f}%"
    )

    print(
        f"Accuracy: "
        f"{best['accuracy']:.2f}%"
    )

    print(
        f"Precision: "
        f"{best['precision']:.2f}%"
    )

    print(
        f"Recall: "
        f"{best['recall']:.2f}%"
    )

    print(
        f"F1 Score: "
        f"{best['f1']:.2f}%"
    )

    print(
        f"Coverage: "
        f"{best['coverage']:.2f}%"
    )

    print(
        f"Predictions made: "
        f"{best['predictions']}"
    )


print(
    "\nExperiment complete."
)