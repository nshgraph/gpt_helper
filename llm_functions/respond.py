from utils.llm import call_openai


def get_response_to_messages(gpt_model, thread_messages):
    system_prompt = """You are a helpful assistant that responds to existing conversations when asked. You are provided with the entire thread of conversation."""

    messages = [
        {"role": "system", "content": system_prompt},
    ] + [{"role": message[0], "content": message[1]} for message in thread_messages]

    response = call_openai(gpt_model, messages)
    response = response["content"]

    return response
