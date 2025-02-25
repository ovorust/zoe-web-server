from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://zoe-web.onrender.com", "https://zoe-web-delta.vercel.app"]}})  # Habilita CORS para a origem específica



# Configurar a API do Gemini
genai.configure(api_key='AIzaSyDG7nEpQ6eeqiyWhIeUytZaI4Gqs9nOQZQ')
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

@app.route('/')
def home():
    return jsonify(message="Hello from Flask!")

@app.route('/chat', methods=['POST'])
def chat_route():
    data = request.json
    print("Recebido:", data)  # Verificar se os dados estão chegando corretamente

    phrase = data.get('message')
    if not phrase:
        print("ERROR: Nenhuma mensagem fornecida")
        return jsonify(error="No message provided"), 400

    print("Mensagem recebida:", phrase)  # Deve imprimir a mensagem corretamente

    response = chat.send_message(f'{phrase}')

    return jsonify(response=f'[zoe]{response.text}')

@app.route('/clear', methods=['POST'])
def clear_route():
    global chat
    chat = model.start_chat(history=[])
    print("Histórico de chat limpo")
    return jsonify(message="Chat history cleared")

if __name__ == '__main__':
    app.run(debug=True)