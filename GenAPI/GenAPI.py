from generator import Generator
from flask import Flask

app = Flask("GenAPI")

generator = Generator()


@app.route("/genapi", methods=['GET'])
def get_image():
    res = generator.generate()
    if res is False:
        return {"img": []}, 500
    return {"img": res.tolist()}, 200


app.run()
