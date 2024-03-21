from enum import Enum
from utils import config

from llm_functions.evaluate_helpfulness import evaluate_helpfulness
from utils.slack_functions import (
    message_is_in_thread,
    is_bot_part_of_thread,
    get_context_messages,
)


class Actions(Enum):
    Respond = "Respond"
    Offer = "Offer"
    Ignore = "Ignore"


def determine_action(app, event):
    # determine if this is a direct message
    if event.get("type") == "app_mention":
        return Actions.Respond
    # determine if it is from a bot (never respond to bots)
    if event.get("subtype") == "bot_message":
        return Actions.Ignore

    # if this is a message in a thread and the bot hasn't been involved we ignore
    is_thread = message_is_in_thread(app, event)
    if is_thread:
        bot_in_thread = is_bot_part_of_thread(app, event)
        if not bot_in_thread:
            return Actions.Ignore

    # we haven't been mentioned, but maybe we could still help
    helpful_threshold = config["HELPFUL_THRESHOLD"]
    thread_messages = get_context_messages(app, event)
    could_be_helpful = evaluate_helpfulness(thread_messages)
    if could_be_helpful > helpful_threshold:
        return Actions.Offer

    return Actions.Ignore
