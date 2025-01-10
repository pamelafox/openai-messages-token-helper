import typing

import pytest
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)

from openai_messages_token_helper import build_messages, count_tokens_for_message

from .functions import search_sources_toolchoice_auto
from .image_messages import text_and_tiny_image_message
from .messages import (
    assistant_message_dresscode,
    assistant_message_perf,
    assistant_message_perf_short,
    system_message_long,
    system_message_short,
    system_message_unicode,
    user_message,
    user_message_dresscode,
    user_message_perf,
    user_message_pm,
    user_message_unicode,
)


def test_messagebuilder():
    messages = build_messages("gpt-35-turbo", system_message_short["message"]["content"])
    assert messages == [system_message_short["message"]]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == system_message_short["count"]


def test_messagebuilder_imagemessage():
    messages = build_messages(
        "gpt-35-turbo",
        system_message_short["message"]["content"],
        new_user_content=text_and_tiny_image_message["message"]["content"],
    )
    assert messages == [system_message_short["message"], text_and_tiny_image_message["message"]]


def test_messagebuilder_append():
    messages = build_messages(
        "gpt-35-turbo", system_message_short["message"]["content"], new_user_content=user_message["message"]["content"]
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
        new_user_content=user_message_unicode["message"]["content"],
    )
    assert messages == [system_message_unicode["message"], user_message_unicode["message"]]
    assert count_tokens_for_message("gpt-35-turbo", messages[0]) == system_message_unicode["count"]
    assert count_tokens_for_message("gpt-35-turbo", messages[1]) == user_message_unicode["count"]


def test_messagebuilder_model_error():
    model = "phi-3"
    with pytest.raises(ValueError, match="Called with unknown model name: phi-3"):
        build_messages(
            model, system_message_short["message"]["content"], new_user_content=user_message["message"]["content"]
        )


def test_messagebuilder_model_fallback():
    model = "phi-3"
    messages = build_messages(
        model,
        system_message_short["message"]["content"],
        new_user_content=user_message["message"]["content"],
        fallback_to_default=True,
    )
    assert messages == [system_message_short["message"], user_message["message"]]
    assert count_tokens_for_message(model, messages[0], default_to_cl100k=True) == system_message_short["count"]
    assert count_tokens_for_message(model, messages[1], default_to_cl100k=True) == user_message["count"]


def test_messagebuilder_pastmessages():
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_short["message"]["content"],  # 12 tokens
        past_messages=[
            user_message_perf["message"],  # 14 tokens
            assistant_message_perf["message"],  # 106 tokens
        ],
        new_user_content=user_message_pm["message"]["content"],  # 14 tokens
        max_tokens=3000,
    )
    assert messages == [
        system_message_short["message"],
        user_message_perf["message"],
        assistant_message_perf["message"],
        user_message_pm["message"],
    ]


def test_messagebuilder_pastmessages_truncated():
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_short["message"]["content"],  # 12 tokens
        past_messages=[
            user_message_perf["message"],  # 14 tokens
            assistant_message_perf["message"],  # 106 tokens
        ],
        new_user_content=user_message_pm["message"]["content"],  # 14 tokens
        max_tokens=10,
    )
    assert messages == [system_message_short["message"], user_message_pm["message"]]


def test_messagebuilder_pastmessages_truncated_longer():
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_short["message"]["content"],  # 12 tokens
        past_messages=[
            user_message_perf["message"],  # 14 tokens
            assistant_message_perf["message"],  # 106 tokens
            user_message_dresscode["message"],  # 13 tokens
            assistant_message_dresscode["message"],  # 30 tokens
        ],
        new_user_content=user_message_pm["message"]["content"],  # 14 tokens
        max_tokens=69,
    )
    assert messages == [
        system_message_short["message"],
        user_message_dresscode["message"],
        assistant_message_dresscode["message"],
        user_message_pm["message"],
    ]


def test_messagebuilder_pastmessages_truncated_break_pair():
    """Tests that the truncation breaks the pair of messages."""
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_short["message"]["content"],  # 12 tokens
        past_messages=[
            user_message_perf["message"],  # 14 tokens
            assistant_message_perf_short["message"],  # 91 tokens
            user_message_dresscode["message"],  # 13 tokens
            assistant_message_dresscode["message"],  # 30 tokens
        ],
        new_user_content=user_message_pm["message"]["content"],  # 14 tokens
        max_tokens=160,
    )
    assert messages == [
        system_message_short["message"],
        assistant_message_perf_short["message"],
        user_message_dresscode["message"],
        assistant_message_dresscode["message"],
        user_message_pm["message"],
    ]


