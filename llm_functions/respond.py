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
                        "description": "The body of the ticket. This should include as much detail from the conversation as possible, provided it is is relevant to the issue",
                    },
                },
                "required": ["project", "taskType", "summary", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "comment_on_jira_issue",
            "description": "Comment on an existing jira issue",
            "parameters": {
                "type": "object",
                "properties": {
                    "issueKey": {
                        "type": "string",
                        "description": "The existing Jira ticket key. This will need to be a valid Jira ticket key taken from the conversation. The format is usually PORTAL-1234 or CUST-1234 or THEMES-1234.",
                    },
                    "comment": {
                        "type": "string",
                        "description": "The comment to add",
                    },
                },
                "required": ["issueKey", "comment"],
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
            if tool_call["function"]["name"] in {"create_jira_ticket", "comment_on_jira_issue"}:
                try:
                    tool_call["function"]["arguments"] = json.loads(
                        tool_call["function"]["arguments"]
                    )
                except:
                    raise ValueError("Failed to parse arguments for {}".format(tool_call["function"]["name"]))
                response = ""
                functions = tool_call["function"]
    else:
        response = response["content"]
        functions = None
    return response, functions
