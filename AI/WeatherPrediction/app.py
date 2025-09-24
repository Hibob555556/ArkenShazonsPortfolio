import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import tensorflow as tf

st.set_page_config(page_title="Weather Forecast", layout="wide")
st.title("Weather Temperature Forecast")

# -----------------------------
# 1. Load and preprocess data
# -----------------------------
st.sidebar.header("Data Settings")
window_size = st.sidebar.slider("Sequence Window Size", min_value=1, max_value=72, value=24)
forecast_horizon = st.sidebar.slider("Forecast Horizon", min_value=1, max_value=72, value=24)
csv_file = st.sidebar.text_input("CSV File Path", value="data/weather_combined.csv")
target_col = "Temp_C"
st.sidebar.markdown("---")

@st.cache_data
def load_and_preprocess(csv_file, target_col):
    df = pd.read_csv(csv_file)
    feature_cols = ['day_sin','day_cos','time_sin','time_cos','Dew Point Temp_C','Rel Hum_%','Wind Speed_km/h','Visibility_km','Press_kPa']
    required_cols = [target_col] + feature_cols
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV!")

    # Convert to numeric and fill missing
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df[required_cols] = df[required_cols].fillna(method='ffill')

    # Features and target
    X_features = df[feature_cols].values.astype(np.float32)
    y = df[target_col].values.astype(np.float32).reshape(-1,1)

    # Scale features and target
    X_scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()
    X_scaled = X_scaler.fit_transform(X_features)
    y_scaled = y_scaler.fit_transform(y)

    # Combine for multi-step sequence
    full_scaled = np.hstack([X_scaled, y_scaled])
    return df, full_scaled, X_scaler, y_scaler

df, full_scaled, X_scaler, y_scaler = load_and_preprocess(csv_file, target_col)

# -----------------------------
# 2. Create multi-step sequences
# -----------------------------
def create_sequences_multi_step(data_scaled, window_size, forecast_horizon):
    X, y = [], []
    for i in range(len(data_scaled) - window_size - forecast_horizon + 1):
        X.append(data_scaled[i:i+window_size, :-1])
        y.append(data_scaled[i+window_size:i+window_size+forecast_horizon, -1])
    return np.array(X), np.array(y)

X, y = create_sequences_multi_step(full_scaled, window_size, forecast_horizon)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)
st.write(f"Loaded {len(X_train)+len(X_val)} sequences, train/val split: {len(X_train)}/{len(X_val)}")

# -----------------------------
# 3. Build and train LSTM model
# -----------------------------
st.subheader("Train LSTM Model")
epochs = st.sidebar.slider("Epochs", min_value=1, max_value=200, value=50)
batch_size = st.sidebar.slider("Batch Size", min_value=1, max_value=256, value=32)

# Progress bar
progress_bar = st.progress(0)
status_text = st.empty()
class StreamlitProgressCallback(tf.keras.callbacks.Callback):
    def __init__(self, total_epochs):
        super().__init__()
        self.total_epochs = total_epochs
    def on_epoch_end(self, epoch, logs=None):
        progress = (epoch+1)/self.total_epochs
        progress_bar.progress(progress)
        status_text.text(f"Training epoch {epoch+1}/{self.total_epochs}")

# Model
model = Sequential([
    Input(shape=(X_train.shape[1], X_train.shape[2])),
    LSTM(64, activation='tanh', return_sequences=True),
    LSTM(32, activation='tanh'),
    Dense(forecast_horizon)
])
model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss='mse')

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=epochs,
    batch_size=batch_size,
    verbose=0,
    callbacks=[StreamlitProgressCallback(epochs)]
)
st.success("Training complete!")

# -----------------------------
# 4. Evaluate validation set
# -----------------------------
st.subheader("Validation Evaluation")
y_pred_val_scaled = model.predict(X_val)
y_val_original = y_val * (y_scaler.data_max_[0] - y_scaler.data_min_[0]) + y_scaler.data_min_[0]
y_pred_val_original = y_pred_val_scaled * (y_scaler.data_max_[0] - y_scaler.data_min_[0]) + y_scaler.data_min_[0]

average_diff = np.mean(np.abs(y_val_original - y_pred_val_original))
st.metric("Validation Average Difference (°C)", f"{average_diff:.2f}")

fig, ax = plt.subplots(figsize=(12,6))
# Plot first forecast horizon of each validation sequence for clarity
for i in range(len(y_val_original)):
    ax.plot(np.arange(i, i+forecast_horizon), y_val_original[i], color='gray', alpha=0.3)
    ax.plot(np.arange(i, i+forecast_horizon), y_pred_val_original[i], color='blue', alpha=0.3)
ax.set_xlabel("Time Step")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Validation Predictions (Multi-Step)")
st.pyplot(fig)

# -----------------------------
# 5. Rolling forecast from last sequence
# -----------------------------
st.subheader("Rolling Forecast Only")
X_last_window = X_val[-1:].copy()
rolling_preds_scaled = model.predict(X_last_window)[0]
rolling_preds_original = rolling_preds_scaled * (y_scaler.data_max_[0] - y_scaler.data_min_[0]) + y_scaler.data_min_[0]

fig_forecast, ax_forecast = plt.subplots(figsize=(12,6))
ax_forecast.plot(np.arange(forecast_horizon), rolling_preds_original, label=f"Rolling Forecast ({forecast_horizon} steps)", color='tab:blue')
ax_forecast.set_xlabel("Forecast Step")
ax_forecast.set_ylabel("Temperature (°C)")
ax_forecast.set_title("Multi-Step Rolling Forecast")
ax_forecast.legend()
st.pyplot(fig_forecast)

# -----------------------------
# 6. Forecast stats
# -----------------------------
forecast_avg = np.mean(rolling_preds_original)
forecast_min = np.min(rolling_preds_original)
forecast_max = np.max(rolling_preds_original)
forecast_std = np.std(rolling_preds_original)
last_actual_temp = y_val_original[-1, -1]
avg_diff_from_last = np.mean(np.abs(rolling_preds_original - last_actual_temp))

st.subheader("Rolling Forecast Stats")
fig3, ax3 = plt.subplots(figsize=(8,4))
stats_values = [forecast_avg, forecast_min, forecast_max, forecast_std, avg_diff_from_last]
stats_labels = ["Avg", "Min", "Max", "Std Dev", "Avg Diff from Last"]
ax3.bar(stats_labels, stats_values, color=['skyblue','lightgreen','salmon','orange','violet'])
ax3.set_ylabel("Temperature (°C)")
ax3.set_title("Rolling Forecast Statistics")
st.pyplot(fig3)

st.metric("Forecast Avg Temp (°C)", f"{forecast_avg:.2f}")
st.metric("Forecast Min Temp (°C)", f"{forecast_min:.2f}")
st.metric("Forecast Max Temp (°C)", f"{forecast_max:.2f}")
st.metric("Forecast Std Dev (°C)", f"{forecast_std:.2f}")
st.metric("Avg Diff from Last Actual Temp (°C)", f"{avg_diff_from_last:.2f}")
