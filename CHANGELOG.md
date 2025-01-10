# Changelog

All notable changes to this project will be documented in this file.

## [0.1.11] - Jan 10, 2025

- When no "detail" is provided for an "image_url" message part, "auto" is now assumed.

## [0.1.10] - Aug 7, 2024

- Add additional OpenAI.com model names to the `get_token_limit` function.

## [0.1.9] - Aug 7, 2024

- Add gpt-4o-mini support, by adding a 33.3x multiplier to the token cost.

## [0.1.8] - Aug 3, 2024

- Fix the type for the tool_choice param to be inclusive of "auto" and other options.

## [0.1.7] - Aug 3, 2024

- Fix bug where you couldn't pass in example tool calls in `few_shots` to `build_messages`.

## [0.1.6] - Aug 2, 2024

- Fix bug where you couldn't pass in `tools` and `default_to_cl100k` to True with a non-OpenAI model.

## [0.1.5] - June 4, 2024

- Remove spurious `print` call when counting tokens for function calling.

## [0.1.4] - May 14, 2024

- Add support and tests for gpt-4o, which has a different tokenizer.

## [0.1.3] - May 2, 2024

- Use openai type annotations for more precise type hints, and add a typing test.

## [0.1.2] - May 2, 2024

- Add `py.typed` file so that mypy can find the type hints in this package.

## [0.1.0] - May 2, 2024

- Add `count_tokens_for_system_and_tools` to count tokens for system message and tools. You should count the tokens for both together, since the token count for tools varies based off whether a system message is provided.
- Updated `build_messages` to allow for `tools` and `tool_choice` to be passed in.
- Breaking change: Changed `new_user_message` to `new_user_content` in `build_messages` for clarity.

## [0.0.6] - April 24, 2024

- Add keyword argument `fallback_to_default` to `build_messages` function to allow for defaulting to the CL100k token encoder and minimum GPT token limit if the model is not found.
- Fixed usage of `past_messages` argument of `build_messages` to not skip the last past message. (New user message should *not* be passed in)

## [0.0.5] - April 24, 2024

- Add keyword argument `default_to_cl100k` to `count_tokens_for_message` function to allow for defaulting to the CL100k token limit if the model is not found.
- Add keyword argument `default_to_minimum` to `get_token_limit` function to allow for defaulting to the minimum token limit if the model is not found.

## [0.0.4] - April 21, 2024

- Rename to openai-messages-token-helper from llm-messages-token-helper to reflect library's current OpenAI focus.

## [0.0.3] - April 21, 2024

- Fix for `count_tokens_for_message` function to match OpenAI output precisely, particularly for calls with images to GPT-4  vision.
