import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf

# ----------------------------
# Settings
# ----------------------------
MODEL_PATH = "my_model.h5"
TEST_DIR = "Data/Test"  # folder structure: TEST_DIR/class_name/*.jpg
IMG_SIZE = (256, 256)   # same as training
BINARY_THRESHOLD = 0.5  # threshold for binary classification

# ----------------------------
# Load model
# ----------------------------
model = load_model(MODEL_PATH)
print("Model loaded successfully!")

# ----------------------------
# Prepare test data
# ----------------------------
# Collect all image paths and labels
image_paths = []
labels = []

class_names = sorted(os.listdir(TEST_DIR))  # assumes each subfolder is a class
class_to_idx = {name: idx for idx, name in enumerate(class_names)}

for class_name in class_names:
    class_folder = os.path.join(TEST_DIR, class_name)
    for fname in os.listdir(class_folder):
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            image_paths.append(os.path.join(class_folder, fname))
            labels.append(class_to_idx[class_name])

labels = np.array(labels)

# ----------------------------
# Load and preprocess images
# ----------------------------
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# ----------------------------
# Predict all images
# ----------------------------
y_pred_probs = []
for img_path in image_paths:
    img_array = preprocess_image(img_path)
    pred = model.predict(img_array)
    y_pred_probs.append(pred[0][0])  # assuming binary output

y_pred_probs = np.array(y_pred_probs)
y_pred = (y_pred_probs > BINARY_THRESHOLD).astype(int)

# ----------------------------
# Confusion Matrix
# ----------------------------
cm = confusion_matrix(labels, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

# ----------------------------
# Classification Report
# ----------------------------
print("Classification Report:")
print(classification_report(labels, y_pred, target_names=class_names))

# ----------------------------
# Optional: show some predictions
# ----------------------------
for i in range(min(5, len(image_paths))):
    img = image.load_img(image_paths[i], target_size=IMG_SIZE)
    plt.imshow(img)
    plt.title(f"True: {class_names[labels[i]]} | Pred: {class_names[y_pred[i]]}")
    plt.axis('off')
    plt.show()
