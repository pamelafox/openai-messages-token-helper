text_message = {
    "message": {
        # 1 token : 1 token
        "role": "user",
        # 1 token : 5 tokens
        "content": "Hello, how are you?",
    },
    "count": 13,
}

system_message = {
    "message": {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    "count": 25,
}

system_message_with_name = {
    "message": {
        "role": "system",
        "name": "example_user",
        "content": "New synergies will help drive top-line growth.",
    },
    "count": 20,  # Less tokens in older vision preview models
}

text_and_image_message = {
    "message": {
        # 1 token : 1 token
        "role": "user",
        # 1 token : 262 tokens
        "content": [
            {"type": "text", "text": "Describe this picture:"},  # 1 token  # 4 tokens
            {
                "type": "image_url",  # 2 tokens
                "image_url": {
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",  # 255 tokens
                    "detail": "auto",
                },
            },
        ],
    },
    "count": 266,
}
