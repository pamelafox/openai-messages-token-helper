from __future__ import annotations

from collections.abc import Mapping

import tiktoken

from .images_helper import count_tokens_for_image

MODELS_2_TOKEN_LIMITS = {
    "gpt-35-turbo": 4000,
    "gpt-3.5-turbo": 4000,
    "gpt-35-turbo-16k": 16000,
    "gpt-3.5-turbo-16k": 16000,
    "gpt-4": 8100,
    "gpt-4-32k": 32000,
    "gpt-4v": 128000,
}


AOAI_2_OAI = {"gpt-35-turbo": "gpt-3.5-turbo", "gpt-35-turbo-16k": "gpt-3.5-turbo-16k", "gpt-4v": "gpt-4-turbo-vision"}


def get_token_limit(model: str) -> int:
    """
    Get the token limit for a given GPT model name (OpenAI.com or Azure OpenAI supported).
    Args:
        model (str): The name of the model to get the token limit for.
    Returns:
        int: The token limit for the model.
    """
    if model not in MODELS_2_TOKEN_LIMITS:
        raise ValueError(f"Called with unknown model name: {model}")
    return MODELS_2_TOKEN_LIMITS[model]


def count_tokens_for_message(model: str, message: Mapping[str, object]) -> int:
    """
    Calculate the number of tokens required to encode a message. Based off cookbook:
    https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

    Args:
        model (str): The name of the model to use for encoding.
        message (Mapping): The message to encode, in a dictionary-like object.
    Returns:
        int: The total number of tokens required to encode the message.

    >> model = 'gpt-3.5-turbo'
    >> message = {'role': 'user', 'content': 'Hello, how are you?'}
    >> count_tokens_for_message(model, message)
    13
    """

    encoding = tiktoken.encoding_for_model(get_oai_chatmodel_tiktok(model))
    # Assumes we're using a recent model
    tokens_per_message = 3

    num_tokens = tokens_per_message
    for key, value in message.items():
        if isinstance(value, list):
            # For GPT-4-vision support, based on https://github.com/openai/openai-cookbook/pull/881/files
            for item in value:
                # Note: item[type] does not seem to be counted in the token count
                if item["type"] == "text":
                    num_tokens += len(encoding.encode(item["text"]))
                elif item["type"] == "image_url":
                    num_tokens += count_tokens_for_image(item["image_url"]["url"], item["image_url"]["detail"])
        elif isinstance(value, str):
            num_tokens += len(encoding.encode(value))
        else:
            raise ValueError(f"Could not encode unsupported message value type: {type(value)}")
        if key == "name":
            num_tokens += 1
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def get_oai_chatmodel_tiktok(aoaimodel: str) -> str:
    message = "Expected valid OpenAI GPT model name"
    if aoaimodel == "" or aoaimodel is None:
        raise ValueError(message)
    if aoaimodel not in AOAI_2_OAI and aoaimodel not in MODELS_2_TOKEN_LIMITS:
        raise ValueError(message)
    return AOAI_2_OAI.get(aoaimodel, aoaimodel)
