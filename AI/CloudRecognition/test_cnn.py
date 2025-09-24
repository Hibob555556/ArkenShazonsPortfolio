from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load model
model = load_model("V5.h5")

# Image paths
img_with_cloud = "Data/Test/cirriform clouds/ca6921c72d873ba72be9722c58da5d2e.jpg"
img_no_cloud = "Data/Test/clear sky/7681d2d01a45f677f1087da485b4dfc3.jpg"

# Load and preprocess images
def preprocess(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # scale pixels
    return img_array

cloud_img_arr = preprocess(img_with_cloud)
no_cloud_img_arr = preprocess(img_no_cloud)

# Predict
cloud_prediction = model.predict(cloud_img_arr)
no_cloud_prediction = model.predict(no_cloud_img_arr)

# Interpret results (binary example)
cloud_label = "Cloud" if cloud_prediction[0][0] > 0.5 else "No Cloud"
no_cloud_label = "Cloud" if no_cloud_prediction[0][0] > 0.5 else "No Cloud"

print(f"Cloud Prediction: {cloud_label} ({cloud_prediction[0][0]:.4f})")
print(f"No Cloud Prediction: {no_cloud_label} ({no_cloud_prediction[0][0]:.4f})")
