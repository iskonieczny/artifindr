import numpy as np
from PIL import Image
from tqdm import tqdm
import os
import cv2

PATH_SRC = "./dataset/person"
PATH_OUT = "./dataset_refit"

line_size = 5
blur_value = 5
total_color = 5
SIZE = 64

def refit_image(image):
    image = np.array(image)
    image = cv2.resize(image, dsize=(SIZE, SIZE), interpolation=cv2.INTER_LINEAR)
    edges = edge_mask(image, line_size, blur_value)
    image = color_quantization(image, total_color)
    blurred = cv2.bilateralFilter(image, d=7, sigmaColor=200, sigmaSpace=200)
    image = cv2.bitwise_and(blurred, blurred, mask=edges)
    image = Image.fromarray(image, "RGB")
    return image


def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges


def color_quantization(img, k):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result


for img_name in tqdm(os.listdir(PATH_SRC)):
    path = os.path.join(PATH_SRC, img_name)
    img = refit_image(Image.open(path))
    img.save(PATH_OUT + "/" + img_name.split(".")[0] + ".jpeg", 'JPEG')
