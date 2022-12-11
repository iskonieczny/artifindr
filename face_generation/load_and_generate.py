import tensorflow as tf
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

dir = "checkpoints_1"

latest = tf.train.latest_checkpoint(dir)
model = tf.keras.models.load_model(latest)
seed = tf.random.normal([16, 100])



def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)

    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
    return Image.fromarray(tensor, mode="L")


def generate_and_save_images(model, input):
    predictions = model(input, training=False)

    _ = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        img_to_show = tensor_to_image(predictions[i])
        plt.imshow(img_to_show)
        plt.axis('off')
        plt.grid(False)

    plt.show()


generate_and_save_images(model.generator, seed)