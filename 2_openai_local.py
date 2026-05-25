import openai

# Query local instance of the OpenAPI on port 1234
openai.api_base = "http://127.0.0.1:1234/v1"
# Any calls made via the openai library will include this key in the headers for authentication.
openai.api_key = "lm-studio"

# chat-based completion from the model: supports roles like “system”, “user”, and “assistant.”
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