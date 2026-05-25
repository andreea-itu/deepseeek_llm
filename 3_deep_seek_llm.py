"""
Tutorial 3: 
Front-end integration (creating our intelligent interface):
"""
from flask import Flask, request, jsonify, render_template
import openai

# Create Flask application
app = Flask(__name__)

# Configure your local AI model endpoint and API key
openai.api_base = "http://127.0.0.1:1234/v1"
openai.api_key = "lm-studio"

# Create Root route
@app.route("/")
def index():
    # Server the frontent HTML page
    # Renders the index.html file (frontend UI)
    return render_template("index.html")

# Handle incoming messages from the user
@app.route("/chat", methods=["POST"])
def chat():
    # Extracts the user's message from the json payload
    user_message = request.json.get('message')
    # If the message is missing return a Bad Request:400
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Send message to local LLM
    try:
        # Create a chat completion request to the local AI model
        completion = openai.ChatCompletion.create(
            model="deepseek-r1-distill-qwen-7b",
            messages=[
                {"role": "system", "content": "Answer happy!"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )
        
        # Extract the AI's response
        content = completion["choices"][0]["message"]["content"]

        # Remove any chain-of-thought if present
        
        # If your model uses tags like <think>...</think> to separate reasoning from the final answer, 
        # this removes the reasoning part and keeps just the answer.
        if "</think>" in content:
            final_output = content.split("</think>")[-1].strip()
        else:
            final_output = content
        
        return jsonify({"response": final_output})
    
    except Exception as e:
        return jsonify({"error":str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

# Notes:
# 1. app.run(debug=True) is used to run the Flask application in debug mode.
# 2. debug=True allows the server to automatically reload when code changes are detected.
