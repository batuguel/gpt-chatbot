import openai
import json
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import shutil
from dotenv import load_dotenv
from utils import prepare_sushi_context, prepare_parking_context



#DELETE SESSION DATA ON EVERY RESTART
session_dir = 'flask_session'
if os.path.exists(session_dir):
    shutil.rmtree(session_dir)
os.makedirs(session_dir, exist_ok=True)

# Load env variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret-key'
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Configure server-side session management
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
# initialize client
client = openai.OpenAI(api_key=openai.api_key)



@app.route('/sushi_chat', methods=['POST'])
def sushi_chat():

    # Get the user message from the request
    user_message = request.json.get('prompt')

    # Initialize or retrieve the existing conversation history
    if 'sushi_history' not in session:
        print("sushi history not in session")
        session['sushi_history'] = []
    sushi_history = session['sushi_history']

    # get sushi context
    sushi_context = prepare_sushi_context()
    # Include the sushi context and the user message in the messages list
    messages = sushi_context + sushi_history + [{"role": "user", "content": user_message}]
    # print("history: ", history)
    # print("whole message: ", messages)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            frequency_penalty=0.5,
        )
        # Access completions text
        if response.choices:
            completion_text = response.choices[0].message.content
        else:
            completion_text = 'No response generated.'  

        # Update the conversation history and save to session
        sushi_history.append({"role": "system", "content": user_message})
        sushi_history.append({"role": "system", "content": completion_text})
        session['sushi_history'] = sushi_history
        session.modified = True

        # Return generated response      
        return jsonify(response=completion_text)
    
    # Handle exceptions
    except Exception as e:
        return jsonify(error=str(e)), 500



@app.route('/parking_chat', methods=['POST'])
def parking_chat():
    user_message = request.json.get('prompt')

    if 'parking_history' not in session:
        session['parking_history'] = []
    parking_history = session['parking_history']

    # Get parking context
    parking_context = prepare_parking_context()
    messages = parking_context + parking_history + [{"role": "user", "content": user_message}]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            frequency_penalty=0.5,
        )
        if response.choices:
            completion_text = response.choices[0].message.content
        else:
            completion_text = 'No response generated.'

        # Update the conversation history for parking and save to session
        parking_history.append({"role": "system", "content": user_message})
        parking_history.append({"role": "system", "content": completion_text})
        session['parking_history'] = parking_history
        session.modified = True

        return jsonify(response=completion_text)
    except Exception as e:
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
    app.run(debug=True)