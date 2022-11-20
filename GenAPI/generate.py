import tensorflow as tf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

generator = tf.keras.models.load_model("model/model.h5", compile=False)
INPUT_SHAPE = 100
GEN_NUM = 1

def tensor_to_image(tensor):
    tensor = (1 + tensor) * 127.5
    tensor = np.array(tensor, dtype=np.uint8)
    tensor = np.squeeze(tensor, 2)
    image = Image.fromarray(tensor)
    image_to_return = image.convert('L')
    return image_to_return


def generate_image_grayscale(model, input):
    predictions = model(input, training=False)
    for i in range(predictions.shape[0]):
        img_to_show = tensor_to_image(predictions[i])
        plt.imshow(img_to_show, cmap="gray")
        plt.axis('off')
        plt.grid(False)

    plt.show()



seed = tf.random.normal([GEN_NUM, INPUT_SHAPE])
generate_image_grayscale(generator, seed)

