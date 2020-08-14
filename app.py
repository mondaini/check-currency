from os import getenv
from flask import Flask
from flask import request
from requests import get
from slackeventsapi import SlackEventAdapter
from slack import WebClient

EXCHANGE_API_KEY = getenv('EXCHANGE_API_KEY')
SLACK_SIGNING_SECRET = getenv('SLACK_SIGNING_SECRET')
SLACK_BOT_TOKEN = getenv("SLACK_BOT_TOKEN")

app = Flask(__name__)
slack_client = WebClient(SLACK_BOT_TOKEN)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/quote', methods=['GET', 'POST'])
def quote():
    url = "https://openexchangerates.org/api/latest.json?app_id={}&symbols=BRL&prettyprint=true".format(EXCHANGE_API_KEY)

    response = get(url)

    return response.json()


slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

@slack_events_adapter.on("message")
def mention(event_data):
    data = quote()
    data.get("rates").get("BRL")
    message = event_data["event"]

    if message.get("subtype") is None and "Dólar" in message.get('text'):
        channel = message["channel"]
        message = ":money: %s" % data.get("rates").get("BRL")
        slack_client.chat_postMessage(channel=channel, text=message)
