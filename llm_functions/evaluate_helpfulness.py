from utils.llm import call_openai


def evaluate_helpfulness(thread_messages):

    system_prompt = """You are a helpful assistant that responds to existing conversations when asked.
You are provided with the entire thread of conversation.

Before answering you must decide if you are the right person to help. 
You must reply to the messages with a number between 0 and 1.
If no help is required you should return 0.0
If you can definitely help you should return 1.0
No other information should be returned.
"""

    messages = [
        {"role": "system", "content": system_prompt},
    ] + [{"role": message[0], "content": message[1]} for message in thread_messages]

    response = call_openai("gpt-3.5-turbo", messages)

    try:
        result = float(response)
        return result
    except:
        # any erroneous output should be treated as a no
        return 0
