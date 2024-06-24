from .ssm import get_ssm_parameter


config = {
    "GPT_KEY": get_ssm_parameter("CONFIG_THEMATIC_GPT3_KEY"),
    "SLACK_APP_TOKEN": get_ssm_parameter("CONFIG_GPT3PO_SLACK_APP_TOKEN"),
    "SLACK_BOT_TOKEN": get_ssm_parameter("CONFIG_GPT3PO_SLACK_BOT_TOKEN"),
    "SLACK_SIGNING_SECRET": get_ssm_parameter("CONFIG_GPT3PO_SLACK_SIGNING"),
    "CONFIG_GPT3PO_ATLASSIAN_PERMISSIONS": get_ssm_parameter(
        "CONFIG_GPT3PO_ATLASSIAN_PERMISSIONS", is_json=True
    ),
    "BOT_USER_ID": "U04V11MGNET",
    "DEBUG_CHANNEL": "D05029Y4F7D",
    "HELPFUL_THRESHOLD": 0.5,
}
