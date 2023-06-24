import PIL.Image
import numpy as np
import cv2 as cv
import requests
import os
from PIL import Image
from matplotlib import pyplot as plt

from generator import Generator


class Processor:
    def __init__(self):
        # self.url = "https://api.deepai.org/api/colorizer"
        self.RES = 2048
        # self.api_key = os.environ['api_key']
        self.alpha = 0.35
        self.beta = 20
        self.searchWindowSize = 21
        self.kernel = np.array([[0, -1, 0],
                                [-1, 5, -1],
                                [0, -1, 0]])
        self.blur_kernel = np.array([[1 / 6, 1 / 6, 1 / 6],
                                     [1 / 6, 1 / 6, 1 / 6],
                                     [1 / 6, 1 / 6, 1 / 6]])

    def __upscale(self, image):
        return cv.resize(image, dsize=(self.RES, self.RES), interpolation=cv.INTER_CUBIC)

    def __denoise(self, image):
        return cv.fastNlMeansDenoising(image, None, self.searchWindowSize)

    def __gaussian_blur(self, image):
        return cv.filter2D(src=image, ddepth=-1, kernel=self.blur_kernel)

    def __sharpen(self, image):
        return cv.filter2D(src=image, ddepth=-1, kernel=self.kernel)

    def __lower_contrast(self, image):
        return cv.convertScaleAbs(image, alpha=self.alpha, beta=self.beta)

    def __colourise(self, image):
        temp = Image.fromarray(image)
        temp.save("temp/temp_in.png")
        res = requests.post(
            self.url,
            files={
                'image': open("temp/temp_in.png", "rb"),
            },
            headers={'api-key': self.api_key}
        )
        print(res.text)
        r = requests.get(res.json()["output_url"])
        with open("temp/temp_out.png", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

        image = Image.open("temp/temp_out.png")
        return image

    def process(self, image):
        image = self.__upscale(image)
        image = self.__denoise(image)
        image = self.__sharpen(image)
        image = self.__gaussian_blur(image)
        image = self.__lower_contrast(image)
        # image = self.__colourise(image)

        return image


# op = open('C:\\Users\\fcb-i\\Downloads\\example_grayscale_old.png', "r")
proc = Processor()
gen = Generator()
img = gen.generate()
print(img.shape)
plt.imshow(img, cmap='gray')
plt.show()
plt.imshow(proc.process(img),cmap='gray')
plt.show()