def test_messagebuilder_system():
    """Tests that the system message token count is considered."""
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_long["message"]["content"],  # 31 tokens
        past_messages=[
            user_message_perf["message"],  # 14 tokens
            assistant_message_perf["message"],  # 106 tokens
            user_message_dresscode["message"],  # 13 tokens
            assistant_message_dresscode["message"],  # 30 tokens
        ],
        new_user_content=user_message_pm["message"]["content"],  # 14 tokens
        max_tokens=36,
    )
    assert messages == [system_message_long["message"], user_message_pm["message"]]


def test_messagebuilder_system_fewshots():
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_short["message"]["content"],
        new_user_content=user_message_pm["message"]["content"],
        past_messages=[],
        few_shots=[
            {"role": "user", "content": "How did crypto do last year?"},
            {"role": "assistant", "content": "Summarize Cryptocurrency Market Dynamics from last year"},
            {"role": "user", "content": "What are my health plans?"},
            {"role": "assistant", "content": "Show available health plans"},
        ],
    )
    # Make sure messages are in the right order
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"
    assert messages[3]["role"] == "user"
    assert messages[4]["role"] == "assistant"
    assert messages[5]["role"] == "user"
    assert messages[5]["content"] == user_message_pm["message"]["content"]


def test_messagebuilder_system_fewshotstools():
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=system_message_short["message"]["content"],
        new_user_content=user_message_pm["message"]["content"],
        past_messages=[],
        few_shots=[
            {"role": "user", "content": "good options for climbing gear that can be used outside?"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_abc123",
                        "type": "function",
                        "function": {
                            "arguments": '{"search_query":"climbing gear outside"}',
                            "name": "search_database",
                        },
                    }
                ],
            },
            {
                "role": "tool",
                "tool_call_id": "call_abc123",
                "content": "Search results for climbing gear that can be used outside: ...",
            },
            {"role": "user", "content": "are there any shoes less than $50?"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_abc456",
                        "type": "function",
                        "function": {
                            "arguments": '{"search_query":"shoes","price_filter":{"comparison_operator":"<","value":50}}',
                            "name": "search_database",
                        },
                    }
                ],
            },
            {"role": "tool", "tool_call_id": "call_abc456", "content": "Search results for shoes cheaper than 50: ..."},
        ],
    )
    # Make sure messages are in the right order
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"
    assert messages[3]["role"] == "tool"
    assert messages[4]["role"] == "user"
    assert messages[5]["role"] == "assistant"
    assert messages[6]["role"] == "tool"
    assert messages[7]["role"] == "user"
    assert messages[7]["content"] == user_message_pm["message"]["content"]


def test_messagebuilder_system_tools():
    """Tests that the system message token count is considered."""
    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt=search_sources_toolchoice_auto["system_message"]["content"],
        tools=search_sources_toolchoice_auto["tools"],
        tool_choice=search_sources_toolchoice_auto["tool_choice"],
        # 66 tokens for system + tools + tool_choice ^
        past_messages=[
            user_message_perf["message"],  # 14 tokens
            assistant_message_perf["message"],  # 106 tokens
        ],
        new_user_content=user_message_pm["message"]["content"],  # 14 tokens
        max_tokens=90,
    )
    assert messages == [search_sources_toolchoice_auto["system_message"], user_message_pm["message"]]


def test_messagebuilder_typing() -> None:
    tools: list[ChatCompletionToolParam] = [
        {
            "type": "function",
            "function": {
                "name": "search_sources",
                "description": "Retrieve sources from the Azure AI Search index",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "Query string to retrieve documents from azure search eg: 'Health care plan'",
                        }
                    },
                    "required": ["search_query"],
                },
            },
        }
    ]
    tool_choice: ChatCompletionToolChoiceOptionParam = {
        "type": "function",
        "function": {"name": "search_sources"},
    }

    past_messages: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "What are my health plans?"},
        {"role": "assistant", "content": "Here are some tools you can use to search for sources."},
    ]

    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt="Here are some tools you can use to search for sources.",
        tools=tools,
        tool_choice=tool_choice,
        past_messages=past_messages,
        new_user_content="What are my health plans?",
        max_tokens=90,
    )

    assert isinstance(messages, list)
    if hasattr(typing, "assert_type"):
        typing.assert_type(messages[0], ChatCompletionMessageParam)

    messages = build_messages(
        model="gpt-35-turbo",
        system_prompt="Here are some tools you can use to search for sources.",
        tools=tools,
        tool_choice="auto",
        past_messages=past_messages,
        new_user_content="What are my health plans?",
        max_tokens=90,
    )

    assert isinstance(messages, list)
    if hasattr(typing, "assert_type"):
        typing.assert_type(messages[0], ChatCompletionMessageParam)
