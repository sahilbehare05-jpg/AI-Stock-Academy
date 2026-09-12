import yfinance as yf
import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from app.ml.prediction import create_features


FEATURE_COLUMNS = [
    "Close",
    "Volume",
    "Return_1D",
    "Return_3D",
    "Return_5D",
    "Return_10D",
    "SMA_10",
    "SMA_20",
    "SMA_50",
    "EMA_10",
    "EMA_20",
    "EMA_50",
    "SMA20_distance",
    "SMA50_distance",
    "EMA20_distance",
    "RSI_14",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "BB_Position",
    "Volatility_10",
    "Volatility_20",
    "High_Low_Range",
    "Open_Close_Range",
    "Volume_Change",
    "Relative_Volume",
    "Return_Lag_1",
    "Return_Lag_2",
    "Return_Lag_3",
    "Return_Lag_5",
]


def calculate_metrics(y_true, predictions):
    accuracy = accuracy_score(
        y_true,
        predictions,
    )

    precision = precision_score(
        y_true,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        predictions,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    )

    return {
        "accuracy": round(
            float(accuracy) * 100,
            2,
        ),
        "precision": round(
            float(precision) * 100,
            2,
        ),
        "recall": round(
            float(recall) * 100,
            2,
        ),
        "f1_score": round(
            float(f1) * 100,
            2,
        ),
        "confusion_matrix": {
            "true_down": int(matrix[0][0]),
            "false_up": int(matrix[0][1]),
            "false_down": int(matrix[1][0]),
            "true_up": int(matrix[1][1]),
        },
    }


def get_model_performance(
    symbol: str,
    period: str = "1y",
):
    symbol = symbol.strip().upper()

    history = yf.download(
        symbol,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if history.empty:
        raise ValueError(
            f"No stock data found for {symbol}"
        )

    if isinstance(
        history.columns,
        pd.MultiIndex,
    ):
        history.columns = (
            history.columns.get_level_values(0)
        )

    # ---------------------------------------------------------
    # FEATURE ENGINEERING
    # ---------------------------------------------------------

    df = create_features(history)

    evaluation_data = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    if len(evaluation_data) < 100:
        raise ValueError(
            "Not enough historical data to evaluate "
            "the models reliably."
        )

    # ---------------------------------------------------------
    # CHRONOLOGICAL TRAIN / TEST SPLIT
    # ---------------------------------------------------------

    split_index = int(
        len(evaluation_data) * 0.80
    )

    train_data = evaluation_data.iloc[
        :split_index
    ]

    test_data = evaluation_data.iloc[
        split_index:
    ]

    if len(test_data) < 10:
        raise ValueError(
            "Not enough test data available."
        )

    X_train = train_data[
        FEATURE_COLUMNS
    ]

    y_train = train_data["Target"]

    X_test = test_data[
        FEATURE_COLUMNS
    ]

    y_test = test_data["Target"]

    # =========================================================
    # MODEL 1 — RANDOM FOREST
    # =========================================================

    random_forest = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        max_depth=8,
        min_samples_leaf=3,
        class_weight="balanced",
        n_jobs=-1,
    )

    random_forest.fit(
        X_train,
        y_train,
    )

    rf_predictions = random_forest.predict(
        X_test
    )

    rf_metrics = calculate_metrics(
        y_test,
        rf_predictions,
    )

    # =========================================================
    # MODEL 2 — GRADIENT BOOSTING
    # =========================================================

    gradient_boosting = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=5,
        random_state=42,
    )

    gradient_boosting.fit(
        X_train,
        y_train,
    )

    gb_predictions = gradient_boosting.predict(
        X_test
    )

    gb_metrics = calculate_metrics(
        y_test,
        gb_predictions,
    )

    # =========================================================
    # SELECT BEST MODEL
    # =========================================================

    if (
        gb_metrics["accuracy"]
        >
        rf_metrics["accuracy"]
    ):
        best_model_name = "Gradient Boosting"
        best_predictions = gb_predictions
        best_metrics = gb_metrics

    else:
        best_model_name = "Random Forest"
        best_predictions = rf_predictions
        best_metrics = rf_metrics

    # =========================================================
    # FEATURE IMPORTANCE
    # =========================================================

    if best_model_name == "Random Forest":
        importances = (
            random_forest.feature_importances_
        )
    else:
        importances = (
            gradient_boosting.feature_importances_
        )

    feature_importance = []

    for feature, importance in zip(
        FEATURE_COLUMNS,
        importances,
    ):
        feature_importance.append(
            {
                "feature": feature,
                "importance": round(
                    float(importance),
                    6,
                ),
            }
        )

    feature_importance.sort(
        key=lambda x: x["importance"],
        reverse=True,
    )

    # =========================================================
    # RESULTS
    # =========================================================

    actual_up = int(
        (y_test == 1).sum()
    )

    actual_down = int(
        (y_test == 0).sum()
    )

    predicted_up = int(
        (best_predictions == 1).sum()
    )

    predicted_down = int(
        (best_predictions == 0).sum()
    )

    correct_predictions = int(
        (
            best_predictions
            == y_test.to_numpy()
        ).sum()
    )

    incorrect_predictions = int(
        (
            best_predictions
            != y_test.to_numpy()
        ).sum()
    )

    # =========================================================
    # CHART DATA
    # =========================================================

    chart_data = []

    for index, actual, predicted in zip(
        test_data.index,
        y_test,
        best_predictions,
    ):

        date_value = index

        if hasattr(
            date_value,
            "strftime",
        ):
            date_value = date_value.strftime(
                "%Y-%m-%d"
            )

        chart_data.append(
            {
                "date": str(date_value),

                "actual": (
                    "UP"
                    if int(actual) == 1
                    else "DOWN"
                ),

                "predicted": (
                    "UP"
                    if int(predicted) == 1
                    else "DOWN"
                ),

                "correct": bool(
                    int(actual)
                    == int(predicted)
                ),
            }
        )

    # =========================================================
    # FINAL RESPONSE
    # =========================================================

    return {
        "symbol": symbol,

        "model": best_model_name,

        "model_type": (
            "RandomForestClassifier"
            if best_model_name == "Random Forest"
            else "GradientBoostingClassifier"
        ),

        "training_samples": int(
            len(train_data)
        ),

        "testing_samples": int(
            len(test_data)
        ),

        "train_test_split": (
            "80/20 chronological"
        ),

        "evaluation_period": period,

        "metrics": best_metrics,

        "model_comparison": {
            "random_forest": rf_metrics,
            "gradient_boosting": gb_metrics,
        },

        "confusion_matrix": (
            best_metrics["confusion_matrix"]
        ),

        "results": {
            "actual_up": actual_up,
            "actual_down": actual_down,
            "predicted_up": predicted_up,
            "predicted_down": predicted_down,
            "correct_predictions": (
                correct_predictions
            ),
            "incorrect_predictions": (
                incorrect_predictions
            ),
        },

        "features": FEATURE_COLUMNS,

        "feature_count": len(
            FEATURE_COLUMNS
        ),

        "feature_importance": (
            feature_importance
        ),

        "chart_data": chart_data,
    }