import logging
import unicodedata
from collections.abc import Mapping
from typing import Optional, Union

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from .model_helper import count_tokens_for_message, get_token_limit


class MessageBuilder:
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

    def __init__(self, system_content: str, chatgpt_model: str):
        self.messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(role="system", content=unicodedata.normalize("NFC", system_content))
        ]
        self.model = chatgpt_model

    def insert_message(self, role: str, content: Union[str, list[ChatCompletionContentPartParam]], index: int = 1):
        """
        Inserts a message into the conversation at the specified index,
        or at index 1 (after system message) if no index is specified.
        Args:
            role (str): The role of the message sender (either "user", "system", or "assistant").
            content (str | List[ChatCompletionContentPartParam]): The content of the message.
            index (int): The index at which to insert the message.
        """
        message: ChatCompletionMessageParam
        if role == "user":
            message = ChatCompletionUserMessageParam(role="user", content=self.normalize_content(content))
        elif role == "assistant" and isinstance(content, str):
            message = ChatCompletionAssistantMessageParam(
                role="assistant", content=unicodedata.normalize("NFC", content)
            )
        else:
            raise ValueError(f"Invalid role: {role}")
        self.messages.insert(index, message)

    def count_tokens_for_message(self, message: Mapping[str, object]):
        return count_tokens_for_message(self.model, message)

    def normalize_content(self, content: Union[str, list[ChatCompletionContentPartParam]]):
        if isinstance(content, str):
            return unicodedata.normalize("NFC", content)
        elif isinstance(content, list):
            for part in content:
                if "image_url" not in part:
                    part["text"] = unicodedata.normalize("NFC", part["text"])
            return content


def build_messages(
    model: str,
    system_prompt: str,
    new_user_message: Union[str, list[ChatCompletionContentPartParam], None] = None,  # list is for GPT4v usage
    past_messages: list[dict[str, str]] = [],  # *not* including system prompt
    few_shots=[],  # will always be inserted after system prompt
    max_tokens: Optional[int] = None,
) -> list[ChatCompletionMessageParam]:
    """
    Build a list of messages for a chat conversation, given the system prompt, new user message,
    and past messages. The function will truncate the history of past messages if necessary to
    stay within the token limit.
    Args:
        model (str): The model name to use for token calculation, like gpt-3.5-turbo.
        system_prompt (str): The initial system prompt message.
        new_user_message (str | List[ChatCompletionContentPartParam]): The new user message to append.
        past_messages (list[dict]): The list of past messages in the conversation.
        few_shots (list[dict]): A few-shot list of messages to insert after the system prompt.
        max_tokens (int): The maximum number of tokens allowed for the conversation.
    """
    message_builder = MessageBuilder(system_prompt, model)
    if max_tokens is None:
        max_tokens = get_token_limit(model)

    for shot in reversed(few_shots):
        message_builder.insert_message(shot.get("role"), shot.get("content"))

    append_index = len(few_shots) + 1

    if new_user_message:
        message_builder.insert_message("user", new_user_message, index=append_index)

    total_token_count = 0
    for existing_message in message_builder.messages:
        total_token_count += message_builder.count_tokens_for_message(existing_message)

    newest_to_oldest = list(reversed(past_messages[:-1]))
    for message in newest_to_oldest:
        potential_message_count = message_builder.count_tokens_for_message(message)
        if (total_token_count + potential_message_count) > max_tokens:
            logging.info("Reached max tokens of %d, history will be truncated", max_tokens)
            break
        message_builder.insert_message(message["role"], message["content"], index=append_index)
        total_token_count += potential_message_count
    return message_builder.messages
