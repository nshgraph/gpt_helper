# GPTHelper

This is a simple slack bot that allows users to include ChatGPT in their Slack conversations.

When running locally it can be used as a websocket based app. When deployed it must be a webhook based app.

# Local development
## Setup
There is a script for creating a virtualenv with all required packages
'''
./setup.sh
'''


## Running as a local server
'''
source env/bin/activate
python app.py
'''

This will run a local websocket app (and the slack app must be websocket app)


# Deployment
This uses serverless to deploy an AWS lambda based webhook based slack app. It only requires permissions to invoke itself (a way to get around the fact that Slack expects a response in 3s but GPT takes longer).

There is a script `push.sh` that pre-supposes that there is an aws profile named staging with the permissions necessary to create and deploy a lambda.


# Environment variables
## OpenAI API Key
Your OpenAI API key must be in an environment variable named `CONFIG_OPENAI_KEY` OR in a AWS Systems Manager secret of the same name. 

## Slack Keys
Your Slack app/bot details need to be in environment variables OR in AWS System Manager secrets:
* `CONFIG_GPT3PO_SLACK_APP_TOKEN`: The slack app token
* `CONFIG_GPT3PO_SLACK_BOT_TOKEN`: The slack bot token
* `CONFIG_GPT3PO_SLACK_SIGNING`: The slack signing secret