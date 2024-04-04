import pytest
from llm_messages_token_helper import count_tokens_for_message, get_token_limit


def test_get_token_limit():
    assert get_token_limit("gpt-35-turbo") == 4000
    assert get_token_limit("gpt-3.5-turbo") == 4000
    assert get_token_limit("gpt-35-turbo-16k") == 16000
    assert get_token_limit("gpt-3.5-turbo-16k") == 16000
    assert get_token_limit("gpt-4") == 8100
    assert get_token_limit("gpt-4-32k") == 32000


def test_get_token_limit_error():
    with pytest.raises(ValueError, match="Called with unknown model name: gpt-3"):
        get_token_limit("gpt-3")


# parameterize the model and the expected number of tokens
@pytest.mark.parametrize(
    "model",
    [
        "gpt-35-turbo",
        "gpt-3.5-turbo",
        "gpt-35-turbo-16k",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-32k",
        "gpt-4v",
    ],
)
def test_count_tokens_for_message(model: str):
    message = {
        # 1 token : 1 token
        "role": "user",
        # 1 token : 5 tokens
        "content": "Hello, how are you?",
    }
    assert count_tokens_for_message(model, message) == 9


def test_count_tokens_for_message_gpt4():
    message = {
        # 1 token : 1 token
        "role": "user",
        # 1 token : 5 tokens
        "content": "Hello, how are you?",
    }
    model = "gpt-4"
    assert count_tokens_for_message(model, message) == 9


def test_count_tokens_for_message_list():
    message = {
        # 1 token : 1 token
        "role": "user",
        # 1 token : 262 tokens
        "content": [
            {"type": "text", "text": "Describe this picture:"},  # 1 token  # 4 tokens
            {
                "type": "image_url",  # 2 tokens
                "image_url": {
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",  # 255 tokens
                    "detail": "auto",
                },
            },
        ],
    }
    model = "gpt-4"
    assert count_tokens_for_message(model, message) == 265


def test_count_tokens_for_message_error():
    message = {
        # 1 token : 1 token
        "role": "user",
        # 1 token : 5 tokens
        "content": {"key": "value"},
    }
    model = "gpt-35-turbo"
    with pytest.raises(ValueError, match="Could not encode unsupported message value type"):
        count_tokens_for_message(model, message)


def test_get_oai_chatmodel_tiktok_error():
    message = {
        "role": "user",
        "content": {"key": "value"},
    }
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message("", message)
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message(None, message)
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message("gpt44", message)
