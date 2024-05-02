import os
from typing import Union

import azure.identity
import openai
from dotenv import load_dotenv
from functions import FUNCTION_COUNTS  # type: ignore[import-not-found]

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
for function_count_pair in FUNCTION_COUNTS:
    response = client.chat.completions.create(  # type: ignore[call-overload]
        model=MODEL_NAME,
        temperature=0.7,
        n=1,
        messages=[function_count_pair["system_message"]],
        tools=function_count_pair["tools"],
        tool_choice=function_count_pair["tool_choice"],
    )

    print(function_count_pair["tools"])
    assert response.usage is not None, "Expected usage to be present"
    assert (
        response.usage.prompt_tokens == function_count_pair["count"]
    ), f"Expected {function_count_pair['count']} tokens, got {response.usage.prompt_tokens}"
