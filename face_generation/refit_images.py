import numpy as np
from PIL import Image
from tqdm import tqdm
import os
import cv2

PATH_SRC = "./dataset"
PATH_OUT = "./dataset_refit"


def refit_image(image):
    image = image.convert("RGBA")
    if image.mode in ('RGBA', 'LA'):
        background = Image.new(image.mode[:-1], image.size, (0, 0, 0))
        background.paste(image, image.split()[-1])
        image = background
    image = np.array(image)
    image = cv2.resize(image, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)
    image = Image.fromarray(image, "RGB")
    return image


for img_name in tqdm(os.listdir(PATH_SRC)):
    path = os.path.join(PATH_SRC, img_name)
    img = refit_image(Image.open(path))
    img.save(PATH_OUT + "/" + img_name.split(".")[0]+".jpeg", 'JPEG')



