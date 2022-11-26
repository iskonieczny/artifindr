import flask

from generator import Generator
from flask import Flask
from flask_cors import CORS

from PIL import Image
from matplotlib import cm
import numpy as np

app = Flask("GenAPI")
CORS(app)

generator = Generator()


@app.route("/genapi", methods=['GET'])
def get_image():
    res = generator.generate()
    if res is False:
        return {"img": []}, 500

    # create and send a file
    img = Image.fromarray(np.uint8(cm.gist_earth(res)*255))
    # todo: img ids
    path_to_file = "img/1.png"
    img.save(path_to_file)
    return flask.send_file(path_to_file), 200


app.run()
