from utils.llm import call_openai


def evaluate_helpfulness(thread_messages):
    # First we check if the message starts with an emoji. We don't offer to help for these
    if thread_messages[0][1].startswith(":"):
        return 0

    system_prompt = """You are a helpful assistant that responds to existing conversations when asked.
Before answering you must decide if you are the right person to help. 
You do not have access to calendars, internal documents or any other company specific information. The help would come from what you already know about development and the world.

You must reply to the messages with a number between 0 and 1.
If no help is required you should return 0.0
If you can definitely help you should return 1.0
No other information should be returned.
"""

    messages = [
        {"role": "system", "content": system_prompt},
    ] + [{"role": message[0], "content": message[1]} for message in thread_messages]

    response = call_openai("gpt-3.5-turbo", messages)
    response = response["content"]

    try:
        result = float(response)
        return result
    except:
        # any erroneous output should be treated as a no
        return 0
