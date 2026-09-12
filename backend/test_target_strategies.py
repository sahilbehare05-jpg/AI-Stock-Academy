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

HORIZONS = [1, 3, 5]

THRESHOLDS = [
    0.0,
    0.005,
    0.01,
    0.02,
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

    # --------------------------------------------------------
    # Returns
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Moving averages
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Volatility
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Price ranges
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Volume
    # --------------------------------------------------------

    df["VolumeChange"] = (
        df["Volume"].pct_change(
            fill_method=None
        )
    )

    volume_avg = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    df["RelativeVolume"] = (
        df["Volume"] /
        volume_avg
    )

    # --------------------------------------------------------
    # Lagged returns
    # --------------------------------------------------------

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

    return df


# ============================================================
# CREATE TARGET
# ============================================================

def create_target(
    df,
    horizon,
    threshold,
):

    data = df.copy()

    future_return = (
        data["Close"].shift(-horizon)
        / data["Close"]
        - 1
    )

    # Remove rows where future return
    # cannot be calculated
    data["FutureReturn"] = future_return

    data = data.dropna(
        subset=FEATURE_COLUMNS +
        ["FutureReturn"]
    ).copy()

    # --------------------------------------------------------
    # Binary target
    #
    # 1 = future movement greater than
    #     positive threshold
    #
    # 0 = future movement not greater
    # --------------------------------------------------------

    data["Target"] = (
        data["FutureReturn"]
        > threshold
    ).astype(int)

    return data


# ============================================================
# EVALUATE ONE STRATEGY
# ============================================================

def evaluate(
    df,
    horizon,
    threshold,
):

    data = create_target(
        df,
        horizon,
        threshold,
    )

    if len(data) < 300:
        return None

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

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    return {
        "horizon": horizon,
        "threshold": threshold * 100,
        "accuracy": accuracy * 100,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
        "train": len(train),
        "test": len(test),
        "up": int(
            (y_test == 1).sum()
        ),
        "down": int(
            (y_test == 0).sum()
        ),
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n=============================================="
)

print(
    "TARGET STRATEGY EXPERIMENT"
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
    f"Rows downloaded: {len(history)}"
)

print(
    "Creating features..."
)

df = create_features(history)

print(
    "Features created successfully.\n"
)


results = []


for horizon in HORIZONS:

    for threshold in THRESHOLDS:

        print(
            f"Testing: "
            f"{horizon}-day horizon | "
            f"{threshold * 100:.1f}% threshold"
        )

        try:

            result = evaluate(
                df,
                horizon,
                threshold,
            )

            if result is not None:

                results.append(
                    result
                )

                print(
                    f"   Accuracy: "
                    f"{result['accuracy']:.2f}%"
                )

        except Exception as e:

            print(
                f"   ERROR: {e}"
            )


# ============================================================
# RESULTS
# ============================================================

print(
    "\n=============================================="
)

print(
    "ALL RESULTS"
)

print(
    "==============================================\n"
)


for r in results:

    print(
        f"{r['horizon']}-day | "
        f"Threshold={r['threshold']:.1f}% | "
        f"Accuracy={r['accuracy']:.2f}% | "
        f"Precision={r['precision']:.2f}% | "
        f"Recall={r['recall']:.2f}% | "
        f"F1={r['f1']:.2f}% | "
        f"UP={r['up']} | "
        f"DOWN={r['down']}"
    )


# ============================================================
# BEST RESULT
# ============================================================

if results:

    best_accuracy = max(
        results,
        key=lambda x: x["accuracy"]
    )

    best_f1 = max(
        results,
        key=lambda x: x["f1"]
    )

    print(
        "\n=============================================="
    )

    print(
        "BEST BY ACCURACY"
    )

    print(
        "=============================================="
    )

    print(
        f"Horizon: "
        f"{best_accuracy['horizon']} days"
    )

    print(
        f"Threshold: "
        f"{best_accuracy['threshold']:.1f}%"
    )

    print(
        f"Accuracy: "
        f"{best_accuracy['accuracy']:.2f}%"
    )

    print(
        f"Precision: "
        f"{best_accuracy['precision']:.2f}%"
    )

    print(
        f"Recall: "
        f"{best_accuracy['recall']:.2f}%"
    )

    print(
        f"F1: "
        f"{best_accuracy['f1']:.2f}%"
    )

    print(
        "\n=============================================="
    )

    print(
        "BEST BY F1 SCORE"
    )

    print(
        "=============================================="
    )

    print(
        f"Horizon: "
        f"{best_f1['horizon']} days"
    )

    print(
        f"Threshold: "
        f"{best_f1['threshold']:.1f}%"
    )

    print(
        f"Accuracy: "
        f"{best_f1['accuracy']:.2f}%"
    )

    print(
        f"Precision: "
        f"{best_f1['precision']:.2f}%"
    )

    print(
        f"Recall: "
        f"{best_f1['recall']:.2f}%"
    )

    print(
        f"F1: "
        f"{best_f1['f1']:.2f}%"
    )


print(
    "\nExperiment complete."
)