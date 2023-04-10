from .ssm import get_ssm_parameter


config = {
    "GPT_KEY": get_ssm_parameter("CONFIG_OPENAI_KEY"),
    "SLACK_APP_TOKEN": get_ssm_parameter("CONFIG_GPT3PO_SLACK_APP_TOKEN"),
    "SLACK_BOT_TOKEN": get_ssm_parameter("CONFIG_GPT3PO_SLACK_BOT_TOKEN"),
    "SLACK_SIGNING_SECRET": get_ssm_parameter("CONFIG_GPT3PO_SLACK_SIGNING"),
}