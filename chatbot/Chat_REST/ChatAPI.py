from chat import Chat
from flask import Flask, request
import os
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import random
import sys

app = Flask("ChatAPI")

CORS(app)

chat = Chat()

DATABASE_HOST = 'postgres'
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "secret"
DATABASE_NAME = "api"

conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    host=DATABASE_HOST,
    password=DATABASE_PASSWORD
)

list_of_characters = ['formal', 'high_ego', 'old', 'regular', 'robot', 'teenager']


@app.route("/get_new_msg", methods=['GET'])
def get_response1():
    cur = conn.cursor(cursor_factory=RealDictCursor)

    data = request.args
    user_id = str(data['user_id'])
    bot_id = data['bot_id']
    msg = data['message']
    last_tag_used = data['last_tag_used']

    cur.execute('INSERT INTO messages (user_id, bot_id, content) VALUES (%s, %s, %s);',
                (user_id, bot_id, msg))
    conn.commit()

    cur.execute('SELECT character FROM bots WHERE bot_id=%s;', bot_id)
    response = cur.fetchall()[0]
    chatbot_character = response['character']

    if chatbot_character == None:
        chatbot_character = list_of_characters[random.randint(0, len(list_of_characters) - 1)]
        cur.execute('UPDATE bots SET character=%s WHERE bot_id=%s;',
                    (chatbot_character, bot_id))

    result = chat.response_to_api(chatbot_character, last_tag_used, msg)
    new_message = result['response']

    # dodaj result do bazy
    cur.execute('INSERT INTO messages (user_id, bot_id, content, from_bot) VALUES (%s, %s, %s, true);',
                (user_id, bot_id, new_message))
    conn.commit()
    cur.close()
    return result


@app.route("/get_all_user_msg", methods=['GET'])
def get_response2():
    cur = conn.cursor(cursor_factory=RealDictCursor)

    data = request.args
    user_id = str(data['user_id'])
    bot_id = data['bot_id']

    cur.execute('SELECT * FROM messages WHERE user_id=%s AND bot_id=%s;',
                (user_id, bot_id))
    result = cur.fetchall()
    cur.close()

    return result


@app.route("/get_all_user_bots", methods=['GET'])
def get_response3():
    cur = conn.cursor(cursor_factory=RealDictCursor)

    data = request.args
    user_id = str(data['user_id'])

    cur.execute('SELECT bots.* FROM bots RIGHT JOIN bot_user ON bots.bot_id=bot_user.bot_id WHERE bot_user.user_id=%s;',
                (user_id,))
    result = cur.fetchall()
    cur.close()

    return result


port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)