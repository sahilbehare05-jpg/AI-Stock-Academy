import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
)

from sklearn.linear_model import LogisticRegression

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

def download_data(symbol, period):
    history = yf.download(
        symbol,
        period=period,
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

    return history


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_experiment_features(history):

    df = history.copy()

    close = df["Close"]

    # --------------------------------------------------------
    # Returns
    # --------------------------------------------------------

    df["Return_1D"] = (
        close.pct_change(
            1,
            fill_method=None,
        )
    )

    df["Return_3D"] = (
        close.pct_change(
            3,
            fill_method=None,
        )
    )

    df["Return_5D"] = (
        close.pct_change(
            5,
            fill_method=None,
        )
    )

    df["Return_10D"] = (
        close.pct_change(
            10,
            fill_method=None,
        )
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

    macd_signal = macd.ewm(
        span=9,
        adjust=False,
    ).mean()

    df["MACD"] = macd

    df["MACD_Signal"] = (
        macd_signal
    )

    df["MACD_Histogram"] = (
        macd -
        macd_signal
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
    # Candle structure
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

    # --------------------------------------------------------
    # 3-DAY TARGET
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
# MODELS
# ============================================================

def get_models():

    return {

        "Random Forest":
            RandomForestClassifier(
                n_estimators=300,
                max_depth=8,
                min_samples_leaf=4,
                class_weight="balanced",
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

        "Extra Trees":
            ExtraTreesClassifier(
                n_estimators=300,
                max_depth=8,
                min_samples_leaf=4,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            ),

        "Hist Gradient Boosting":
            HistGradientBoostingClassifier(
                max_iter=200,
                learning_rate=0.05,
                max_leaf_nodes=15,
                l2_regularization=1.0,
                random_state=42,
            ),

        "Logistic Regression":
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42,
            ),
    }


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

    data = df.dropna(
        subset=
        FEATURE_COLUMNS +
        ["Target"]
    ).copy()

    if len(data) < 300:
        raise ValueError(
            "Not enough valid observations."
        )

    return data


# ============================================================
# TRAIN + TEST
# ============================================================

def evaluate_model(
    model,
    data,
):

    split_index = int(
        len(data) * 0.80
    )

    train = data.iloc[
        :split_index
    ]

    test = data.iloc[
        split_index:
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
        "accuracy":
            accuracy * 100,

        "precision":
            precision * 100,

        "recall":
            recall * 100,

        "f1":
            f1 * 100,

        "train":
            len(train),

        "test":
            len(test),
    }


# ============================================================
# MAIN
# ============================================================

print(
    "\n========================================"
)

print(
    "MODEL ALGORITHM EXPERIMENT"
)

print(
    "========================================\n"
)

print(
    f"Stock: {SYMBOL}"
)

print(
    f"Period: {PERIOD}"
)

print(
    f"Prediction Horizon: {HORIZON} days"
)

print(
    "Split: 80/20 chronological\n"
)

print(
    "Downloading data..."
)

history = download_data(
    SYMBOL,
    PERIOD,
)

print(
    f"Downloaded rows: {len(history)}"
)

print(
    "Creating features..."
)

df = create_experiment_features(
    history
)

data = prepare_data(df)

print(
    f"Valid rows: {len(data)}"
)

print(
    f"Features: {len(FEATURE_COLUMNS)}\n"
)

models = get_models()

results = []

print(
    "Training models...\n"
)

for name, model in models.items():

    print(
        f"Testing {name}..."
    )

    result = evaluate_model(
        model,
        data,
    )

    results.append({
        "model": name,
        **result,
    })

# ============================================================
# RESULTS
# ============================================================

print(
    "\n========================================"
)

print(
    "RESULTS"
)

print(
    "========================================\n"
)

for result in results:

    print(
        f"{result['model']}: "
        f"Accuracy={result['accuracy']:.2f}% | "
        f"Precision={result['precision']:.2f}% | "
        f"Recall={result['recall']:.2f}% | "
        f"F1={result['f1']:.2f}%"
    )

# ============================================================
# BEST MODEL
# ============================================================

best = max(
    results,
    key=lambda x: x["accuracy"],
)

print(
    "\n========================================"
)

print(
    "BEST MODEL"
)

print(
    "========================================"
)

print(
    f"Model: {best['model']}"
)

print(
    f"Accuracy: {best['accuracy']:.2f}%"
)

print(
    f"Precision: {best['precision']:.2f}%"
)

print(
    f"Recall: {best['recall']:.2f}%"
)

print(
    f"F1 Score: {best['f1']:.2f}%"
)

print(
    "\nExperiment complete."
)