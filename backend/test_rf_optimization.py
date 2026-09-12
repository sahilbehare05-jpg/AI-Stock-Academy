import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
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

INITIAL_TRAIN_SIZE = 500
TEST_BLOCK_SIZE = 60
STEP_SIZE = 60


# ============================================================
# FEATURES
# ============================================================

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
# FEATURE ENGINEERING
# ============================================================

def create_features(history):

    df = history.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    close = df["Close"]

    # --------------------------------------------------------
    # RETURNS
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
    # MOVING AVERAGES
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

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = (
        avg_gain /
        avg_loss.replace(0, np.nan)
    )

    df["RSI"] = (
        100 -
        (100 / (1 + rs))
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
    # VOLATILITY
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
    # PRICE RANGE
    # --------------------------------------------------------

    df["High_Low_Range"] = (
        (df["High"] - df["Low"])
        / close
    )

    df["Open_Close_Range"] = (
        (df["Close"] - df["Open"])
        / df["Open"]
    )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    df["VolumeChange"] = (
        df["Volume"]
        .pct_change(
            fill_method=None
        )
    )

    volume_average = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    df["RelativeVolume"] = (
        df["Volume"]
        / volume_average
    )

    # --------------------------------------------------------
    # LAGGED RETURNS
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

    # --------------------------------------------------------
    # TARGET
    # --------------------------------------------------------

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
# LOAD DATA
# ============================================================

def load_data(symbol):

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

    df = create_features(history)

    data = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    return data


# ============================================================
# WALK-FORWARD EVALUATION
# ============================================================

def evaluate_model(data, params):

    predictions = []
    actuals = []

    total = len(data)

    train_end = INITIAL_TRAIN_SIZE

    while train_end < total:

        test_start = train_end

        test_end = min(
            test_start + TEST_BLOCK_SIZE,
            total,
        )

        if test_end - test_start < 10:
            break

        train = data.iloc[:train_end]
        test = data.iloc[test_start:test_end]

        X_train = train[FEATURE_COLUMNS]
        y_train = train["Target"]

        X_test = test[FEATURE_COLUMNS]
        y_test = test["Target"]

        model = RandomForestClassifier(
            random_state=42,
            n_jobs=-1,
            **params,
        )

        model.fit(
            X_train,
            y_train,
        )

        pred = model.predict(X_test)

        predictions.extend(pred)
        actuals.extend(
            y_test.to_numpy()
        )

        train_end += STEP_SIZE

    predictions = np.array(predictions)
    actuals = np.array(actuals)

    return {
        "accuracy": accuracy_score(
            actuals,
            predictions,
        ) * 100,

        "precision": precision_score(
            actuals,
            predictions,
            zero_division=0,
        ) * 100,

        "recall": recall_score(
            actuals,
            predictions,
            zero_division=0,
        ) * 100,

        "f1": f1_score(
            actuals,
            predictions,
            zero_division=0,
        ) * 100,

        "predictions": len(actuals),
    }


# ============================================================
# EXPERIMENT CONFIGURATIONS
# ============================================================

CONFIGURATIONS = [

    # --------------------------------------------------------
    # BASELINE
    # --------------------------------------------------------

    {
        "name": "Baseline",
        "params": {
            "n_estimators": 250,
            "max_depth": 6,
            "min_samples_leaf": 4,
            "max_features": "sqrt",
        },
    },

    # --------------------------------------------------------
    # MORE TREES
    # --------------------------------------------------------

    {
        "name": "More Trees",
        "params": {
            "n_estimators": 500,
            "max_depth": 6,
            "min_samples_leaf": 4,
            "max_features": "sqrt",
        },
    },

    # --------------------------------------------------------
    # DEEPER TREES
    # --------------------------------------------------------

    {
        "name": "Depth 8",
        "params": {
            "n_estimators": 300,
            "max_depth": 8,
            "min_samples_leaf": 4,
            "max_features": "sqrt",
        },
    },

    {
        "name": "Depth 10",
        "params": {
            "n_estimators": 300,
            "max_depth": 10,
            "min_samples_leaf": 4,
            "max_features": "sqrt",
        },
    },

    # --------------------------------------------------------
    # MORE REGULARIZATION
    # --------------------------------------------------------

    {
        "name": "Leaf 8",
        "params": {
            "n_estimators": 300,
            "max_depth": 8,
            "min_samples_leaf": 8,
            "max_features": "sqrt",
        },
    },

    {
        "name": "Leaf 12",
        "params": {
            "n_estimators": 300,
            "max_depth": 8,
            "min_samples_leaf": 12,
            "max_features": "sqrt",
        },
    },

    # --------------------------------------------------------
    # DIFFERENT FEATURE SAMPLING
    # --------------------------------------------------------

    {
        "name": "Max Features 0.5",
        "params": {
            "n_estimators": 300,
            "max_depth": 8,
            "min_samples_leaf": 4,
            "max_features": 0.5,
        },
    },

    {
        "name": "Max Features Log2",
        "params": {
            "n_estimators": 300,
            "max_depth": 8,
            "min_samples_leaf": 4,
            "max_features": "log2",
        },
    },

    # --------------------------------------------------------
    # BALANCED CONFIGURATION
    # --------------------------------------------------------

    {
        "name": "Balanced",
        "params": {
            "n_estimators": 500,
            "max_depth": 8,
            "min_samples_leaf": 8,
            "max_features": 0.5,
        },
    },

    # --------------------------------------------------------
    # STRONG REGULARIZATION
    # --------------------------------------------------------

    {
        "name": "Regularized",
        "params": {
            "n_estimators": 500,
            "max_depth": 6,
            "min_samples_leaf": 10,
            "max_features": 0.5,
        },
    },
]


# ============================================================
# MAIN EXPERIMENT
# ============================================================

print()
print("=" * 65)
print("RANDOM FOREST OPTIMIZATION EXPERIMENT")
print("=" * 65)

print()

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
    f"Initial training: "
    f"{INITIAL_TRAIN_SIZE}"
)

