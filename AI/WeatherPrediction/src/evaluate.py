import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error  # type: ignore

def evaluate_model(model, X_val, y_val, y_min, y_max):
    # Predict
    y_pred_scaled = model.predict(X_val)
    # Invert scaling
    y_val_original = y_val * (y_max - y_min) + y_min
    y_pred_original = y_pred_scaled * (y_max - y_min) + y_min

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(y_val_original, label="Actual Temp_C")
    plt.plot(y_pred_original, label="Predicted Temp_C")
    plt.xlabel("Time step")
    plt.ylabel("Temperature (°C)")
    plt.title("Validation: Actual vs Predicted")
    plt.legend()
    plt.show()

    # Metrics
    mae = mean_absolute_error(y_val_original, y_pred_original)
    rmse = np.sqrt(mean_squared_error(y_val_original, y_pred_original))
    print(f"Validation MAE: {mae:.2f} °C")
    print(f"Validation RMSE: {rmse:.2f} °C")
