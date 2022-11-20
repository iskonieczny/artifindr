import tensorflow as tf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def tensor_to_image(tensor):
    tensor = (1 + tensor) * 127.5
    tensor = np.array(tensor, dtype=np.uint8)
    tensor = np.squeeze(tensor, 2)
    image = Image.fromarray(tensor)
    image_to_return = image.convert('L')
    return image_to_return


class Generator:
    def __init__(self):
        self.model = tf.keras.models.load_model("model/model.h5", compile=False)
        self.INPUT_SHAPE = 100
        self.GEN_NUM = 1

    def __generate_image_grayscale(self, seed):
        predictions = self.model(seed, training=False)
        image = tensor_to_image(predictions[0])
        # plt.imshow(image, cmap="gray")
        # plt.axis('off')
        # plt.grid(False)
        # plt.show()
        return np.array(image)

    def generate(self, seed=None):
        try:
            if seed is None:
                seed = tf.random.normal([self.GEN_NUM, self.INPUT_SHAPE])
            else:
                assert seed.shape == [self.GEN_NUM, self.INPUT_SHAPE]
            return self.__generate_image_grayscale(seed)
        except AssertionError:
            return False
