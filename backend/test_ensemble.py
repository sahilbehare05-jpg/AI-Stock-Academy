import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
    VotingClassifier,
)

from sklearn.linear_model import LogisticRegression

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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
        (df["High"] - df["Low"])
        / close
    )

    df["Open_Close_Range"] = (
        (df["Close"] - df["Open"])
        / df["Open"]
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
        df["Volume"]
        / volume_average
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
# LOAD STOCK DATA
# ============================================================

def load_stock(symbol):

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

    if len(data) < 300:
        raise ValueError(
            f"Not enough valid data for {symbol}"
        )

    return data


# ============================================================
# BUILD MODELS
# ============================================================

def build_models():

    random_forest = RandomForestClassifier(
        n_estimators=300,
        max_depth=6,
        min_samples_leaf=4,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1,
    )

    gradient_boosting = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.03,
        max_depth=3,
        min_samples_leaf=5,
        random_state=42,
    )

    extra_trees = ExtraTreesClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=3,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1,
    )

    hist_gradient = HistGradientBoostingClassifier(
        max_iter=200,
        learning_rate=0.05,
        max_leaf_nodes=15,
        l2_regularization=1.0,
        random_state=42,
    )

    logistic = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=2000,
                    random_state=42,
                ),
            ),
        ]
    )

    ensemble = VotingClassifier(
        estimators=[
            (
                "rf",
                random_forest,
            ),
            (
                "gb",
                gradient_boosting,
            ),
            (
                "et",
                extra_trees,
            ),
            (
                "hist",
                hist_gradient,
            ),
            (
                "lr",
                logistic,
            ),
        ],
        voting="soft",
        weights=[
            1,
            2,
            1,
            1,
            1,
        ],
    )

    return {
        "Random Forest": random_forest,
        "Gradient Boosting": gradient_boosting,
        "Extra Trees": extra_trees,
        "Hist Gradient Boosting": hist_gradient,
        "Logistic Regression": logistic,
        "ENSEMBLE": ensemble,
    }


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    model,
    train,
    test,
):

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
        "accuracy": accuracy * 100,
        "precision": precision * 100,
        "recall": recall * 100,
        "f1": f1 * 100,
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n======================================================"
)

print(
    "ENSEMBLE MODEL EXPERIMENT"
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
    "Validation: 80/20 chronological"
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

        data = load_stock(
            symbol
        )

        split = int(
            len(data) * 0.80
        )

        train = data.iloc[:split]
        test = data.iloc[split:]

        print(
            f"  Training samples: "
            f"{len(train)}"
        )

        print(
            f"  Testing samples: "
            f"{len(test)}"
        )

        models = build_models()

        for name, model in models.items():

            print(
                f"  Testing {name}..."
            )

            result = evaluate_model(
                model,
                train,
                test,
            )

            all_results.append({
                "stock": symbol,
                "model": name,
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
            f"  ERROR: {e}"
        )


# ============================================================
# MODEL AVERAGES
# ============================================================

print(
    "\n======================================================"
)

print(
    "AVERAGE PERFORMANCE ACROSS ALL STOCKS"
)

print(
    "======================================================\n"
)


model_names = [
    "Random Forest",
    "Gradient Boosting",
    "Extra Trees",
    "Hist Gradient Boosting",
    "Logistic Regression",
    "ENSEMBLE",
]


average_results = []


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

    average_results.append({
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

if average_results:

    best = max(
        average_results,
        key=lambda x: x["accuracy"],
    )

    print(
        "\n======================================================"
    )

    print(
        "BEST MODEL BY AVERAGE ACCURACY"
    )

    print(
        "======================================================"
    )

    print(
        f"Model: {best['model']}"
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


# ============================================================
# ENSEMBLE VS CURRENT BEST
# ============================================================

ensemble_results = [
    r
    for r in average_results
    if r["model"] == "ENSEMBLE"
]

gb_results = [
    r
    for r in average_results
    if r["model"] == "Gradient Boosting"
]


if ensemble_results:

    ensemble = ensemble_results[0]

    print(
        "\n======================================================"
    )

    print(
        "ENSEMBLE VS GRADIENT BOOSTING"
    )

    print(
        "======================================================"
    )

    print(
        f"Ensemble Accuracy: "
        f"{ensemble['accuracy']:.2f}%"
    )

    if gb_results:

        gb = gb_results[0]

        print(
            f"Gradient Boosting Accuracy: "
            f"{gb['accuracy']:.2f}%"
        )

        difference = (
            ensemble["accuracy"]
            - gb["accuracy"]
        )

        print(
            f"Difference: "
            f"{difference:+.2f} percentage points"
        )


print(
    "\nExperiment complete."
)