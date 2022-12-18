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
BATCH_SIZE = 32
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
data_set = []

for img_name in tqdm(os.listdir(PATH_SRC)):
    path = os.path.join(PATH_SRC, img_name)
    img = Image.open(path)
    data_set.append(np.array(img))
    # limiting the amount of data
    if img_name.split(".")[0] == "05000":
        break

data_set = np.asarray(data_set, dtype=object)
data_set = np.reshape(data_set, (data_set.shape[0], IMG_DIM, IMG_DIM, 3)).astype('float32')
data_set = (data_set - 127.5) / 127.5
data_set = tf.data.Dataset.from_tensor_slices(data_set).shuffle(data_set.shape[0]).batch(BATCH_SIZE)


def make_generator_model():
    model = tf.keras.Sequential()
    model.add(layers.Dense(64 * 64 * 3, use_bias=False, input_shape=(100,)))
    model.add(layers.Reshape((64, 64, 3)))
    model.add(
        tf.keras.layers.Conv2D(128, 4, strides=1, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(
        tf.keras.layers.Conv2D(128, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(
        tf.keras.layers.Conv2D(256, 4, strides=1, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(
        tf.keras.layers.Conv2D(256, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2DTranspose(512, 4, strides=1, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(
        tf.keras.layers.Conv2D(512, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2DTranspose(512, 4, strides=1, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(tf.keras.layers.Conv2DTranspose(512, 4, strides=2, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2DTranspose(256, 4, strides=1, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(tf.keras.layers.Conv2DTranspose(256, 4, strides=2, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.Conv2DTranspose(128, 4, strides=2, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(tf.keras.layers.Conv2DTranspose(128, 4, strides=1, padding='same', kernel_initializer='he_normal',
                                              use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Conv2DTranspose(3, 4, strides=1, padding='same', activation='tanh'))
    model.add(layers.Reshape((64, 64, 3)))

    return model


generator = make_generator_model()


def make_discriminator_model():
    filters = 64
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(filters, (4, 4), strides=(2, 2), padding='same',
                            input_shape=[64, 64, 3]))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2D(128, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2D(256, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2D(256, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Conv2D(512, 4, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(1))
    return model


discriminator = make_discriminator_model()


def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

checkpoint_dir = 'checkpoints_2'
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
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
    return Image.fromarray(tensor)


def generate_and_save_images(model, epoch, test_input):
    predictions = model(test_input, training=False)

    _ = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        img_to_show = tensor_to_image(predictions[i])
        plt.imshow(img_to_show)
        plt.axis('off')
        plt.grid(False)

    plt.savefig('./gan_2_images/image_at_epoch_{:04d}.png'.format(epoch+7))
    # plt.show()


@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, noise_dim])

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


ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=50)
checkpoint.restore(ckpt_manager.latest_checkpoint)


def train(dataset, epochs):
    for epoch in range(epochs):
        start = time.time()

        for image_batch in dataset:
            train_step(image_batch)

        display.clear_output(wait=True)
        generate_and_save_images(generator,
                                 epoch + 1,
                                 seed)

        checkpoint.save(file_prefix=checkpoint_prefix)

        print('Time for epoch {} is {} sec'.format(epoch + 8, time.time() - start))

    display.clear_output(wait=True)
    generate_and_save_images(generator,
                             epochs,
                             seed)


train(data_set, EPOCHS)
