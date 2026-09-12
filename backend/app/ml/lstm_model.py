import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


FEATURE_COLUMNS = [
    "Return_1D",
    "Return_3D",
    "Return_5D",
    "Return_10D",
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


def create_sequences(
    data,
    targets,
    sequence_length=30,
):
    X = []
    y = []

    for i in range(
        sequence_length,
        len(data),
    ):
        X.append(
            data[
                i - sequence_length:i
            ]
        )

        y.append(
            targets[i]
        )

    return np.array(X), np.array(y)


def build_lstm_model(
    sequence_length,
    feature_count,
):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(
            shape=(
                sequence_length,
                feature_count,
            )
        ),

        tf.keras.layers.LSTM(
            64,
            return_sequences=True,
        ),

        tf.keras.layers.Dropout(
            0.2
        ),

        tf.keras.layers.LSTM(
            32
        ),

        tf.keras.layers.Dropout(
            0.2
        ),

        tf.keras.layers.Dense(
            16,
            activation="relu",
        ),

        tf.keras.layers.Dense(
            1,
            activation="sigmoid",
        ),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    return model


def evaluate_lstm(
    df: pd.DataFrame,
    sequence_length=30,
):
    data = df.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    if len(data) < 150:
        raise ValueError(
            "Not enough historical data "
            "for LSTM evaluation."
        )

    # ---------------------------------------------------------
    # CHRONOLOGICAL SPLIT
    # ---------------------------------------------------------

    split_index = int(
        len(data) * 0.80
    )

    train_data = data.iloc[
        :split_index
    ].copy()

    test_data = data.iloc[
        split_index:
    ].copy()

    # ---------------------------------------------------------
    # SCALE USING TRAINING DATA ONLY
    # ---------------------------------------------------------

    scaler = StandardScaler()

    X_train_raw = train_data[
        FEATURE_COLUMNS
    ].values

    X_test_raw = test_data[
        FEATURE_COLUMNS
    ].values

    scaler.fit(
        X_train_raw
    )

    X_train_scaled = scaler.transform(
        X_train_raw
    )

    X_test_scaled = scaler.transform(
        X_test_raw
    )

    y_train = train_data[
        "Target"
    ].values.astype("float32")

    y_test = test_data[
        "Target"
    ].values.astype("float32")

    # ---------------------------------------------------------
    # CREATE SEQUENCES
    # ---------------------------------------------------------

    X_train, y_train_seq = create_sequences(
        X_train_scaled,
        y_train,
        sequence_length,
    )

    # Include the previous training observations
    # needed to construct the first test sequence.
    combined_test = np.vstack([
        X_train_scaled[
            -sequence_length:
        ],
        X_test_scaled,
    ])

    combined_targets = np.concatenate([
        y_train[
            -sequence_length:
        ],
        y_test,
    ])

    X_test, y_test_seq = create_sequences(
        combined_test,
        combined_targets,
        sequence_length,
    )

    # ---------------------------------------------------------
    # MODEL
    # ---------------------------------------------------------

    model = build_lstm_model(
        sequence_length,
        len(FEATURE_COLUMNS),
    )

    # ---------------------------------------------------------
    # TRAIN
    # ---------------------------------------------------------

    early_stopping = (
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=8,
            restore_best_weights=True,
        )
    )

    model.fit(
        X_train,
        y_train_seq,
        epochs=50,
        batch_size=32,
        validation_split=0.15,
        shuffle=False,
        callbacks=[
            early_stopping
        ],
        verbose=0,
    )

    # ---------------------------------------------------------
    # PREDICT
    # ---------------------------------------------------------

    probabilities = model.predict(
        X_test,
        verbose=0,
    ).reshape(-1)

    predictions = (
        probabilities >= 0.5
    ).astype(int)

    # ---------------------------------------------------------
    # METRICS
    # ---------------------------------------------------------

    accuracy = accuracy_score(
        y_test_seq,
        predictions,
    )

    precision = precision_score(
        y_test_seq,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test_seq,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test_seq,
        predictions,
        zero_division=0,
    )

    return {
        "model": "LSTM",

        "model_type": (
            "Long Short-Term Memory"
        ),

        "sequence_length": sequence_length,

        "features": FEATURE_COLUMNS,

        "training_samples": int(
            len(X_train)
        ),

        "testing_samples": int(
            len(X_test)
        ),

        "metrics": {
            "accuracy": round(
                accuracy * 100,
                2,
            ),

            "precision": round(
                precision * 100,
                2,
            ),

            "recall": round(
                recall * 100,
                2,
            ),

            "f1_score": round(
                f1 * 100,
                2,
            ),
        },
    }