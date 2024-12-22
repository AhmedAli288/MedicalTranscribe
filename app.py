from flask import Flask, request, jsonify, render_template
from huggingface_hub import InferenceClient

app = Flask(__name__)

# Initialize Hugging Face Inference Client
API_KEY = "hf_your_api_key"  # Replace with your Hugging Face API key
client = InferenceClient(api_key=API_KEY)

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

        # Prepare the input for LLaMA 3.3
        messages = [
            {"role": "user", "content": user_message}
        ]

        # Call Hugging Face API to generate a response
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct", 
            messages=messages,
            max_tokens=200
        )

        # Extract the response from the model
        assistant_response = completion.choices[0].message["content"]

        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
