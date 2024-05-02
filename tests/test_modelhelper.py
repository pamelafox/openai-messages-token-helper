import pytest
from openai_messages_token_helper import count_tokens_for_message, count_tokens_for_system_and_tools, get_token_limit

from .functions import FUNCTION_COUNTS
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


def test_get_token_limit_default(caplog):
    with caplog.at_level("WARNING"):
        assert get_token_limit("gpt-3", default_to_minimum=True) == 4000
        assert "Model gpt-3 not found, defaulting to minimum token limit 4000" in caplog.text


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


def test_count_tokens_for_message_model_error():
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message("", user_message["message"])
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message(None, user_message["message"])
    with pytest.raises(ValueError, match="Expected valid OpenAI GPT model name"):
        count_tokens_for_message("gpt44", user_message["message"])


def test_count_tokens_for_message_model_default(caplog):
    model = "phi-3"
    with caplog.at_level("WARNING"):
        assert count_tokens_for_message(model, user_message["message"], default_to_cl100k=True) == user_message["count"]
        assert "Model phi-3 not found, defaulting to CL100k encoding" in caplog.text


@pytest.mark.parametrize(
    "function_count_pair",
    FUNCTION_COUNTS,
)
def test_count_tokens_for_system_and_tools(function_count_pair):
    counted_tokens = count_tokens_for_system_and_tools(
        "gpt-35-turbo",
        function_count_pair["system_message"],
        function_count_pair["tools"],
        function_count_pair["tool_choice"],
    )
    expected_tokens = function_count_pair["count"]
    diff = counted_tokens - expected_tokens
    assert (
        diff >= 0 and diff <= 3
    ), f"Expected {expected_tokens} tokens, got {counted_tokens}. Counted tokens is only allowed to be off by 3 in the over-counting direction."
