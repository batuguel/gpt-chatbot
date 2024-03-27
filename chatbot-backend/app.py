import openai
import json
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import shutil
from dotenv import load_dotenv
from utils import prepare_sushi_context



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



@app.route('/chat', methods=['POST'])
def chat():

    # Get the user message from the request
    user_message = request.json.get('prompt')

    # Initialize or retrieve the existing conversation history
    if 'history' not in session:
        print("history not in session")
        session['history'] = []
    history = session['history']

    # get sushi context
    sushi_context = prepare_sushi_context()
    # Include the sushi context and the user message in the messages list
    messages = sushi_context + history + [{"role": "user", "content": user_message}]
    # print("history: ", history)
    # print("whole message: ", messages)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        # Access completions text
        if response.choices:
            completion_text = response.choices[0].message.content
        else:
            completion_text = 'No response generated.'  

        # Update the conversation history and save to session
        history.append({"role": "system", "content": user_message})
        history.append({"role": "system", "content": completion_text})
        session['history'] = history
        session.modified = True

        # Return generated response      
        return jsonify(response=completion_text)
    
    # Handle exceptions
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)