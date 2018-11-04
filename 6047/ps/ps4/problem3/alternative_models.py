from keras.models import *
from keras.layers import *
import keras

def deep_conv_net():
    model = Sequential()
    model.add(Conv2D(32,
                     input_shape=(4, 100, 1),
                     kernel_size=(4, 6),
                     activation="relu",
                     padding="same"))
    model.add(Conv2D(64,
                     kernel_size=(4, 3),
                     activation="relu",
                     padding="same"))
    model.add(MaxPool2D(pool_size=(4, 6)))
    model.add(Conv2D(128,
                     kernel_size=(4, 3),
                     activation="relu",
                     padding="same"))
    model.add(Conv2D(1024,
                     input_shape=(4, 100, 1),
                     kernel_size=(1, 1),
                     activation="relu",
                     padding="same"))
    model.add(Flatten())
    model.add(Dense(64, activation="relu"))
    model.add(Dense(2, activation="softmax")) # same as 1 output sigmoid
    return model