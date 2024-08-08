import os
from typing import Union

import azure.identity
import openai
from dotenv import load_dotenv
from image_messages import IMAGE_MESSAGE_COUNTS  # type: ignore[import-not-found]
from messages import MESSAGE_COUNTS  # type: ignore[import-not-found]

# Setup the OpenAI client to use either Azure OpenAI or OpenAI API
load_dotenv()
API_HOST = os.getenv("API_HOST")

client: Union[openai.OpenAI, openai.AzureOpenAI]

if API_HOST == "azure":
    if (azure_openai_version := os.getenv("AZURE_OPENAI_VERSION")) is None:
        raise ValueError("Missing Azure OpenAI version")
    if (azure_openai_endpoint := os.getenv("AZURE_OPENAI_ENDPOINT")) is None:
        raise ValueError("Missing Azure OpenAI endpoint")
    if (azure_openai_deployment := os.getenv("AZURE_OPENAI_DEPLOYMENT")) is None:
        raise ValueError("Missing Azure OpenAI deployment")

    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=azure_openai_version,
        azure_endpoint=azure_openai_endpoint,
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = azure_openai_deployment
else:
    if (openai_key := os.getenv("OPENAI_KEY")) is None:
        raise ValueError("Missing OpenAI API key")
    if (openai_model := os.getenv("OPENAI_MODEL")) is None:
        raise ValueError("Missing OpenAI model")
    client = openai.OpenAI(api_key=openai_key)
    MODEL_NAME = openai_model

# Test the token count for each message

for message_count_pair in MESSAGE_COUNTS:
    for model, expected_tokens in [("gpt-4o", message_count_pair["count_omni"])]:
        message = message_count_pair["message"]
        expected_tokens = message_count_pair["count"]
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.7,
            n=1,
            messages=[message],  # type: ignore[list-item]
        )

        print(message)
        assert response.usage is not None, "Expected usage to be present"
        assert (
            response.usage.prompt_tokens == expected_tokens
        ), f"Expected {expected_tokens} tokens, got {response.usage.prompt_tokens} for model {MODEL_NAME}"


for message_count_pair in IMAGE_MESSAGE_COUNTS:
    for model, expected_tokens in [
        ("gpt-4o", message_count_pair["count"]),
        ("gpt-4o-mini", message_count_pair["count_4o_mini"]),
    ]:
        response = client.chat.completions.create(
            model=model,
            temperature=0.7,
            n=1,
            messages=[message_count_pair["message"]],  # type: ignore[list-item]
        )

        assert response.usage is not None, "Expected usage to be present"
        assert (
            response.usage.prompt_tokens == expected_tokens
        ), f"Expected {expected_tokens} tokens, got {response.usage.prompt_tokens} for model {model}"
