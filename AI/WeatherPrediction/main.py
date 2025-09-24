from src.preprocess import load_and_preprocess
from src.model import build_model, train_model
from src.evaluate import evaluate_model
from src.forecast import rolling_forecast_on_plot
import numpy as np

# -----------------------------
# 1. Load and preprocess data
# -----------------------------
X_train, X_val, y_train, y_val, X_min, X_max, y_min, y_max = load_and_preprocess(
    csv_file="data/weather.csv",
    target_col="Temp_C",
    window_size=24
)

# -----------------------------
# 2. Build and train LSTM model
# -----------------------------
model = build_model(input_shape=(X_train.shape[1], X_train.shape[2]))
train_model(
    model, 
    X_train, y_train, 
    X_val, y_val, 
    epochs=50, 
    batch_size=32
)

# -----------------------------
# 3. Evaluate on validation set
# -----------------------------
evaluate_model(
    model, 
    X_val, y_val, 
    y_min=y_min, 
    y_max=y_max
)

# -----------------------------
# 4. Compute average difference
# -----------------------------
# Predict on validation set
y_pred_scaled = model.predict(X_val)
y_val_original = y_val * (y_max - y_min) + y_min
y_pred_original = y_pred_scaled * (y_max - y_min) + y_min

# Calculate average absolute difference
average_diff = np.mean(np.abs(y_val_original - y_pred_original))
print(f"Average difference: {average_diff:.2f} °C")

# -----------------------------
# 5. Rolling forecast
# -----------------------------
# Use the last sequence from validation set as starting point
X_last_window = X_val[-1:].copy()

# Plot validation predictions + future rolling forecast
predictions = rolling_forecast_on_plot(
    model,
    X_val, y_val,
    X_last_window,
    steps_ahead=24,   # Forecast next 24 hours
    y_min=y_min,
    y_max=y_max
)
