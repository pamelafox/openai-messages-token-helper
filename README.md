# llm-messages-token-helper

A helper library for estimating tokens used by messages and building messages lists that fit within the token limits of a model.
Currently designed to work with the OpenAI GPT models (including GPT-4 turbo with vision).
Uses the tiktoken library for tokenizing text and the Pillow library for image-related calculations.

## Installation

Install the package:

```sh
python3 -m pip install llm-messages-token-helper
```

## Usage

Build a messages list that fits within the max tokens for a model:

```python
from llm_messages_token_helper import build_messages, count_tokens_for_message

messages = build_messages(
    model="gpt-35-turbo",
    system_prompt="You are a bot.",
    new_user_message="That wasn't a good poem.",
    past_messages=[
        {
            "role": "user",
            "content": "Write me a poem",
        },
        {
            "role": "assistant",
            "content": "Tuna tuna I love tuna",
        },
    ],
    few_shots=[
        {
            "role": "user",
            "content": "Write me a poem",
        },
        {
            "role": "assistant",
            "content": "Tuna tuna is the best",
        },
    ]
)
```

Count the number of tokens in a message:

```python
from llm_messages_token_helper import count_tokens

message = {
    "role": "user",
    "content": "Hello, how are you?",
}
model = "gpt-4"
num_tokens = count_tokens_for_message(model, message)
```

Count the number of tokens for an image sent to GPT-4-vision:

```python
from llm_messages_token_helper import count_tokens_for_image

image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEA..."
num_tokens = count_tokens_for_image(image)
```

Get the max tokens for a model:

```python
from llm_messages_token_helper import get_token_limit

model = "gpt-4"
max_tokens = get_token_limit(model)
```
