import logging
from utils.slack_functions import get_context_messages
from llm_functions.respond import get_response_to_messages

from actions.thinking import say_thinking, remove_thinking

log = logging.getLogger()


def respond_with_help(app, say, message):
    thread_ts = message.get("thread_ts", message.get("ts"))

    thread_messages = get_context_messages(app, message)

    gpt_model = "gpt-3.5-turbo"

    if "(be special)" in message["text"]:
        gpt_model = "gpt-4"

    thinking_message = say_thinking(say, message, gpt_model)

    try:
        response = get_response_to_messages(gpt_model, thread_messages)
        response = response["content"]
        say(response, thread_ts=thread_ts)
    except Exception as e:
        say("Something went wrong! {}".format(str(e)), thread_ts=thread_ts)

    remove_thinking(app, thinking_message)
