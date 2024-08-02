# openai-messages-token-helper

A helper library for estimating tokens used by messages and building messages lists that fit within the token limits of a model.
Currently designed to work with the OpenAI GPT models (including GPT-4 turbo with vision).
Uses the tiktoken library for tokenizing text and the Pillow library for image-related calculations.

## Installation

Install the package:

```sh
python3 -m pip install openai-messages-token-helper
```

## Usage

The library provides the following functions:

* [`build_messages`](#build_messages)
* [`count_tokens_for_message`](#count_tokens_for_message)
* [`count_tokens_for_image`](#count_tokens_for_image)
* [`get_token_limit`](#get_token_limit)

### `build_messages`

Build a list of messages for a chat conversation, given the system prompt, new user message,
and past messages. The function will truncate the history of past messages if necessary to
stay within the token limit.

Arguments:

* `model` (`str`): The model name to use for token calculation, like gpt-3.5-turbo.
* `system_prompt` (`str`): The initial system prompt message.
* `tools` (`List[openai.types.chat.ChatCompletionToolParam]`): (Optional) The tools that will be used in the conversation. These won't be part of the final returned messages, but they will be used to calculate the token count.
* `tool_choice` (`openai.types.chat.ChatCompletionToolChoiceOptionParam`): (Optional) The tool choice that will be used in the conversation. This won't be part of the final returned messages, but it will be used to calculate the token count.
* `new_user_content` (`str | List[openai.types.chat.ChatCompletionContentPartParam]`): (Optional) The content of new user message to append.
* `past_messages` (`list[openai.types.chat.ChatCompletionMessageParam]`): (Optional) The list of past messages in the conversation.
* `few_shots` (`list[openai.types.chat.ChatCompletionMessageParam]`): (Optional) A few-shot list of messages to insert after the system prompt.
* `max_tokens` (`int`): (Optional) The maximum number of tokens allowed for the conversation.
* `fallback_to_default` (`bool`): (Optional) Whether to fallback to default model/token limits if model is not found. Defaults to `False`.


Returns:

* `list[openai.types.chat.ChatCompletionMessageParam]`

Example:

```python
from openai_messages_token_helper import build_messages

messages = build_messages(
    model="gpt-35-turbo",
    system_prompt="You are a bot.",
    new_user_content="That wasn't a good poem.",
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

### `count_tokens_for_message`

Counts the number of tokens in a message.

Arguments:

* `model` (`str`): The model name to use for token calculation, like gpt-3.5-turbo.
* `message` (`openai.types.chat.ChatCompletionMessageParam`): The message to count tokens for.
* `default_to_cl100k` (`bool`): Whether to default to the CL100k token limit if the model is not found.

Returns:

* `int`: The number of tokens in the message.

Example:

```python
from openai_messages_token_helper import count_tokens_for_message

message = {
    "role": "user",
    "content": "Hello, how are you?",
}
model = "gpt-4"
num_tokens = count_tokens_for_message(model, message)
```

### `count_tokens_for_image`

Count the number of tokens for an image sent to GPT-4-vision, in base64 format.

Arguments:

* `image` (`str`): The base64-encoded image.

Returns:

* `int`: The number of tokens used up for the image.

Example:

```python

Count the number of tokens for an image sent to GPT-4-vision:

```python
from openai_messages_token_helper import count_tokens_for_image

image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEA..."
num_tokens = count_tokens_for_image(image)
```

### `get_token_limit`

Get the token limit for a given GPT model name (OpenAI.com or Azure OpenAI supported).

Arguments:

* `model` (`str`): The model name to use for token calculation, like gpt-3.5-turbo (OpenAI.com) or gpt-35-turbo (Azure).
* `default_to_minimum` (`bool`): Whether to default to the minimum token limit if the model is not found.

Returns:

* `int`: The token limit for the model.

Example:

```python
from openai_messages_token_helper import get_token_limit

model = "gpt-4"
max_tokens = get_token_limit(model)
```
