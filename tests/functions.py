search_sources_toolchoice_auto = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
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
    ],
    "tool_choice": "auto",
    "count": 66,
}

search_sources_toolchoice_none = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
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
    ],
    "tool_choice": "none",
    "count": 67,
}

search_sources_toolchoice_name = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
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
    ],
    "tool_choice": {"type": "function", "function": {"name": "search_sources"}},
    "count": 75,
}

integer_enum = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "data_demonstration",
                "description": "This is the main function description",
                "parameters": {"type": "object", "properties": {"integer_enum": {"type": "integer", "enum": [-1, 1]}}},
            },
        }
    ],
    "tool_choice": "none",
    "count": 54,
}


integer_enum_tool_choice_name = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "data_demonstration",
                "description": "This is the main function description",
                "parameters": {"type": "object", "properties": {"integer_enum": {"type": "integer", "enum": [-1, 1]}}},
            },
        }
    ],
    "tool_choice": {
        "type": "function",
        "function": {"name": "data_demonstration"},
    },  # 4 tokens for "data_demonstration"
    "count": 64,
}

no_parameters = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "search_sources",
                "description": "Retrieve sources from the Azure AI Search index",
            },
        }
    ],
    "tool_choice": "auto",
    "count": 42,
}

no_parameters_tool_choice_name = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "search_sources",
                "description": "Retrieve sources from the Azure AI Search index",
            },
        }
    ],
    "tool_choice": {"type": "function", "function": {"name": "search_sources"}},  # 2 tokens for "search_sources"
    "count": 51,
}

no_parameter_description_or_required = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "search_sources",
                "description": "Retrieve sources from the Azure AI Search index",
                "parameters": {"type": "object", "properties": {"search_query": {"type": "string"}}},
            },
        }
    ],
    "tool_choice": "auto",
    "count": 49,
}

no_parameter_description = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "search_sources",
                "description": "Retrieve sources from the Azure AI Search index",
                "parameters": {
                    "type": "object",
                    "properties": {"search_query": {"type": "string"}},
                    "required": ["search_query"],
                },
            },
        }
    ],
    "tool_choice": "auto",
    "count": 49,
}

string_enum = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "summarize_order",
                "description": "Summarize the customer order request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "Product name ordered by customer",
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity ordered by customer",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["meals", "days"],
                            "description": "unit of measurement of the customer order",
                        },
                    },
                    "required": ["product_name", "quantity", "unit"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 86,
}

inner_object = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "data_demonstration",
                "description": "This is the main function description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_1": {
                            "type": "object",
                            "description": "The object data type as a property",
                            "properties": {
                                "string1": {"type": "string"},
                            },
                        }
                    },
                    "required": ["object_1"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 65,  # counted 67, over by 2
}
"""
namespace functions {

// This is the main function description
type data_demonstration = (_: {
// The object data type as a property
object_1: {
  string1?: string,
},
}) => any;

} // namespace functions
"""

inner_object_with_enum_only = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "data_demonstration",
                "description": "This is the main function description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_1": {
                            "type": "object",
                            "description": "The object data type as a property",
                            "properties": {"string_2a": {"type": "string", "enum": ["Happy", "Sad"]}},
                        }
                    },
                    "required": ["object_1"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 73,  # counted 74, over by 1
}
"""
namespace functions {

// This is the main function description
type data_demonstration = (_: {
// The object data type as a property
object_1: {
  string_2a?: "Happy" | "Sad",
},
}) => any;

} // namespace functions
"""

inner_object_with_enum = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "data_demonstration",
                "description": "This is the main function description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_1": {
                            "type": "object",
                            "description": "The object data type as a property",
                            "properties": {
                                "string_2a": {"type": "string", "enum": ["Happy", "Sad"]},
                                "string_2b": {
                                    "type": "string",
                                    "description": "Description in a second object is lost",
                                },
                            },
                        }
                    },
                    "required": ["object_1"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 89,  # counted 92, over by 3
}
"""
namespace functions {

// This is the main function description
type data_demonstration = (_: {
// The object data type as a property
object_1: {
  string_2a?: "Happy" | "Sad",
  // Description in a second object is lost
  string_2b?: string,
},
}) => any;

} // namespace functions
"""

inner_object_and_string = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "data_demonstration",
                "description": "This is the main function description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_1": {
                            "type": "object",
                            "description": "The object data type as a property",
                            "properties": {
                                "string_2a": {"type": "string", "enum": ["Happy", "Sad"]},
                                "string_2b": {
                                    "type": "string",
                                    "description": "Description in a second object is lost",
                                },
                            },
                        },
                        "string_1": {"type": "string", "description": "Not required gets a question mark"},
                    },
                    "required": ["object_1"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 103,  # counted 106, over by 3
}
"""
namespace functions {

// This is the main function description
type data_demonstration = (_: {
// The object data type as a property
object_1: {
  string_2a?: "Happy" | "Sad",
  // Description in a second object is lost
  string_2b?: string,
},
// Not required gets a question mark
string_1?: string,
}) => any;

} // namespace functions
"""

boolean = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "human_escalation",
                "description": "Check if user wants to escalate to a human",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requires_escalation": {
                            "type": "boolean",
                            "description": "If user is showing signs of frustration or anger in the query. Also if the user says they want to talk to a real person and not a chat bot.",
                        }
                    },
                    "required": ["requires_escalation"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 89,  # over by 3
}

array = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_coordinates",
                "description": "Get the latitude and longitude of multiple mailing addresses",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "addresses": {
                            "type": "array",
                            "description": "The mailing addresses to be located",
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["addresses"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 59,
}

null = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_null",
                "description": "Get the null value",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "null_value": {
                            "type": "null",
                            "description": "The null value to be returned",
                        }
                    },
                    "required": ["null_value"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 55,
}

no_type = {
    "system_message": {
        "role": "system",
        "content": "You are a bot.",
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_no_type",
                "description": "Get the no type value",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "no_type_value": {
                            "description": "The no type value to be returned",
                        }
                    },
                    "required": ["no_type_value"],
                },
            },
        }
    ],
    "tool_choice": "none",
    "count": 59,
}

FUNCTION_COUNTS = [
    inner_object,
    inner_object_and_string,
    inner_object_with_enum_only,
    inner_object_with_enum,
    search_sources_toolchoice_auto,
    search_sources_toolchoice_none,
    search_sources_toolchoice_name,
    integer_enum,
    integer_enum_tool_choice_name,
    no_parameters,
    no_parameters_tool_choice_name,
    no_parameter_description_or_required,
    no_parameter_description,
    string_enum,
    boolean,
    array,
    no_type,
    null,
]
