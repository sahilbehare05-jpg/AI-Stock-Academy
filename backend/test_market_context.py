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

MARKET_SYMBOL = "SPY"
TECH_SYMBOL = "XLK"


# ============================================================
# STOCK FEATURES
# ============================================================

def create_stock_features(history):

    df = history.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    close = df["Close"]

    # --------------------------------------------------------
    # STOCK RETURNS
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
        100 / (1 + rs)
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

    return df


# ============================================================
# MARKET / SECTOR FEATURES
# ============================================================

def create_context_features(history):

    df = history.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    close = df["Close"]

    features = pd.DataFrame(
        index=df.index
    )

    # --------------------------------------------------------
    # RETURNS
    # --------------------------------------------------------

    features["Context_Return_1D"] = (
        close.pct_change(
            1,
            fill_method=None,
        )
    )

    features["Context_Return_3D"] = (
        close.pct_change(
            3,
            fill_method=None,
        )
    )

    features["Context_Return_5D"] = (
        close.pct_change(
            5,
            fill_method=None,
        )
    )

    features["Context_Return_10D"] = (
        close.pct_change(
            10,
            fill_method=None,
        )
    )

    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    sma20 = close.rolling(20).mean()
    sma50 = close.rolling(50).mean()

    features["Context_SMA20_Distance"] = (
        close / sma20 - 1
    )

    features["Context_SMA50_Distance"] = (
        close / sma50 - 1
    )

    # --------------------------------------------------------
    # VOLATILITY
    # --------------------------------------------------------

    daily_return = close.pct_change(
        fill_method=None
    )

    features["Context_Volatility20"] = (
        daily_return
        .rolling(20)
        .std()
    )

    return features


# ============================================================
# DOWNLOAD CONTEXT DATA
# ============================================================

