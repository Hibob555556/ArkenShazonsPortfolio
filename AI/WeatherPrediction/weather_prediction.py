import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense # type: ignore
from sklearn.preprocessing import MinMaxScaler # type: ignore
import pandas as pd
import numpy as np

# define functions
def create_sequences(X, y, window_size):
    """
      Description: Create a sequence from the time data. Use a sliding 24 hour scale.
      Args:
        - X | Number
        - y | Number
        - window_size | Number

      Returns:
        - sequence_array | numpy.array
    """
    X_seq, y_seq = [], []
    for i in range(len(X) - window_size):
        X_seq.append(X[i:i+window_size])
        y_seq.append(y[i+window_size])
    return np.array(X_seq), np.array(y_seq)


# load and parse csv
df = pd.read_csv("WeatherData/WeatherDataset.csv")
df = df.sort_values(by="Date/Time")
df = df.reset_index(drop=True)

# select features and targets
features = ["Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]
target = "Temp_C"
X = df[features].values
y = df[target].values.reshape(-1, 1)

# normalize data
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# create time sequences
window_size = 24 
X_seq, y_seq = create_sequences(X_scaled, y_scaled, window_size)

# split data into training and validation sets
split_ratio = 0.8
split_index = int(len(X_seq) * split_ratio)
X_train, X_val = X_seq[:split_index], X_seq[split_index:]
y_train, y_val = y_seq[:split_index], y_seq[split_index:]

model = Sequential()
model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=32
)
