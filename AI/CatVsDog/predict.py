import tensorflow as tf
import numpy as np

# Class names (from your training dataset order)
class_names = ['cat', 'dog']

def predict_image(def_model, image_path):
    # load in image
    image = tf.keras.utils.load_img(image_path,target_size=(128,128))
    image_array = tf.keras.utils.img_to_array(image)

    # scale image
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array,axis=0) # batch dimension

    # predict the image
    predictions = def_model.predict(image_array)
    predicted_class = np.argmax(predictions,axis=1)[0]

    print(f"Prediction: {class_names[predicted_class]}")


cat_path = "data/test/cat.jpg"
dog_path = "data/test/dog.jpg"

model = tf.keras.models.load_model("my_model.h5")

for i in range(50):
    print("Attempt to predict cat image")
    predict_image(model, cat_path)

    print("Attempt to predict dog image")
    predict_image(model, dog_path)