from chat import Chat
from flask import Flask, request
import os
from flask_cors import CORS
import psycopg2
import random

app = Flask("ChatAPI")

CORS(app)

chat = Chat()

# zobaczyć jak działa host
# zobaczyć co zwraca cur.execute i w razie co przemapować
DATABASE_HOST='localhost:5432'
DATABASE_USER="postgres"
DATABASE_PASSWORD="secret"
DATABASE_NAME="api"

conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    host=DATABASE_HOST,
    password=DATABASE_PASSWORD
)


list_of_characters = ['formal.json', 'high_ego.json', 'old.json', 'regular.json', 'robot.json', 'teenager.json']

@app.route("/get_new_msg", methods=['GET'])
def get_response():
    cur = conn.cursor()

    data = request.json
    user_id = data['user_id']
    bot_id = data['bot_id']
    msg = data['message']

    cur.execute(f'INSERT INTO messages (user_id, bot_id, content) VALUES (\'{user_id}\', {bot_id}, \'{msg})\';')

    cur.execute(f'SELECT character FROM bots WHERE bot_id={bot_id};')
    chatbot_character = cur.fetchone()[0]
    
    if chatbot_character == "null":
        chatbot_character = list_of_characters[random.randint(0, len(list_of_characters) - 1)]
        cur.execute(f'UPDATE bots SET character = \'{chatbot_character}\' WHERE bot_id={bot_id};')

    result = chat.response_to_api(chatbot_character, data['last_tag_used'], data['message'])
    new_message = result['response']

    #dodaj result do bazy
    cur.execute(f'INSERT INTO messages (user_id, bot_id, content, from_bot) VALUES (\'{user_id}\', {bot_id}, \'{new_message}\', true);')
    result = cur.fetchone()[0]
    cur.close()
    return result

@app.route("/get_all_user_msg", methods=['GET'])
def get_response():
    cur = conn.cursor()

    data = request.json
    user_id = data['user.id']
    bot_id = data['bot.id']

    cur.execute(f'SELECT * FROM messages WHERE user_id=\'{user_id}\' AND bot_id={bot_id};')
    result = cur.fetchone()[0]
    cur.close()

    return result

@app.route("/get_all_user_bots", methods=['GET'])
def get_response():
    cur = conn.cursor()

    data = request.json
    user_id = data['user.id']

    cur.execute(f'SELECT bot_id FROM bot_user WHERE user_id=\'{user_id}\'')
    result = cur.fetchone()[0]
    cur.close()

    return result

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)