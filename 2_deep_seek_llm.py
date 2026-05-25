import openai
import json
import os
"""
Improving the Readability of the Chatbot’s Response
"""

# Query local instance of the OpenAPI on port 1234
openai.api_base = "http://127.0.0.1:1234/v1"
openai.api_key = "lm-studio"

# chat-based completion from the model: supports roles like "system", "user", and "assistant."
completion = openai.ChatCompletion.create(
    model="deepseek-r1-distill-qwen-7b",
    messages=[
        # system: sets the behavior or context for the AI assistant.
        {"role": "system", "content": "Answer the following queries without including any internal chain-of-thought in its final answer."},
        # user: provides the input to the AI assistant.
        {"role": "user", "content":"Introduce yourself."}
    ],
    # temperature: controls the randomness of the model's output.
    # 0 = deterministic, 1 = most random
    temperature=0.7,
)

# completion: typically includes a choices list. Each “choice” represents a possible completion 
# (though usually there’s just one by default unless you request more).
# completion.choices[0] selects the first (and presumably only) completion choice.
# .message is the actual chat message object returned by the model

print(completion.choices[0].message)

content = completion["choices"][0]["message"]["content"]

print(content)
# Now post-process to remove the chain-of-thought if present
if "</think>" in content:
    final_output = content.split("</think>")[1].strip()
else:
    final_output = content

print("Final output:")
print(final_output)

# File to store conversation history
history_file = "converstation_history.json"

# Function to load the convesrsation history from the file
def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    else:
        # if no file exists, start with an empty file
        return []

def save_history(history):
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

conversation_history = load_history()

if not conversation_history:
    conversation_history.append(
        {
            "role": "system", 
            "content": "Answer the following queries without including any internal chain-of-thought in its final answer."
        }
    )

def add_message(role, content):
    conversation_history.append(
        {
            "role": role,
            "content": content
        }
    )
    save_history(conversation_history)

# Example: Adding user message
user_message = "Thanks that's actually great! I'll do my best to get you onto my project team."
add_message("user", user_message)

# Send the complete conversation to the chatbot
try:
    completion = openai.ChatCompletion.create(
        model="deepseek-r1-distill-qwen-7b",
        messages=conversation_history,
        temperature=0.7,
    )
    
    print("Raw completion response:")
    print(completion)
    print("\n" + "="*50 + "\n")
    
    print(completion.choices[0].message)
    
    content = completion["choices"][0]["message"]["content"]
    
    print(content)
    
except Exception as e:
    print(f"Error calling OpenAI API: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
