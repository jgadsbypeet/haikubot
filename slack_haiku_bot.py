import os
import requests
import threading
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

def fetch_last_message(channel_id, trigger_ts):
    url = "https://slack.com/api/conversations.history"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    params = {
        "channel": channel_id,
        "latest": trigger_ts,
        "limit": 2,
        "inclusive": False
    }

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    messages = data.get("messages", [])

    # Return the message just before the slash command
    for msg in messages:
        if not msg.get("bot_id") and "text" in msg:
            return msg["text"]
    return "The world is full of change and contrast."

def generate_and_post_haiku(channel_text, response_url):
    prompt = f"Write a liberal-leaning haiku about this Slack message:\n\n{channel_text}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        haiku = response.choices[0].message.content.strip()
    except Exception as e:
        haiku = f"Error generating haiku: {e}"

    requests.post(response_url, json={"text": haiku})

@app.route("/haiku", methods=["POST"])
def haiku():
    data = request.form
    channel_id = data.get("channel_id")
    trigger_ts = data.get("trigger_id") or data.get("command_ts") or data.get("timestamp")
    response_url = data.get("response_url")

    threading.Thread(target=lambda: generate_and_post_haiku(
        fetch_last_message(channel_id, data.get("trigger_id")),
        response_url
    )).start()

    return "", 200
