system_message_short = {
    "message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "count": 12,
    "count_omni": 12,
}

system_message = {
    "message": {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    "count": 25,
    "count_omni": 24,
}

system_message_long = {
    "message": {
        "role": "system",
        "content": "Assistant helps the company employees with their healthcare plan questions, and questions about the employee handbook. Be brief in your answers.",
    },
    "count": 31,
    "count_omni": 31,
}

system_message_unicode = {
    "message": {
        "role": "system",
        "content": "á",
    },
    "count": 8,
    "count_omni": 8,
}

system_message_with_name = {
    "message": {
        "role": "system",
        "name": "example_user",
        "content": "New synergies will help drive top-line growth.",
    },
    "count": 20,  # Less tokens in older vision preview models
    "count_omni": 20,
}

user_message = {
    "message": {
        "role": "user",
        "content": "Hello, how are you?",
    },
    "count": 13,
    "count_omni": 13,
}

user_message_unicode = {
    "message": {
        "role": "user",
        "content": "á",
    },
    "count": 8,
    "count_omni": 8,
}

user_message_perf = {
    "message": {
        "role": "user",
        "content": "What happens in a performance review?",
    },
    "count": 14,
    "count_omni": 14,
}

assistant_message_perf = {
    "message": {
        "role": "assistant",
        "content": "During the performance review at Contoso Electronics, the supervisor will discuss the employee's performance over the past year and provide feedback on areas for improvement. They will also provide an opportunity for the employee to discuss their goals and objectives for the upcoming year. The review is a two-way dialogue between managers and employees, and employees will receive a written summary of their performance review which will include a rating of their performance, feedback, and goals and objectives for the upcoming year [employee_handbook-3.pdf].",
    },
    "count": 106,
    "count_omni": 106,
}

assistant_message_perf_short = {
    "message": {
        "role": "assistant",
        "content": "The supervisor will discuss the employee's performance and provide feedback on areas for improvement. They will also provide an opportunity for the employee to discuss their goals and objectives for the upcoming year. The review is a two-way dialogue between managers and employees, and employees will receive a written summary of their performance review which will include a rating of their performance, feedback, and goals for the upcoming year [employee_handbook-3.pdf].",
    },
    "count": 91,
    "count_omni": 91,
}

user_message_dresscode = {
    "message": {
        "role": "user",
        "content": "Is there a dress code?",
    },
    "count": 13,
    "count_omni": 13,
}

assistant_message_dresscode = {
    "message": {
        "role": "assistant",
        "content": "Yes, there is a dress code at Contoso Electronics. Look sharp! [employee_handbook-1.pdf]",
    },
    "count": 30,
    "count_omni": 30,
}
user_message_pm = {
    "message": {
        "role": "user",
        "content": "What does a Product Manager do?",
    },
    "count": 14,
    "count_omni": 14,
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
    "count_omni": 266,
}

MESSAGE_COUNTS = [
    system_message,
    system_message_short,
    system_message_long,
    system_message_unicode,
    system_message_with_name,
    user_message,
    user_message_unicode,
    user_message_perf,
    user_message_dresscode,
    user_message_pm,
    assistant_message_perf,
    assistant_message_perf_short,
    assistant_message_dresscode,
]
