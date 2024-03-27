import openai
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from utils import prepare_sushi_context


# Load env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
# initialize client
client = openai.OpenAI(api_key=openai.api_key)

@app.route('/chat', methods=['POST'])
def chat():

    # Get the user message from the request
    data = request.get_json()
    user_message = data['prompt']

    # get sushi context
    sushi_context = prepare_sushi_context()

    try:
        # Start the messages with sushi context, then add the user's message
        messages = sushi_context + [{"role": "user", "content": user_message}]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        # Access completions text
        if response.choices:
            completion_text = response.choices[0].message.content
        else:
            completion_text = 'No response generated.'  
        # Return generated response      
        return jsonify(response=completion_text)
    
    # Handle exceptions
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)