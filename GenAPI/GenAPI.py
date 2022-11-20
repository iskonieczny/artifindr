from generator import Generator
from flask import Flask, jsonify, request

app = Flask("GenAPI")

generator = Generator()


@app.get("/genapi")
def get_image():
    res = generator.generate()

    return jsonify({"img": res.tolist()})


app.run()
