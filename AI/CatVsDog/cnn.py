import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf # type: ignore
from tensorflow.keras import Model # type: ignore
from tensorflow import keras # type: ignore
from tensorflow.keras import layers # type: ignore
from tensorflow.keras.callbacks import TensorBoard # type: ignore

train_data = tf.keras.utils.image_dataset_from_directory(
    "data/cat_dog/Train",
    image_size=(128,128),
    batch_size=32
)

validate_data = tf.keras.utils.image_dataset_from_directory(
    "data\cat_dog\Validation",
    image_size=(128,128),
    batch_size=32
)

# create model and session saver
model = keras.Sequential()

model = tf.keras.Sequential([
    # First Conv Block
    tf.keras.layers.Conv2D(16, (3, 3), padding='same', activation=None,
                           input_shape=(128, 128, 3), kernel_initializer='he_normal'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.ReLU(),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), padding='same'),

    # Second Conv Block
    tf.keras.layers.Conv2D(32, (3, 3), padding='same', activation=None,
                           kernel_initializer='he_normal'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.ReLU(),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), padding='same'),

    # Transition to Dense
    tf.keras.layers.GlobalAveragePooling2D(),

    # Dense Block 1
    tf.keras.layers.Dense(16, activation='relu', use_bias=True,
                          kernel_initializer='he_normal',
                          kernel_regularizer=tf.keras.regularizers.l2(0.0005),
                          bias_initializer='zeros'),
    tf.keras.layers.Dropout(0.2),

    # Dense Block 2
    tf.keras.layers.Dense(8, activation='relu', use_bias=True,
                          kernel_initializer='he_normal',
                          kernel_regularizer=tf.keras.regularizers.l2(0.0005),
                          bias_initializer='zeros'),
    tf.keras.layers.Dropout(0.1),

    # Output Layer
    tf.keras.layers.Dense(2, activation='softmax', use_bias=True,
                          kernel_initializer='he_normal',
                          kernel_regularizer=tf.keras.regularizers.l2(0.0005),
                          bias_initializer='zeros')
])

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
    train_data,
    validation_data=validate_data,
    epochs=10,
    callbacks=[early_stopping, tensorboard_callback]
)

model.save("my_model.h5")
model.summary()

layer_outputs = [layer.output for layer in model.layers if 'conv2d' in layer.name]
activation_model = Model(inputs=model.inputs, outputs=layer_outputs)