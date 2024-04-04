import json
import logging
import traceback
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from logic.determine import Actions, determine_action
from logic.respond_to_offer import respond_to_offer
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
    try:
        action = determine_action(app, event)
        if action == Actions.Respond:
            respond_with_help(app, say, event)
        elif action == Actions.Offer:
            handle_offer(app, say, event)
    except Exception as e:
        log.error("Error: {}\n{}".format(str(e), traceback.format_exc()))
        raise e

    # default is to do nothing


def handle_command(action, say, respond):
    # otherwise we have to evaluate this message
    respond(delete_original=True)
    try:
        if action.get("action_id") == "accept_help_button":
            respond_to_offer(app, action, say)
    except Exception as e:
        log.error("Error: {}\n{}".format(str(e), traceback.format_exc()))
        raise e


app.event("app_mention")(ack=respond_to_slack_within_3_seconds, lazy=[handle_message])
app.event("message")(ack=respond_to_slack_within_3_seconds, lazy=[handle_message])
app.action("accept_help_button")(
    ack=respond_to_slack_within_3_seconds, lazy=[handle_command]
)
app.action("deny_help_button")(
    ack=respond_to_slack_within_3_seconds, lazy=[handle_command]
)


if __name__ == "__main__":
    SocketModeHandler(app, config["SLACK_APP_TOKEN"]).start()

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context):
    body = event.get("body", "{}")
    try:
        log.info("Event Body: {}".format(body))
    except:
        log.info("Event: {}".format(json.dumps(event)))

    slack_handler = SlackRequestHandler(app=app)
    res = slack_handler.handle(event, context)
    return res
