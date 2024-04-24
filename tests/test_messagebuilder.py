import pytest
from openai_messages_token_helper import build_messages, count_tokens_for_message

from .messages import system_message_short, system_message_unicode, user_message, user_message_unicode


def test_messagebuilder():
    messages = build_messages("gpt-35-turbo", system_message_short["message"]["content"])
    assert messages == [system_message_short["message"]]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == system_message_short["count"]


def test_messagebuilder_append():
    messages = build_messages(
        "gpt-35-turbo", system_message_short["message"]["content"], new_user_message=user_message["message"]["content"]
    )
    assert messages == [system_message_short["message"], user_message["message"]]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == system_message_short["count"]
    assert count_tokens_for_message("gpt-35-turbo", messages[1]) == user_message["count"]


def test_messagebuilder_unicode():
    messages = build_messages("gpt-35-turbo", system_message_unicode["message"]["content"])
    assert messages == [system_message_unicode["message"]]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == system_message_unicode["count"]


def test_messagebuilder_unicode_append():
    messages = build_messages(
        "gpt-35-turbo",
        system_message_unicode["message"]["content"],
        new_user_message=user_message_unicode["message"]["content"],
    )
    assert messages == [system_message_unicode["message"], user_message_unicode["message"]]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == system_message_unicode["count"]
    assert count_tokens_for_message("gpt-35-turbo", messages[1]) == user_message_unicode["count"]


def test_messagebuilder_model_error():
    model = "phi-3"
    with pytest.raises(ValueError, match="Called with unknown model name: phi-3"):
        build_messages(
            model, system_message_short["message"]["content"], new_user_message=user_message["message"]["content"]
        )


def test_messagebuilder_model_fallback():
    model = "phi-3"
    messages = build_messages(
        model,
        system_message_short["message"]["content"],
        new_user_message=user_message["message"]["content"],
        fallback_to_default=True,
    )
    assert messages == [system_message_short["message"], user_message["message"]]
    assert count_tokens_for_message(model, messages[0], default_to_cl100k=True) == system_message_short["count"]
    assert count_tokens_for_message(model, messages[1], default_to_cl100k=True) == user_message["count"]
