import json
from utils.llm import call_openai


tools = [
    {
        "type": "function",
        "function": {
            "name": "create_jira_ticket",
            "description": "Create a jira ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "enum": ["PORTAL", "CUST", "THEMES"],
                        "description": "The Jira project. Use PORTAL for anything related to the product and if unsure. Use CUST for customer specific tasks or THEMES for R&D tasks",
                    },
                    "taskType": {"type": "string", "enum": ["Task", "Bug"]},
                    "summary": {
                        "type": "string",
                        "description": "The title of the ticket",
                    },
                    "description": {
                        "type": "string",
                        "description": "The body of the ticket",
                    },
                },
                "required": ["project", "taskType", "summary", "description"],
            },
        },
    }
]


def get_response_to_messages(gpt_model, thread_messages):
    system_prompt = """You are a helpful assistant that responds to existing conversations when asked. You are provided with the entire thread of conversation."""

    messages = [
        {"role": "system", "content": system_prompt},
    ] + [{"role": message[0], "content": message[1]} for message in thread_messages]

    response = call_openai(gpt_model, messages, tools=tools)

    functions = None
    if response.get("tool_calls"):
        for tool_call in response["tool_calls"]:
            if tool_call["function"]["name"] == "create_jira_ticket":
                try:
                    tool_call["function"]["arguments"] = json.loads(
                        tool_call["function"]["arguments"]
                    )
                except:
                    raise ValueError("Failed to parse arguments for create_jira_ticket")
                response = ""
                functions = tool_call["function"]
    else:
        response = response["content"]
        functions = None
    return response, functions
