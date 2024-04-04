from llm_messages_token_helper import build_messages, count_tokens_for_message


def test_messagebuilder():
    messages = build_messages("gpt-35-turbo", "You are a bot.")
    assert messages == [
        # 1 token, 1 token, 1 token, 5 tokens
        {"role": "system", "content": "You are a bot."}
    ]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == 8


def test_messagebuilder_append():
    messages = build_messages("gpt-35-turbo", "You are a bot.", new_user_message="Hello, how are you?")
    assert messages == [
        # 1 token, 1 token, 1 token, 5 tokens
        {"role": "system", "content": "You are a bot."},
        # 1 token, 1 token, 1 token, 6 tokens
        {"role": "user", "content": "Hello, how are you?"},
    ]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == 8
    assert count_tokens_for_message("gpt-35-turbo", messages[1]) == 9


def test_messagebuilder_unicode():
    messages = build_messages("gpt-35-turbo", "a\u0301")
    assert messages == [
        # 1 token, 1 token, 1 token, 1 token
        {"role": "system", "content": "á"}
    ]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == 4


def test_messagebuilder_unicode_append():
    messages = build_messages("gpt-35-turbo", "a\u0301", new_user_message="a\u0301")
    assert messages == [
        # 1 token, 1 token, 1 token, 1 token
        {"role": "system", "content": "á"},
        # 1 token, 1 token, 1 token, 1 token
        {"role": "user", "content": "á"},
    ]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == 4
    assert count_tokens_for_message("gpt-35-turbo", messages[1]) == 4
