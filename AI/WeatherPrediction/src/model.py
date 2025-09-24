from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Input # type: ignore
import tensorflow as tf # type: ignore

def build_model(input_shape):
    model = Sequential([
        Input(shape=input_shape),
        LSTM(64, activation='tanh', return_sequences=True),  # return_sequences=True for stacking
        LSTM(32, activation='tanh'),
        Dense(1)
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss='mse')
    return model


def train_model(model, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size
    )
    return history
