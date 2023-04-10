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

# Usage
In any channel you can mention `@GPTHelper`. The bot will take as context the _thread_ that it has been mentioned in (and only that thread). If a thread hasn't been created, the bot will create a thread and respond. It will only have the initial message as context. This is how you can limit what is 'sent' to GPT and maintain control over data privacy.

User messages in the thread will be treated as individual messages. The bot will respond with `Thinking...` to indicate that it is responding and then replace this message with its response.

If the bot is mentioned multiple times in the same thread its previous responses will be marked as such (so it knows what it 'said' previously).

The bot is also available under 'Apps' where it is not necessary to mention `@GPTHelper` to get a response. 

This will use the GPT3.5 model.

## GPT4
If your OpenAI key allows access to GPT4 it is possible to invoke this model by including `(be special)` in the message. For example `@GPTHelper (be special) what is 2+2?` will invoke GPT4