import glob
import os
import numpy as np
import matplotlib.image as mpimg
from skimage.transform import resize


def read_images(folder_path):
    images = list()

    files = glob.glob(os.path.join(folder_path, '*.png'))
    for file in files:
        image = resize(mpimg.imread(file), (28, 28), anti_aliasing=True, mode='constant')
        images.append(image)

    return np.array(images)

