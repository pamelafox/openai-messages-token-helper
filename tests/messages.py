user_message = {
    "message": {
        "role": "user",
        "content": "Hello, how are you?",
    },
    "count": 13,
}

user_message_unicode = {
    "message": {
        "role": "user",
        "content": "á",
    },
    "count": 8,
}

system_message_short = {
    "message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "count": 12,
}

system_message = {
    "message": {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    "count": 25,
}

system_message_unicode = {
    "message": {
        "role": "system",
        "content": "á",
    },
    "count": 8,
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
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this picture:"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",
                    "detail": "auto",
                },
            },
        ],
    },
    "count": 266,
}
