import json
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from logic.determine import Actions, determine_action
from actions.help import respond_with_help
from actions.offer import handle_offer

from utils import config

log = logging.getLogger()


# Install the Slack app and get xoxb- token in advance
app = App(
    process_before_response=True,
    token=config["SLACK_BOT_TOKEN"],
    signing_secret=config["SLACK_SIGNING_SECRET"],
)


def respond_to_slack_within_3_seconds(body, ack):
    ack(f"Accepted!")


def handle_message(say, event):

    # otherwise we have to evaluate this message

    action = determine_action(app, event)
    if action == Actions.Respond:
        respond_with_help(say, event)
    elif action == Actions.Offer:
        handle_offer(say, event)

    # default is to do nothing


app.event("app_mention")(ack=respond_to_slack_within_3_seconds, lazy=[handle_message])
app.event("message")(ack=respond_to_slack_within_3_seconds, lazy=[handle_message])


if __name__ == "__main__":
    SocketModeHandler(app, config["SLACK_APP_TOKEN"]).start()

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context):
    print(event)
    slack_handler = SlackRequestHandler(app=app)
    res = slack_handler.handle(event, context)
    return res
