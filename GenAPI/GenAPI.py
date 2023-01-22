import flask

from generator import Generator
from processor import Processor
from flask import Flask
from flask_cors import CORS
from PIL import Image

app = Flask("GenAPI")
CORS(app)

generator = Generator()
processor = Processor()


@app.route("/genapi", methods=['GET'])
def get_image():
    img = generator.generate()
    if img is False:
        return {"img": []}, 500

    img = processor.process(img)
    img = Image.fromarray(img)
    path_to_file = "img/1.png"
    img.save(path_to_file)
    return flask.send_file(path_to_file), 200

app.run()
