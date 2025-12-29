import pytest

from openai_messages_token_helper import count_tokens_for_message, count_tokens_for_system_and_tools, get_token_limit

from .functions import FUNCTION_COUNTS, search_sources_toolchoice_auto
from .image_messages import IMAGE_MESSAGE_COUNTS
from .messages import system_message, system_message_with_name, user_message


def test_get_token_limit():
    assert get_token_limit("gpt-35-turbo") == 4000
    assert get_token_limit("gpt-3.5-turbo") == 4000
    assert get_token_limit("gpt-35-turbo-16k") == 16000
    assert get_token_limit("gpt-3.5-turbo-16k") == 16000
    assert get_token_limit("gpt-4") == 8100
    assert get_token_limit("gpt-4-32k") == 32000
    assert get_token_limit("gpt-4o") == 128000
    # GPT-5 models
    assert get_token_limit("gpt-5") == 272000
    assert get_token_limit("gpt-5-mini") == 272000
    assert get_token_limit("gpt-5-nano") == 272000
    assert get_token_limit("gpt-5-chat") == 128000
    assert get_token_limit("gpt-5.1") == 272000
    assert get_token_limit("gpt-5.1-chat") == 111616
    assert get_token_limit("gpt-5.2") == 272000
    assert get_token_limit("gpt-5.2-chat") == 111616


def test_get_token_limit_error():
    with pytest.raises(ValueError, match="Called with unknown model name: gpt-3"):
        get_token_limit("gpt-3")


def test_get_token_limit_default(caplog):
    with caplog.at_level("WARNING"):
        assert get_token_limit("gpt-3", default_to_minimum=True) == 4000
        assert "Model gpt-3 not found, defaulting to minimum token limit 4000" in caplog.text


# parameterize the model and the expected number of tokens
@pytest.mark.parametrize(
    "model, count_key",
    [
        ("gpt-35-turbo", "count"),
        ("gpt-3.5-turbo", "count"),
        ("gpt-35-turbo-16k", "count"),
        ("gpt-3.5-turbo-16k", "count"),
        ("gpt-4", "count"),
        ("gpt-4-32k", "count"),
        ("gpt-4v", "count"),
        ("gpt-4o", "count_omni"),
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
def test_count_tokens_for_message(model, count_key, message):
    assert count_tokens_for_message(model, message["message"]) == message[count_key]


@pytest.mark.parametrize(
    "model, count_key",
    [
        ("gpt-4", "count"),
        ("gpt-4o", "count"),
        ("gpt-4o-mini", "count_4o_mini"),
    ],
)
def test_count_tokens_for_message_list(model, count_key):
    for message_count_pair in IMAGE_MESSAGE_COUNTS:
        assert count_tokens_for_message(model, message_count_pair["message"]) == message_count_pair[count_key]


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


def test_count_tokens_for_system_and_tools_fallback(caplog):
    function_count_pair = search_sources_toolchoice_auto
    with caplog.at_level("WARNING"):
        counted_tokens = count_tokens_for_system_and_tools(
            "llama-3.1",
            function_count_pair["system_message"],
            function_count_pair["tools"],
            function_count_pair["tool_choice"],
            default_to_cl100k=True,
        )
        assert counted_tokens == function_count_pair["count"]
        assert "Model llama-3.1 not found, defaulting to CL100k encoding" in caplog.text


@pytest.mark.parametrize("model", ["gpt-5", "gpt-5-mini", "gpt-5-nano"])
def test_count_tokens_for_message_reasoning_model_warning(caplog, model):
    """Test that reasoning models log warnings when counting tokens."""
    with caplog.at_level("WARNING"):
        count_tokens_for_message(model, user_message["message"], default_to_cl100k=True)
        assert (
            f"Model {model} is a reasoning model. Token usage estimates may not reflect actual costs due to reasoning tokens."
            in caplog.text
        )


def test_count_tokens_for_message_non_reasoning_model_no_warning(caplog):
    """Test that non-reasoning models (like gpt-5-chat) do not log warnings."""
    with caplog.at_level("WARNING"):
        count_tokens_for_message("gpt-5-chat", user_message["message"], default_to_cl100k=True)
        # Should only have encoding warning, not reasoning model warning
        warning_messages = [record.message for record in caplog.records if record.levelname == "WARNING"]
        reasoning_warnings = [msg for msg in warning_messages if "reasoning model" in msg]
        assert len(reasoning_warnings) == 0
