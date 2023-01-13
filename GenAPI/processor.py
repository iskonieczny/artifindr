import numpy as np
import matplotlib.pyplot as plt
import cv2
from generator import Generator
import requests
import os
from PIL import Image


class Processor:
    def __init__(self):
        self.url = "https://api.deepai.org/api/colorizer"
        self.RES = 2048
        self.api_key = os.environ['api_key']
        self.alpha = 0.3
        self.beta = 20
        self.searchWindowSize = 20
        self.kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

    def __upscale(self, image):
        return cv2.resize(image, dsize=(self.RES, self.RES), interpolation=cv2.INTER_CUBIC)

    def __denoise(self, image):
        return cv2.fastNlMeansDenoising(image, None, self.searchWindowSize)

    def __sharpen(self, image):
        return cv2.filter2D(src=image, ddepth=-1, kernel=self.kernel)

    def __lower_contrast(self, image):
        return cv2.convertScaleAbs(image, alpha=self.alpha, beta=self.beta)

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
        # os.remove("temp/temp_in.png")
        # os.remove("temp/temp_out.png")
        return image

    def process(self, image):
        image = self.__upscale(image)
        image = self.__denoise(image)
        image = self.__sharpen(image)
        image = self.__lower_contrast(image)
        image = self.__colourise(image)

        return image


gen = Generator()
img = gen.generate()
proc = Processor()
img = proc.process(img)
plt.imshow(img)
plt.show()


