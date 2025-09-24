import pandas as pd
import numpy as np

weather = pd.read_csv("data/weather.csv")
encoded = pd.read_csv("data/time_encoding.csv")

# Parse Date/Time automatically
weather['Date/Time'] = pd.to_datetime(weather['Date/Time'], infer_datetime_format=True)

# Extract day of year and minute of day
weather['day'] = weather['Date/Time'].dt.dayofyear
weather['minute'] = weather['Date/Time'].dt.hour * 60 + weather['Date/Time'].dt.minute

# Merge with time encoding CSV
df = pd.merge(weather, encoded, on=['day','minute'])

# Save combined CSV
df.to_csv("data/weather_combined.csv", index=False)
