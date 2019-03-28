import numpy as np
import matplotlib.image as mpimg
import tensorflow as tf
import os
from tensorflow import keras
from skimage.transform import resize

DATASET_PATH = 'images/'

def read_images(dataset_path):
    images, labels = list(), list()

    classes = sorted(os.walk(dataset_path).__next__()[1])

    for c in classes:
        print("Class: " + c)
        c_dir = os.path.join(dataset_path, c)
        walk = os.walk(c_dir).__next__()
        for sample in walk[2]:
            if sample.endswith('.png'):
                image = resize(mpimg.imread(os.path.join(c_dir, sample)), (28, 28), anti_aliasing=True, mode='constant')
                images.append(image)
                labels.append(c)

    return np.array(images), np.array(labels)


train_images, train_labels = read_images("dataset_cqt")

model_path = "tfdata/"

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28, 4)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(train_labels.size, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=40)

model.save(model_path + "my_model.h5")
