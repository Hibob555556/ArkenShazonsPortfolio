import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf # type: ignore
from tensorflow import keras # type: ignore
from tensorflow.keras import layers # type: ignore
from tensorflow.keras.callbacks import TensorBoard # type: ignore
from tensorflow.keras import Model # type: ignore

# define data locations
# --------------------------------------------------
train_dir = "cloud-data/Train"
valid_dir = "cloud-data/Validation"
# --------------------------------------------------


# define image properties
# --------------------------------------------------
img_height = 128
img_width = 128
batch_size = 8
# --------------------------------------------------


# specify datasets
# --------------------------------------------------
training_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

validation_ds = tf.keras.preprocessing.image_dataset_from_directory(
    valid_dir,
    seed=321,
    image_size=(img_height, img_width),
    batch_size=batch_size
)
# --------------------------------------------------

class_names = training_ds.class_names
print(class_names)

# Normalization and optimization
# --------------------------------------------------
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

normalization_layer = tf.keras.layers.Rescaling(1./255)
train_ds = training_ds.map(lambda x, y: (data_augmentation(normalization_layer(x)), y))
val_ds = validation_ds.map(lambda x, y: (normalization_layer(x), y))

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
# --------------------------------------------------


# define model
# --------------------------------------------------
model = tf.keras.Sequential()
# --------------------------------------------------


# define layers to add to the model
# --------------------------------------------------
conv_layer_16 = tf.keras.layers.Conv2D(
    filters=16,
    kernel_size=(3, 3),
    strides=(1, 1),
    padding='same',
    activation='relu',
    input_shape=(img_height, img_width, 3)
)

conv_layer_32 = tf.keras.layers.Conv2D(
    filters=32,
    kernel_size=(3, 3),
    strides=(1, 1),
    padding='same',
    activation='relu',
)

pooling_layer = tf.keras.layers.MaxPooling2D(
    pool_size=(2, 2),
    strides=(2, 2),
    padding='same'
)

hidden_dense_layer_16 = tf.keras.layers.Dense(
    units=16,
    activation='relu',
    use_bias=True,
    kernel_initializer='he_normal',
    kernel_regularizer=tf.keras.regularizers.l2(0.0005),
    bias_initializer='zeros',
)

hidden_dense_layer_8 = tf.keras.layers.Dense(
    units=8,
    activation='relu',
    use_bias=True,
    kernel_initializer='he_normal',
    kernel_regularizer=tf.keras.regularizers.l2(0.0005),
    bias_initializer='zeros',
)

output_dense_layer = tf.keras.layers.Dense(
    units=3,
    activation='softmax',
    use_bias=True,
    kernel_initializer='he_normal',
    kernel_regularizer=tf.keras.regularizers.l2(0.0005),
    bias_initializer='zeros',
)
# --------------------------------------------------


# Add layers to the model
# --------------------------------------------------
model.add(conv_layer_16)
model.add(tf.keras.layers.BatchNormalization())
model.add(pooling_layer)

model.add(conv_layer_32)
model.add(tf.keras.layers.BatchNormalization())
model.add(pooling_layer)

model.add(tf.keras.layers.GlobalAveragePooling2D())

model.add(hidden_dense_layer_16)
tf.keras.layers.Dropout(0.2)

model.add(hidden_dense_layer_8)
tf.keras.layers.Dropout(0.1)

model.add(output_dense_layer)
# --------------------------------------------------

# implement early stopping to help prevent overfitting
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=6, restore_best_weights=True
)

# record weight for each epoch
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1)

# Compile and train the model
# --------------------------------------------------
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)

model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=120,
    callbacks=[early_stopping, tensorboard_callback]
)

model.summary()

layer_outputs = [layer.output for layer in model.layers if 'conv2d' in layer.name]
activation_model = Model(inputs=model.input, outputs=layer_outputs)

# Take one batch of images and labels from the dataset
for images, labels in train_ds.take(1):
    some_input_image_batch = images  # shape: (batch_size, 128, 128, 3)
    break

activations = activation_model.predict(some_input_image_batch)
# --------------------------------------------------
