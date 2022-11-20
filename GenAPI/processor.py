import numpy as np
import matplotlib.pyplot as plt
import cv2
from generator import Generator

class Processor:
    def __init__(self):
        self.RES = 256

    def __upscale(self, image):
        return cv2.resize(image, dsize=(self.RES, self.RES), interpolation=cv2.INTER_CUBIC)

    def __denoise(self, image):
        return cv2.fastNlMeansDenoising(image, None, 20)

    def __sharpen(self, image):
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

    def __colourise(self, image):
        pass

    def process(self, image):
        image = self.__upscale(image)
        image = self.__denoise(image)
        image = self.__sharpen(image)
        # image = self.__colourise(image)
        return image

# prc = Processor()
# gnr = Generator()
# image = gnr.generate()
# plt.imshow(image, cmap="gray")
# plt.show()
# image = prc.process(image)
# plt.imshow(image, cmap="gray")
# plt.show()