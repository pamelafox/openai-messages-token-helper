import pytest
from openai_messages_token_helper import count_tokens_for_message, get_token_limit

from .messages import system_message, system_message_with_name, text_and_image_message, user_message


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
@pytest.mark.parametrize(
    "message",
    [
        user_message,
        system_message,
        system_message_with_name,
    ],
)
def test_count_tokens_for_message(model: str, message: dict):
    assert count_tokens_for_message(model, message["message"]) == message["count"]


def test_count_tokens_for_message_list():
    model = "gpt-4"
    assert count_tokens_for_message(model, text_and_image_message["message"]) == text_and_image_message["count"]


def test_count_tokens_for_message_error():
    message = {
        "role": "user",
        "content": {"key": "value"},
    }
    model = "gpt-35-turbo"
    with pytest.raises(ValueError, match="Could not encode unsupported message value type"):
        count_tokens_for_message(model, message)


def test_get_oai_chatmodel_tiktok_error():
    message = {
        "role": "user",
        "content": "hello",
    }
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message("", message)
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message(None, message)
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message("gpt44", message)
