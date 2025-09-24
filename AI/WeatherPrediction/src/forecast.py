import matplotlib.pyplot as plt
import numpy as np

def rolling_forecast_on_plot(model, X_val, y_val, X_last_window, steps_ahead, y_min, y_max):
    """
    Combines validation actual/predicted and future rolling forecast on the same plot.
    
    X_val, y_val: validation sequences and targets
    X_last_window: the last sequence to start rolling forecast
    steps_ahead: how many future steps to predict
    y_min, y_max: for inverting scaling
    """
    # --- 1. Validation predictions ---
    y_pred_val_scaled = model.predict(X_val)
    y_val_original = y_val * (y_max - y_min) + y_min
    y_pred_val = y_pred_val_scaled * (y_max - y_min) + y_min

    # --- 2. Rolling forecast ---
    rolling_preds = []
    current_window = X_last_window.copy()
    for _ in range(steps_ahead):
        pred_scaled = model.predict(current_window)[0,0]
        rolling_preds.append(pred_scaled)

        # Shift window: keep last features, append prediction as the last "target" feature
        new_window = np.vstack([current_window[0,1:], current_window[0,-1]])
        current_window = np.array([new_window])

    rolling_preds_original = np.array(rolling_preds) * (y_max - y_min) + y_min

    # --- 3. Combine for plotting ---
    plt.figure(figsize=(12,6))
    plt.plot(y_val_original, label="Validation Actual")
    plt.plot(y_pred_val, label="Validation Predicted")
    # Extend x-axis for rolling forecast
    x_forecast = np.arange(len(y_val_original), len(y_val_original)+steps_ahead)
    plt.plot(x_forecast, rolling_preds_original, label=f"Rolling Forecast ({steps_ahead} steps)")
    
    plt.xlabel("Time step")
    plt.ylabel("Temperature (°C)")
    plt.title("Validation Predictions + Rolling Forecast")
    plt.legend()
    plt.show()

    return rolling_preds_original