def load_context():

    print(
        "Downloading market data..."
    )

    market = yf.download(
        MARKET_SYMBOL,
        period=PERIOD,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    print(
        "Downloading sector data..."
    )

    sector = yf.download(
        TECH_SYMBOL,
        period=PERIOD,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if market.empty:
        raise ValueError(
            "Unable to download market data."
        )

    if sector.empty:
        raise ValueError(
            "Unable to download sector data."
        )

    market_features = create_context_features(
        market
    )

    sector_features = create_context_features(
        sector
    )

    market_features = market_features.add_prefix(
        "Market_"
    )

    sector_features = sector_features.add_prefix(
        "Sector_"
    )

    context = pd.concat(
        [
            market_features,
            sector_features,
        ],
        axis=1,
    )

    return context


# ============================================================
# CREATE COMPLETE DATASET
# ============================================================

def create_dataset(
    stock_history,
    context,
):

    stock = create_stock_features(
        stock_history
    )

    # --------------------------------------------------------
    # ALIGN MARKET + SECTOR WITH STOCK
    # --------------------------------------------------------

    combined = stock.join(
        context,
        how="inner",
    )

    close = combined["Close"]

    # --------------------------------------------------------
    # RELATIVE STRENGTH
    # --------------------------------------------------------

    combined["Relative_Market_1D"] = (
        combined["Return_1D"]
        - combined["Market_Context_Return_1D"]
    )

    combined["Relative_Market_3D"] = (
        combined["Return_3D"]
        - combined["Market_Context_Return_3D"]
    )

    combined["Relative_Market_5D"] = (
        combined["Return_5D"]
        - combined["Market_Context_Return_5D"]
    )

    combined["Relative_Sector_1D"] = (
        combined["Return_1D"]
        - combined["Sector_Context_Return_1D"]
    )

    combined["Relative_Sector_3D"] = (
        combined["Return_3D"]
        - combined["Sector_Context_Return_3D"]
    )

    # --------------------------------------------------------
    # MARKET / SECTOR AGREEMENT
    # --------------------------------------------------------

    combined["Market_Trend"] = (
        combined["Market_Context_SMA20_Distance"]
        > 0
    ).astype(int)

    combined["Sector_Trend"] = (
        combined["Sector_Context_SMA20_Distance"]
        > 0
    ).astype(int)

    # --------------------------------------------------------
    # FUTURE TARGET
    # --------------------------------------------------------

    future_return = (
        close.shift(-HORIZON)
        / close
        - 1
    )

    combined["Target"] = (
        future_return > 0
    ).astype(int)

    return combined


# ============================================================
# FEATURE SETS
# ============================================================

BASE_FEATURES = [
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


CONTEXT_FEATURES = [
    "Market_Context_Return_1D",
    "Market_Context_Return_3D",
    "Market_Context_Return_5D",
    "Market_Context_Return_10D",
    "Market_Context_SMA20_Distance",
    "Market_Context_SMA50_Distance",
    "Market_Context_Volatility20",

    "Sector_Context_Return_1D",
    "Sector_Context_Return_3D",
    "Sector_Context_Return_5D",
    "Sector_Context_Return_10D",
    "Sector_Context_SMA20_Distance",
    "Sector_Context_SMA50_Distance",
    "Sector_Context_Volatility20",

    "Relative_Market_1D",
    "Relative_Market_3D",
    "Relative_Market_5D",

    "Relative_Sector_1D",
    "Relative_Sector_3D",

    "Market_Trend",
    "Sector_Trend",
]


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_walk_forward(
    data,
    feature_columns,
):

    predictions = []
    actuals = []

    total = len(data)

    train_end = INITIAL_TRAIN_SIZE

    while train_end < total:

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
            feature_columns
        ]

        y_train = train[
            "Target"
        ]

        X_test = test[
            feature_columns
        ]

        y_test = test[
            "Target"
        ]

        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=6,
            min_samples_leaf=4,
            max_features="sqrt",
            random_state=42,
            n_jobs=-1,
        )

        model.fit(
            X_train,
            y_train,
        )

        pred = model.predict(
            X_test
        )

        predictions.extend(
            pred
        )

        actuals.extend(
            y_test.to_numpy()
        )

        train_end += STEP_SIZE

    predictions = np.array(
        predictions
    )

    actuals = np.array(
        actuals
    )

    return {
        "accuracy":
            accuracy_score(
                actuals,
                predictions,
            ) * 100,

        "precision":
            precision_score(
                actuals,
                predictions,
                zero_division=0,
            ) * 100,

        "recall":
            recall_score(
                actuals,
                predictions,
                zero_division=0,
            ) * 100,

        "f1":
            f1_score(
                actuals,
                predictions,
                zero_division=0,
            ) * 100,

        "predictions":
            len(actuals),
    }


# ============================================================
# MAIN
# ============================================================

print()
print("=" * 70)
print("MARKET + SECTOR CONTEXT EXPERIMENT")
print("=" * 70)
print()

print(
    f"Stocks: {', '.join(STOCKS)}"
)

print(
    f"Period: {PERIOD}"
)

print(
    f"Prediction horizon: "
    f"{HORIZON} days"
)

print(
    "Validation: Walk-forward chronological"
)

print(
    f"Market index: {MARKET_SYMBOL}"
)

print(
    f"Sector index: {TECH_SYMBOL}"
)

print()
print("=" * 70)
print()


context = load_context()

print()
print(
    f"Context features created: "
    f"{len(context.columns)}"
)

print()


all_results = []


for symbol in STOCKS:

    print("=" * 70)

    print(
        f"TESTING {symbol}"
    )

    print("=" * 70)

    try:

        history = yf.download(
            symbol,
            period=PERIOD,
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

        if history.empty:
            print(
                "No stock data."
            )

            continue

        data = create_dataset(
            history,
            context,
        )

        base_data = data.dropna(
            subset=BASE_FEATURES + ["Target"]
        ).copy()

        context_data = data.dropna(
            subset=BASE_FEATURES +
            CONTEXT_FEATURES +
            ["Target"]
        ).copy()

        print(
            f"Base valid rows: "
            f"{len(base_data)}"
        )

        print(
            f"Context valid rows: "
            f"{len(context_data)}"
        )

        # ----------------------------------------------------
        # BASELINE
        # ----------------------------------------------------

        print()
        print(
            "Testing BASE FEATURES..."
        )

        base_result = evaluate_walk_forward(
            base_data,
            BASE_FEATURES,
        )

        print(
            f"  Accuracy="
            f"{base_result['accuracy']:.2f}% | "
            f"Precision="
            f"{base_result['precision']:.2f}% | "
            f"Recall="
            f"{base_result['recall']:.2f}% | "
            f"F1="
            f"{base_result['f1']:.2f}%"
        )

        # ----------------------------------------------------
        # CONTEXT MODEL
        # ----------------------------------------------------

        print()
        print(
            "Testing BASE + MARKET + SECTOR..."
        )

        context_result = evaluate_walk_forward(
            context_data,
            BASE_FEATURES +
            CONTEXT_FEATURES,
        )

        print(
            f"  Accuracy="
            f"{context_result['accuracy']:.2f}% | "
            f"Precision="
            f"{context_result['precision']:.2f}% | "
            f"Recall="
            f"{context_result['recall']:.2f}% | "
            f"F1="
            f"{context_result['f1']:.2f}%"
        )

        improvement = (
            context_result["accuracy"]
            - base_result["accuracy"]
        )

        print()
        print(
            f"Accuracy improvement: "
            f"{improvement:+.2f} "
            f"percentage points"
        )

        all_results.append({
            "stock": symbol,
            "base": base_result,
            "context": context_result,
            "improvement": improvement,
        })

    except Exception as e:

        print(
            f"ERROR: {e}"
        )


# ============================================================
# FINAL RESULTS
# ============================================================

print()
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
print()


if all_results:

    base_accuracy = np.mean([
        r["base"]["accuracy"]
        for r in all_results
    ])

    context_accuracy = np.mean([
        r["context"]["accuracy"]
        for r in all_results
    ])

    base_precision = np.mean([
        r["base"]["precision"]
        for r in all_results
    ])

    context_precision = np.mean([
        r["context"]["precision"]
        for r in all_results
    ])

    base_recall = np.mean([
        r["base"]["recall"]
        for r in all_results
    ])

    context_recall = np.mean([
        r["context"]["recall"]
        for r in all_results
    ])

    base_f1 = np.mean([
        r["base"]["f1"]
        for r in all_results
    ])

    context_f1 = np.mean([
        r["context"]["f1"]
        for r in all_results
    ])

    print(
        "BASE FEATURES:"
    )

    print(
        f"  Accuracy: "
        f"{base_accuracy:.2f}%"
    )

    print(
        f"  Precision: "
        f"{base_precision:.2f}%"
    )

    print(
        f"  Recall: "
        f"{base_recall:.2f}%"
    )

    print(
        f"  F1: "
        f"{base_f1:.2f}%"
    )

    print()

    print(
        "BASE + MARKET + SECTOR:"
    )

    print(
        f"  Accuracy: "
        f"{context_accuracy:.2f}%"
    )

    print(
        f"  Precision: "
        f"{context_precision:.2f}%"
    )

    print(
        f"  Recall: "
        f"{context_recall:.2f}%"
    )

    print(
        f"  F1: "
        f"{context_f1:.2f}%"
    )

    print()

    print(
        "OVERALL IMPROVEMENT:"
    )

    print(
        f"  Accuracy: "
        f"{context_accuracy - base_accuracy:+.2f} "
        f"percentage points"
    )

    print(
        f"  F1: "
        f"{context_f1 - base_f1:+.2f} "
        f"percentage points"
    )

    print()

    if context_accuracy > base_accuracy:

        print(
            "RESULT: MARKET + SECTOR FEATURES "
            "IMPROVED THE MODEL."
        )

    else:

        print(
            "RESULT: MARKET + SECTOR FEATURES "
            "DID NOT IMPROVE ACCURACY."
        )


print()
print("=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)