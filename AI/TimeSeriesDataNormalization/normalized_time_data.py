import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

# -----------------------------
# Parameters
# -----------------------------
graph_type = "2D"  # "2D" or "3D"
csv_output = True   # Set to True to save CSV
output_file = "time_encoding.csv"

days = np.arange(1, 366)             # Days 1–365
minutes_in_day = np.arange(0, 24*60, 1)  # 1-minute intervals

# -----------------------------
# Meshgrid for day × minute
# -----------------------------
day_grid, minute_grid = np.meshgrid(days, minutes_in_day, indexing='ij')

# -----------------------------
# Cyclical encodings
# -----------------------------
day_sin = np.sin(2 * np.pi * day_grid / 365)
day_cos = np.cos(2 * np.pi * day_grid / 365)
time_sin = np.sin(2 * np.pi * minute_grid / 1440)
time_cos = np.cos(2 * np.pi * minute_grid / 1440)

# -----------------------------
# Unique scalar per (day, minute)
# -----------------------------
combined_value = day_sin + day_cos + time_sin + time_cos
normalized_value = (combined_value - combined_value.min()) / (combined_value.max() - combined_value.min())

# -----------------------------
# Convert minutes to hours for plotting
# -----------------------------
time_hours = minute_grid / 60

# -----------------------------
# CSV Export
# -----------------------------
if csv_output:
    print(f"Saving dataset to {output_file} ...")
    # Flatten all arrays to 1D
    day_flat = day_grid.flatten()
    minute_flat = minute_grid.flatten()
    day_sin_flat = day_sin.flatten()
    day_cos_flat = day_cos.flatten()
    time_sin_flat = time_sin.flatten()
    time_cos_flat = time_cos.flatten()
    normalized_flat = normalized_value.flatten()

    # Write to CSV
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(["day", "minute", "day_sin", "day_cos", "time_sin", "time_cos", "normalized_value"])
        # Data
        for i in range(len(day_flat)):
            writer.writerow([day_flat[i], minute_flat[i], day_sin_flat[i], day_cos_flat[i],
                             time_sin_flat[i], time_cos_flat[i], normalized_flat[i]])
    print("CSV saved successfully!")

# -----------------------------
# Plotting
# -----------------------------
if graph_type.upper() == "2D":
    plt.figure(figsize=(14, 6))
    plt.imshow(normalized_value, aspect='auto', cmap='viridis', origin='lower')
    plt.colorbar(label='Normalized Unique Value')
    plt.xlabel('Minute of Day Index')
    plt.ylabel('Day of Year')
    plt.title('Unique Scalar per Day and Minute of the Year (2D Heatmap)')
    plt.show()

elif graph_type.upper() == "3D":
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Use rstride/cstride to speed up plotting without losing data
    surf = ax.plot_surface(
        time_hours, day_grid, normalized_value,
        rstride=10, cstride=10,  # adjust for speed vs smoothness
        cmap='plasma', edgecolor='none', alpha=0.95
    )

    ax.set_xlabel('Time of Day (hours)')
    ax.set_ylabel('Day of Year')
    ax.set_zlabel('Normalized Unique Value')
    ax.set_title('3D Visualization of Combined Daily and Yearly Cycles')
    fig.colorbar(surf, shrink=0.5, aspect=10, label='Normalized Unique Value')

    # Optional: better viewing angle
    ax.view_init(elev=30, azim=-60)

    plt.show()

else:
    print("Invalid graph_type! Choose '2D' or '3D'.")
