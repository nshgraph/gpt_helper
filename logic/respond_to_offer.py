import logging

from utils.slack_functions import get_message_from_reference, remove_message
from actions.help import respond_with_help

log = logging.getLogger()


def respond_to_offer(app, action, say):
    channel, ts = action.get("value").split(":")

    message = get_message_from_reference(app, channel, ts)
    message["channel"] = channel
    respond_with_help(app, say, message)
