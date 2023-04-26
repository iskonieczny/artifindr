import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import tensorflow as tf
from keras import layers
import time
from IPython import display

from tqdm import tqdm

PATH_SRC = "./dataset_refit"
IMG_DIM = 64
BATCH_SIZE = 128
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
data_set = []

for img_name in tqdm(os.listdir(PATH_SRC)):
    path = os.path.join(PATH_SRC, img_name)
    img = Image.open(path)
    data_set.append(np.array(img))
    print(img_name)
    if img_name.split("(")[1].split(")")[0] == "1000":
        break

print("Amount of data: ", len(data_set))

data_set = np.asarray(data_set, dtype=object)
data_set = np.reshape(data_set, (data_set.shape[0], IMG_DIM, IMG_DIM, 1)).astype('float32')
data_set = (data_set - 127.5) / 127.5
data_set = tf.data.Dataset.from_tensor_slices(data_set).shuffle(data_set.shape[0]).batch(BATCH_SIZE)


def make_generator_model():
    model = tf.keras.Sequential()
    model.add(layers.Dense(4 * 4 * 1024, use_bias=False, input_shape=(100,)))
    model.add(layers.Reshape((4, 4, 1024)))

    model.add(layers.Conv2DTranspose(512, 5, strides=2, padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())

    model.add(layers.Conv2DTranspose(256, 5, strides=2, padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())

    model.add(layers.Conv2DTranspose(128, 5, strides=2, padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())

    model.add(layers.Conv2DTranspose(1, 5, strides=2, padding='same', use_bias=False, activation='tanh'))
    assert model.output_shape == (None, 64, 64, 3)

    return model


generator = make_generator_model()


def make_discriminator_model():
    filters = 64
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(filters, (4, 4), strides=(2, 2), padding='same',
                            input_shape=[64, 64, 3]))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters * 2, (4, 4), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters * 4, (4, 4), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters * 8, (4, 4), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization())

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model


discriminator = make_discriminator_model()


def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator_optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.0002, beta_1=0.5)
discriminator_optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.0002, beta_1=0.5)

checkpoint_dir = 'checkpoints_new'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                 discriminator_optimizer=discriminator_optimizer,
                                 generator=generator,
                                 discriminator=discriminator)

EPOCHS = 100
noise_dim = 100
num_examples_to_generate = 16

seed = tf.random.normal([num_examples_to_generate, noise_dim])


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    tensor = np.squeeze(tensor, 2)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1

    image = Image.fromarray(tensor)
    image_to_return = image.convert('L')
    return image_to_return


def generate_and_save_images(model, epoch, test_input):
    predictions = model(test_input, training=False)

    _ = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        img_to_show = tensor_to_image(predictions[i])
        plt.imshow(img_to_show, cmap="gray")
        plt.axis('off')
        plt.grid(False)

    plt.savefig('./gan_new_model/01___{:04d}.png'.format(epoch))


@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, noise_dim], stddev=0.2)

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))


ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=70)
# checkpoint.restore('checkpoints_grayscale\\ckpt-26')


def train(dataset, epochs):
    for epoch in range(epochs):
        start = time.time()

        for image_batch in dataset:
            train_step(image_batch)

        display.clear_output(wait=True)
        generate_and_save_images(generator,
                                 epoch + 1,
                                 seed)

        if (epoch + 1) % 5 == 0:
            checkpoint.save(file_prefix=checkpoint_prefix)

        print('Time for epoch {} is {} sec'.format(epoch + 1, time.time() - start))

    display.clear_output(wait=True)
    generate_and_save_images(generator,
                             epochs,
                             seed)
    generator.compile(generator_optimizer)
    generator.save("model/model.h5")


train(data_set, EPOCHS)
