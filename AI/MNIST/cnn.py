import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf # type: ignore
from tensorflow import keras # type: ignore
from tensorflow.keras.datasets import mnist # type: ignore
from tensorflow.keras import layers # type: ignore
from tensorflow.keras.callbacks import TensorBoard # type: ignore


# Load the dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize pixel values to 0-1
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Reshape the data to match CNN input: (samples, height, width, channels)
x_train = x_train.reshape((-1, 28, 28, 1))
x_test = x_test.reshape((-1, 28, 28, 1))

# create the model and session saver
model = keras.Sequential() 


# Define convelutional layers
# --------------------------------------------------
conv_layer_32 = tf.keras.layers.Conv2D(
    filters=32,
    kernel_size=(3, 3),
    strides=(1, 1),
    padding='same',
    activation='relu',
    input_shape=(28, 28, 1)
)

conv_layer_64 = tf.keras.layers.Conv2D(
    filters=64,
    kernel_size=(3, 3),
    strides=(1, 1),
    padding='same',
    activation='relu',
    input_shape=(28, 28, 1)
)

conv_layer_128 = tf.keras.layers.Conv2D(
    filters=128,
    kernel_size=(3, 3),
    strides=(1, 1),
    padding='valid',
    activation='relu',
    input_shape=(28, 28, 1)
)
# --------------------------------------------------



# Define pooling layers
# --------------------------------------------------
pooling_layer_32 = tf.keras.layers.MaxPooling2D(
    pool_size=(2, 2),
    strides=(2, 2),
    padding='same'
)

pooling_layer_64 = tf.keras.layers.MaxPooling2D(
    pool_size=(2, 2),
    strides=(2, 2),
    padding='same'
)

pooling_layer_128 = tf.keras.layers.MaxPooling2D(
    pool_size=(2, 2),
    strides=(2, 2),
    padding='same'
)
# --------------------------------------------------


# Define flattening layers
# --------------------------------------------------
flatten_layer = tf.keras.layers.Flatten(data_format=None)
# --------------------------------------------------


# Define dense layers
# --------------------------------------------------
hidden_dense_layer = tf.keras.layers.Dense(
    units=64,
    activation='relu',
    use_bias=True,
    kernel_initializer='he_normal',
    kernel_regularizer=tf.keras.regularizers.l2(0.01),
    bias_initializer='zeros',
    activity_regularizer=tf.keras.regularizers.l2(0.01)
)

output_dense_layer = tf.keras.layers.Dense(
    units=10,
    activation='softmax',
    use_bias=True,
    kernel_initializer='he_normal',
    kernel_regularizer=tf.keras.regularizers.l2(0.01),
    bias_initializer='zeros',
    activity_regularizer=tf.keras.regularizers.l2(0.01)
)
# --------------------------------------------------


# Add Layers
# --------------------------------------------------
model.add(conv_layer_32)
model.add(pooling_layer_32)
model.add(conv_layer_64)
model.add(pooling_layer_64)
model.add(conv_layer_128)
model.add(pooling_layer_128)
model.add(flatten_layer)
model.add(hidden_dense_layer)
model.add(output_dense_layer)


# create model for visualization
tf.keras.utils.plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)


# compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# implement early stopping to help prevent overfitting
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=3, restore_best_weights=True
)


# record weight for each epoch
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1)


# train the model
history = model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    shuffle=True,
    callbacks=[early_stopping, tensorboard_callback]
)

