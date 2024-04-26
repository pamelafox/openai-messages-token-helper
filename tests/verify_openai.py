import os

import azure.identity
import openai
from dotenv import load_dotenv
from messages import MESSAGE_COUNTS

# Setup the OpenAI client to use either Azure OpenAI or OpenAI API
load_dotenv()
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
else:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")

# Test the token count for each message
for message_count_pair in MESSAGE_COUNTS:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        n=1,
        messages=[message_count_pair["message"]],
    )

    print(message_count_pair["message"])
    expected_tokens = message_count_pair["count"]
    assert (
        response.usage.prompt_tokens == expected_tokens
    ), f"Expected {expected_tokens} tokens, got {response.usage.prompt_tokens}"
