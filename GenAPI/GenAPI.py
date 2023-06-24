
import flask
import uuid
import sys

from generator import Generator
from processor import Processor
from flask import Flask, request
from flask_cors import CORS

from PIL import Image
from matplotlib import cm
import numpy as np

import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask("GenAPI")
CORS(app)

DATABASE_HOST='postgres'
DATABASE_USER="postgres"
DATABASE_PASSWORD="secret"
DATABASE_NAME="api"

conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    host=DATABASE_HOST,
    password=DATABASE_PASSWORD
)


generator = Generator()
processor = Processor()

curr_user_faces = {}


@app.route("/generate", methods=['GET'])
def generate():
    img = generator.generate()
    if img is False:
        return {"img": []}, 500

    data = request.args
    user_id = data['user_id']
    filename = str(uuid.uuid4())
    img = Image.fromarray(processor.process(img))
    path_to_file = f"img/{filename}.png"
    img.save(path_to_file)
    curr_user_faces[user_id] = filename
    return flask.send_file(path_to_file), 200


@app.route("/accept", methods=['POST'])
def accept():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    data = request.get_json()
    user_id = data['user_id']
    name = data['name']
    gender = data['gender']
    bio = data['bio']

    if user_id not in curr_user_faces.keys():
        return {}, 400
    print(curr_user_faces[user_id], name, gender, bio)
    
    cur.execute("""INSERT INTO bots 
                  (img_path, name, gender, bio) VALUES 
                  (%s, %s, %s, %s)
                  RETURNING bot_id, img_path, name;""",
                  (curr_user_faces[user_id], name, gender, bio))
    result = cur.fetchall()[0]
    conn.commit()

    cur.execute("""INSERT INTO bot_user 
                  (bot_id, user_id) VALUES 
                  ((SELECT bot_id from bots where 
                  img_path=%s), %s);""",
                  (curr_user_faces[user_id], user_id))

    conn.commit()
    cur.close()
    return result, 200


@app.route("/face", methods=['GET'])
def face():
    cur = conn.cursor(cursor_factory=RealDictCursor)

    data = request.args
    #user_id = data['user_id']
    bot_id = data['bot_id']
    
    cur.execute("SELECT img_path from bots where bot_id=%s;",
                (bot_id,))
    result = cur.fetchall()
    if len(result) == 0:
        return {}, 404

    filename = result[0]['img_path']
    path_to_file = f"img/{filename}.png"
    cur.close()
    return flask.send_file(path_to_file), 200


app.run()
