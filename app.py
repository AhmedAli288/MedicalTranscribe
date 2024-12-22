from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables from the .env file
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not API_KEY:
    raise ValueError("API key is missing. Please add it to your .env file.")

# Initialize OpenAI Hugging Face client
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key=API_KEY
)

app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# Serve the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Chat endpoint to process user messages
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the user's message from the request
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message received"}), 400

        # Prepare the input for the model
        messages = [
            {"role": "user", "content": user_message}
        ]

        # Call Hugging Face API to generate a response
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            max_tokens=500
        )

        # Extract the response from the model
        assistant_response = completion.choices[0].message["content"]

        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
