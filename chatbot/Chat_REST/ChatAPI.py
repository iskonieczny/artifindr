from chat import Chat
from flask import Flask, request, jsonify

app = Flask("ChatAPI")

chat = Chat()


@app.route("/chatapi", methods=['GET'])
def get_response():
    data = request.json
    result = chat.response_to_api(data['chatbot_character'], data['last_tag_used'], data['message'])
    return result


app.run()