print(
    f"Test block: "
    f"{TEST_BLOCK_SIZE}"
)

print(
    "Validation: Walk-forward chronological"
)

print()
print("=" * 65)
print()


all_results = []


for symbol in STOCKS:

    print(
        f"\n{'=' * 65}"
    )

    print(
        f"STOCK: {symbol}"
    )

    print(
        f"{'=' * 65}"
    )

    try:

        data = load_data(symbol)

        print(
            f"Valid observations: "
            f"{len(data)}"
        )

        for config in CONFIGURATIONS:

            print(
                f"  Testing "
                f"{config['name']}..."
            )

            result = evaluate_model(
                data,
                config["params"],
            )

            all_results.append({
                "stock": symbol,
                "configuration": config["name"],
                **result,
            })

            print(
                f"    Accuracy="
                f"{result['accuracy']:.2f}% | "
                f"Precision="
                f"{result['precision']:.2f}% | "
                f"Recall="
                f"{result['recall']:.2f}% | "
                f"F1="
                f"{result['f1']:.2f}%"
            )

    except Exception as e:

        print(
            f"ERROR: {e}"
        )


# ============================================================
# AVERAGE RESULTS
# ============================================================

print()
print("=" * 65)
print("AVERAGE PERFORMANCE BY CONFIGURATION")
print("=" * 65)
print()


configuration_averages = []


for config in CONFIGURATIONS:

    name = config["name"]

    results = [
        r
        for r in all_results
        if r["configuration"] == name
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

    configuration_averages.append({
        "configuration": name,
        "accuracy": avg_accuracy,
        "precision": avg_precision,
        "recall": avg_recall,
        "f1": avg_f1,
    })

    print(
        f"{name}:"
    )

    print(
        f"  Accuracy = "
        f"{avg_accuracy:.2f}%"
    )

    print(
        f"  Precision = "
        f"{avg_precision:.2f}%"
    )

    print(
        f"  Recall = "
        f"{avg_recall:.2f}%"
    )

    print(
        f"  F1 = "
        f"{avg_f1:.2f}%"
    )

    print()


# ============================================================
# BEST CONFIGURATION
# ============================================================

if configuration_averages:

    best_accuracy = max(
        configuration_averages,
        key=lambda x: x["accuracy"],
    )

    best_f1 = max(
        configuration_averages,
        key=lambda x: x["f1"],
    )

    print("=" * 65)
    print("BEST CONFIGURATION BY ACCURACY")
    print("=" * 65)

    print(
        f"Configuration: "
        f"{best_accuracy['configuration']}"
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
        f"F1 Score: "
        f"{best_accuracy['f1']:.2f}%"
    )

    print()

    print("=" * 65)
    print("BEST CONFIGURATION BY F1")
    print("=" * 65)

    print(
        f"Configuration: "
        f"{best_f1['configuration']}"
    )

    print(
        f"Accuracy: "
        f"{best_f1['accuracy']:.2f}%"
    )

    print(
        f"F1 Score: "
        f"{best_f1['f1']:.2f}%"
    )


# ============================================================
# IMPROVEMENT OVER BASELINE
# ============================================================

baseline = next(
    (
        x
        for x in configuration_averages
        if x["configuration"] == "Baseline"
    ),
    None,
)

if baseline:

    print()
    print("=" * 65)
    print("IMPROVEMENT OVER BASELINE")
    print("=" * 65)
    print()

    for result in configuration_averages:

        improvement = (
            result["accuracy"]
            - baseline["accuracy"]
        )

        print(
            f"{result['configuration']}: "
            f"{improvement:+.2f} percentage points"
        )


print()
print("=" * 65)
print("EXPERIMENT COMPLETE")
print("=" * 65)