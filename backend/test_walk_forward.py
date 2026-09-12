import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
    HistGradientBoostingClassifier,
)
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

# Minimum number of observations used for initial training
INITIAL_TRAIN_SIZE = 500

# Test block size for every walk-forward step
TEST_BLOCK_SIZE = 60

# Move forward by this many observations
STEP_SIZE = 60


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
        df.columns = (
            df.columns
            .get_level_values(0)
        )

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
    # VOLUME
    # --------------------------------------------------------

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
    # FUTURE TARGET
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

    df = create_features(
        history
    )

    data = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    return data


# ============================================================
# BUILD MODELS
# ============================================================

def build_models():

    models = {

        "Random Forest":
            RandomForestClassifier(
                n_estimators=250,
                max_depth=6,
                min_samples_leaf=4,
                max_features="sqrt",
                random_state=42,
                n_jobs=-1,
            ),

        "Gradient Boosting":
            GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.03,
                max_depth=3,
                min_samples_leaf=5,
                random_state=42,
            ),

        "Hist Gradient Boosting":
            HistGradientBoostingClassifier(
                max_iter=200,
                learning_rate=0.05,
                max_leaf_nodes=15,
                l2_regularization=1.0,
                random_state=42,
            ),
    }

    return models


# ============================================================
# WALK-FORWARD EVALUATION
# ============================================================

def walk_forward(
    data,
    model,
):

    all_actual = []
    all_predictions = []

    fold_results = []

    total = len(data)

    train_end = INITIAL_TRAIN_SIZE

    fold_number = 1

    while (
        train_end < total
    ):

        test_start = train_end

        test_end = min(
            test_start +
            TEST_BLOCK_SIZE,
            total,
        )

        if (
            test_end -
            test_start
            < 10
        ):
            break

        train = data.iloc[
            :train_end
        ]

        test = data.iloc[
            test_start:test_end
        ]

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

        model.fit(
            X_train,
            y_train,
        )

        predictions = model.predict(
            X_test
        )

        fold_accuracy = (
            accuracy_score(
                y_test,
                predictions,
            ) * 100
        )

        fold_results.append(
            {
                "fold": fold_number,
                "train": len(train),
                "test": len(test),
                "accuracy": fold_accuracy,
            }
        )

        all_actual.extend(
            y_test.to_numpy()
        )

        all_predictions.extend(
            predictions
        )

        fold_number += 1

        train_end += STEP_SIZE

    all_actual = np.array(
        all_actual
    )

    all_predictions = np.array(
        all_predictions
    )

    accuracy = (
        accuracy_score(
            all_actual,
            all_predictions,
        ) * 100
    )

    precision = (
        precision_score(
            all_actual,
            all_predictions,
            zero_division=0,
        ) * 100
    )

    recall = (
        recall_score(
            all_actual,
            all_predictions,
            zero_division=0,
        ) * 100
    )

    f1 = (
        f1_score(
            all_actual,
            all_predictions,
            zero_division=0,
        ) * 100
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "folds": fold_results,
        "predictions": len(all_actual),
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n======================================================"
)

print(
    "WALK-FORWARD VALIDATION EXPERIMENT"
)

print(
    "======================================================\n"
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
    f"Initial training size: "
    f"{INITIAL_TRAIN_SIZE}"
)

print(
    f"Test block size: "
    f"{TEST_BLOCK_SIZE}"
)

print(
    "Validation type: Walk-forward chronological"
)

print(
    "\n======================================================\n"
)


all_results = []


for symbol in STOCKS:

    print(
        f"\nTesting {symbol}..."
    )

    try:

        data = load_data(
            symbol
        )

        print(
            f"Valid observations: "
            f"{len(data)}"
        )

        models = build_models()

        for model_name, model in models.items():

            print(
                f"  {model_name}..."
            )

            result = walk_forward(
                data,
                model,
            )

            all_results.append({
                "stock": symbol,
                "model": model_name,
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
                f"{result['f1']:.2f}% | "
                f"Predictions="
                f"{result['predictions']}"
            )

    except Exception as e:

        print(
            f"  ERROR: {e}"
        )


# ============================================================
# MODEL AVERAGES
# ============================================================

print(
    "\n======================================================"
)

print(
    "WALK-FORWARD MODEL AVERAGES"
)

print(
    "======================================================\n"
)


model_names = [
    "Random Forest",
    "Gradient Boosting",
    "Hist Gradient Boosting",
]


averages = []


for model_name in model_names:

    results = [
        r
        for r in all_results
        if r["model"] == model_name
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

    averages.append({
        "model": model_name,
        "accuracy": avg_accuracy,
        "precision": avg_precision,
        "recall": avg_recall,
        "f1": avg_f1,
    })

    print(
        f"{model_name}: "
        f"Accuracy={avg_accuracy:.2f}% | "
        f"Precision={avg_precision:.2f}% | "
        f"Recall={avg_recall:.2f}% | "
        f"F1={avg_f1:.2f}%"
    )


# ============================================================
# BEST MODEL
# ============================================================

if averages:

    best_accuracy = max(
        averages,
        key=lambda x: x["accuracy"],
    )

    best_f1 = max(
        averages,
        key=lambda x: x["f1"],
    )

    print(
        "\n======================================================"
    )

    print(
        "BEST WALK-FORWARD MODEL"
    )

    print(
        "======================================================"
    )

    print(
        f"Best by accuracy: "
        f"{best_accuracy['model']}"
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
        "\nBest by F1:"
    )

    print(
        f"Model: "
        f"{best_f1['model']}"
    )

    print(
        f"F1: "
        f"{best_f1['f1']:.2f}%"
    )


# ============================================================
# FOLD STABILITY
# ============================================================

print(
    "\n======================================================"
)

print(
    "FOLD STABILITY"
)

print(
    "======================================================"
)


for result in all_results:

    fold_accuracies = [
        fold["accuracy"]
        for fold in result["folds"]
    ]

    if not fold_accuracies:
        continue

    print(
        f"\n{result['stock']} - "
        f"{result['model']}"
    )

    print(
        f"  Folds: "
        f"{len(fold_accuracies)}"
    )

    print(
        f"  Best fold: "
        f"{max(fold_accuracies):.2f}%"
    )

    print(
        f"  Worst fold: "
        f"{min(fold_accuracies):.2f}%"
    )

    print(
        f"  Mean fold accuracy: "
        f"{np.mean(fold_accuracies):.2f}%"
    )

    print(
        f"  Fold stability "
        f"(std): "
        f"{np.std(fold_accuracies):.2f}"
    )


print(
    "\n======================================================"
)

print(
    "Experiment complete."
)

print(
    "======================================================"
)