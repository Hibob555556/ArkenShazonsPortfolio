import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.preprocessing import MinMaxScaler # type: ignore

def load_and_preprocess(csv_file: str, target_col: str = "Temp_C", window_size: int = 24, test_size: float = 0.2):
    """
    Load CSV with temperature + time features, normalize, and create LSTM sequences.
    
    Args:
        csv_file: Path to CSV containing at least target_col and time features:
                  ['day_sin','day_cos','time_sin','time_cos'].
        target_col: Column to predict (temperature).
        window_size: Sequence length for LSTM.
        test_size: Fraction of data for validation.
    
    Returns:
        X_train, X_val, y_train, y_val: LSTM-ready sequences
        X_min, X_max, y_min, y_max: Scalars for rescaling
    """
    # ----------------------
    # 1. Load data
    # ----------------------
    df = pd.read_csv(csv_file)
    
    # Ensure required columns exist
    required_cols = [target_col, 'day_sin','day_cos','time_sin','time_cos']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV")
    
    # ----------------------
    # 2. Extract features and target
    # ----------------------
    feature_cols = ['day_sin','day_cos','time_sin','time_cos', target_col]  # include Temp_C as last feature for sequencing
    data = df[feature_cols].values.astype(np.float32)
    
    # ----------------------
    # 3. Normalize features and target separately
    # ----------------------
    X_scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()
    
    X_scaled = X_scaler.fit_transform(data[:, :-1])          # time features
    y_scaled = y_scaler.fit_transform(data[:, -1].reshape(-1,1))  # temperature
    
    # Combine scaled features + target for sequence creation
    full_scaled = np.hstack([X_scaled, y_scaled])
    
    # ----------------------
    # 4. Create sequences
    # ----------------------
    X, y = [], []
    for i in range(len(full_scaled) - window_size):
        X.append(full_scaled[i:i+window_size, :-1])  # features only
        y.append(full_scaled[i+window_size, -1])     # target temperature at next step
    
    X = np.array(X)
    y = np.array(y)
    
    # ----------------------
    # 5. Train/validation split
    # ----------------------
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, shuffle=False)
    
    # Return min/max for rescaling
    X_min, X_max = X_scaler.data_min_, X_scaler.data_max_
    y_min, y_max = y_scaler.data_min_[0], y_scaler.data_max_[0]
    
    return X_train, X_val, y_train, y_val, X_min, X_max, y_min, y_max
