from enum import Enum
from utils import config
import logging

from llm_functions.evaluate_helpfulness import evaluate_helpfulness
from utils.slack_functions import (
    message_is_in_thread,
    is_bot_part_of_thread,
    get_context_messages,
)

log = logging.getLogger()


class Actions(Enum):
    Respond = "Respond"
    Offer = "Offer"
    Ignore = "Ignore"


def determine_action(app, event):
    # determine if this is a direct message
    if event.get("type") == "app_mention":
        log.info("Responding: app mention")
        return Actions.Respond
    # determine if it is from a bot (never respond to bots)
    if event.get("subtype") == "bot_message" or event.get("bot_id") is not None:
        log.info("Ignoring: bot message")
        return Actions.Ignore
    # ignore anything not messages
    if event.get("type") != "message":
        log.info("Ignoring: not a message")
        return Actions.Ignore
    elif event.get("subtype") in {
        "channel_join",
        "channel_leave",
        "message_deleted",
        "message_changed",
    }:
        log.info("Ignoring: not just a message")
        return Actions.Ignore

    # if this is a message in a thread and the bot hasn't been involved we ignore
    is_thread = message_is_in_thread(app, event)
    if is_thread:
        # bot_in_thread = is_bot_part_of_thread(app, event)
        # if not bot_in_thread:
        #     log.info("Ignoring: bot not in thread")
        return Actions.Ignore

    # we haven't been mentioned, but maybe we could still help
    helpful_threshold = config["HELPFUL_THRESHOLD"]
    thread_messages = get_context_messages(app, event)
    could_be_helpful = evaluate_helpfulness(thread_messages)
    log.info("Could be helpful: {}".format(could_be_helpful))
    if could_be_helpful > helpful_threshold:
        log.info("Offering: {}/{}".format(could_be_helpful, helpful_threshold))
        return Actions.Offer
    log.info("Ignoring: not helpful enough")
    return Actions.Ignore
