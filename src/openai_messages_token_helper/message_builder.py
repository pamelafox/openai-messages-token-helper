import logging
import unicodedata
from collections.abc import Iterable
from typing import Optional, Union

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionRole,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
    ChatCompletionUserMessageParam,
)

from .model_helper import count_tokens_for_message, count_tokens_for_system_and_tools, get_token_limit


def normalize_content(content: Union[str, Iterable[ChatCompletionContentPartParam], None]):
    if content is None:
        return None
    if isinstance(content, str):
        return unicodedata.normalize("NFC", content)
    else:
        for part in content:
            if part["type"] == "text":
                part["text"] = unicodedata.normalize("NFC", part["text"])
        return content


class _MessageBuilder:
    """
    A class for building and managing messages in a chat conversation.
    Attributes:
        message (list): A list of dictionaries representing chat messages.
        model (str): The name of the ChatGPT model.
        token_count (int): The total number of tokens in the conversation.
    Methods:
        __init__(self, system_content: str, chatgpt_model: str): Initializes the MessageBuilder instance.
        insert_message(self, role: str, content: str, index: int = 1): Inserts a new message to the conversation.
    """

    def __init__(self, system_content: str):
        self.system_message = ChatCompletionSystemMessageParam(role="system", content=normalize_content(system_content))
        self.messages: list[ChatCompletionMessageParam] = []

    @property
    def all_messages(self) -> list[ChatCompletionMessageParam]:
        return [self.system_message] + self.messages

    def insert_message(
        self,
        role: ChatCompletionRole,
        content: Union[str, Iterable[ChatCompletionContentPartParam], None],
        index: int = 0,
        tool_calls: Optional[Iterable[ChatCompletionMessageToolCallParam]] = None,
        tool_call_id: Optional[str] = None,
    ):
        """
        Inserts a message into the conversation at the specified index,
        or at index 0 if no index is specified.
        Args:
            role (str): The role of the message sender (either "user", "system", or "assistant").
            content (str | List[ChatCompletionContentPartParam]): The content of the message.
            index (int): The index at which to insert the message.
        """
        message: ChatCompletionMessageParam
        if role == "user":
            message = ChatCompletionUserMessageParam(role="user", content=normalize_content(content))
        elif role == "assistant" and isinstance(content, str):
            message = ChatCompletionAssistantMessageParam(role="assistant", content=normalize_content(content))
        elif role == "assistant" and tool_calls is not None:
            message = ChatCompletionAssistantMessageParam(role="assistant", tool_calls=tool_calls)
        elif role == "tool" and tool_call_id is not None:
            message = ChatCompletionToolMessageParam(
                role="tool", tool_call_id=tool_call_id, content=normalize_content(content)
            )
        else:
            raise ValueError("Invalid message for builder")
        self.messages.insert(index, message)


def build_messages(
    model: str,
    system_prompt: str,
    *,
    tools: Optional[list[ChatCompletionToolParam]] = None,
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
    new_user_content: Union[str, list[ChatCompletionContentPartParam], None] = None,  # list is for GPT4v usage
    past_messages: list[ChatCompletionMessageParam] = [],  # *not* including system prompt
    few_shots: list[ChatCompletionMessageParam] = [],  # will always be inserted after system prompt
    max_tokens: Optional[int] = None,
    fallback_to_default: bool = False,
) -> list[ChatCompletionMessageParam]:
    """
    Build a list of messages for a chat conversation, given the system prompt, new user message,
    and past messages. The function will truncate the history of past messages if necessary to
    stay within the token limit.
    Args:
        model (str): The model name to use for token calculation, like gpt-3.5-turbo.
        system_prompt (str): The initial system prompt message.
        tools (list[ChatCompletionToolParam]): A list of tools to include in the conversation.
        tool_choice (ChatCompletionToolChoiceOptionParam): The tool to use in the conversation.
        new_user_content (str | List[ChatCompletionContentPartParam]): Content of new user message to append.
        past_messages (list[ChatCompletionMessageParam]): The list of past messages in the conversation.
        few_shots (list[ChatCompletionMessageParam]): A few-shot list of messages to insert after the system prompt.
        max_tokens (int): The maximum number of tokens allowed for the conversation.
        fallback_to_default (bool): Whether to fallback to default model if the model is not found.
    """
    if max_tokens is None:
        max_tokens = get_token_limit(model, default_to_minimum=fallback_to_default)

    # Start with the required messages: system prompt, few-shots, and new user message
    message_builder = _MessageBuilder(system_prompt)

    for shot in reversed(few_shots):
        if shot["role"] is None or (shot.get("content") is None and shot.get("tool_calls") is None):
            raise ValueError("Few-shot messages must have role and either content or tool_calls")
        tool_call_id = shot.get("tool_call_id")
        if tool_call_id is not None and not isinstance(tool_call_id, str):
            raise ValueError("tool_call_id must be a string value")
        tool_calls = shot.get("tool_calls")
        if tool_calls is not None and not isinstance(tool_calls, Iterable):
            raise ValueError("tool_calls must be a list of tool calls")
        message_builder.insert_message(
            shot["role"], shot.get("content"), tool_calls=tool_calls, tool_call_id=tool_call_id  # type: ignore[arg-type]
        )

    append_index = len(few_shots)

    if new_user_content:
        message_builder.insert_message("user", new_user_content, index=append_index)

    total_token_count = count_tokens_for_system_and_tools(
        model, message_builder.system_message, tools, tool_choice, default_to_cl100k=fallback_to_default
    )
    for existing_message in message_builder.messages:
        total_token_count += count_tokens_for_message(model, existing_message, default_to_cl100k=fallback_to_default)

    newest_to_oldest = list(reversed(past_messages))
    for message in newest_to_oldest:
        potential_message_count = count_tokens_for_message(model, message, default_to_cl100k=fallback_to_default)
        if (total_token_count + potential_message_count) > max_tokens:
            logging.info("Reached max tokens of %d, history will be truncated", max_tokens)
            break

        if message["role"] is None or message["content"] is None:
            raise ValueError("Few-shot messages must have both role and content")
        message_builder.insert_message(message["role"], message["content"], index=append_index)  # type: ignore[arg-type]
        total_token_count += potential_message_count
    return message_builder.all_messages
