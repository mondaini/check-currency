from os import getenv
from flask import Flask
from flask import request
from requests import get
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from decimal import Decimal

EXCHANGE_API_KEY = getenv('EXCHANGE_API_KEY')
SLACK_SIGNING_SECRET = getenv('SLACK_SIGNING_SECRET')
SLACK_BOT_TOKEN = getenv("SLACK_BOT_TOKEN")

app = Flask(__name__)
slack_client = WebClient(SLACK_BOT_TOKEN)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

MESSAGE = """:dollar::dollar::dollar:

:flag-br: = {:.2f}
:husky: = {:.2f} (2,5%)
"""


@slack_events_adapter.on("message")
def mention(event_data):
    message = event_data["event"]

    rate = Decimal(data.get("rates").get("BRL"))
    husky = rate * Decimal(0.975)

    if message.get("subtype") is None and "dólar" in message.get('text'):
        data = quote()
        data.get("rates").get("BRL")

        channel = message["channel"]
        message = MESSAGE.format(rate, husky)
        slack_client.chat_postMessage(channel=channel, text=message)
