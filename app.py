import os
import sys

import globals

from datetime import datetime

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image

load_dotenv()


machine = TocMachine(
    states=["init", "menu",
                    "spending",
                            "setGoal", 
                                    "storeGoal",
                            "setSpendingMenu",
                                    "setSpending", "storeSpending",
                            "checkSpendingMenu",
                                    "checkSpending",
                    "tree", 
                            "myCurrentTree", "configInteractWithTree", "interactWithTree",
                            "treeIntro",
                    ],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "spending",
            "conditions": "is_going_to_spending",
        },
                    {
                        "trigger": "advance",
                        "source": "spending",
                        "dest": "setGoal",
                        "conditions": "is_going_to_setGoal",
                    },
                                {
                                    "trigger": "advance",
                                    "source": "setGoal",
                                    "dest": "storeGoal",
                                    "conditions": "is_going_to_storeGoal",
                                },
                                {
                                    "trigger": "advance",
                                    "source": "storeGoal",
                                    "dest": "spending",
                                },
                    {
                        "trigger": "advance",
                        "source": "spending",
                        "dest": "setSpendingMenu",
                        "conditions": "is_going_to_setSpendingMenu",
                    },
                                {
                                    "trigger": "advance",
                                    "source": "setSpendingMenu",
                                    "dest": "setSpending",
                                    "conditions": "is_going_to_setSpending",
                                },
                                            {
                                                "trigger": "advance",
                                                "source": "setSpending",
                                                "dest": "storeSpending",
                                                "conditions": "is_going_to_storeSpending",
                                            },
                                                        {
                                                            "trigger": "advance",
                                                            "source": "storeSpending",
                                                            "dest": "setSpending",
                                                            "conditions": "is_going_to_setSpending",
                                                        },
                                                        {
                                                            "trigger": "advance",
                                                            "source": "storeSpending",
                                                            "dest": "spending",
                                                            "conditions": "is_going_to_spending",
                                                        },
                    {
                        "trigger": "advance",
                        "source": "spending",
                        "dest": "checkSpendingMenu",
                        "conditions": "is_going_to_checkSpendingMenu",
                    },
                                {
                                    "trigger": "advance",
                                    "source": "checkSpendingMenu",
                                    "dest": "checkSpending",
                                    "conditions": "is_going_to_checkSpending",
                                },
                                            {
                                                "trigger": "advance",
                                                "source": "checkSpending",
                                                "dest": "spending",
                                            },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "tree",
            "conditions": "is_going_to_tree",
        },
                    {
                        "trigger": "advance",
                        "source": "tree",
                        "dest": "myCurrentTree",
                        "conditions": "is_going_to_myCurrentTree",
                    },
                                {
                                    "trigger": "advance",
                                    "source": "myCurrentTree",
                                    "dest": "tree",
                                    "conditions": "is_going_to_tree",
                                },
                                {
                                    "trigger": "advance",
                                    "source": "myCurrentTree",
                                    "dest": "configInteractWithTree",
                                    "conditions": "is_going_to_configInteractWithTree",
                                },
                                            {
                                                "trigger": "advance",
                                                "source": "configInteractWithTree",
                                                "dest": "myCurrentTree",
                                                "conditions": "is_going_to_myCurrentTree",
                                            },
                                            {
                                                "trigger": "advance",
                                                "source": "configInteractWithTree",
                                                "dest": "interactWithTree",
                                                "conditions": "is_going_to_interactWithTree",
                                            },
                                                        {
                                                            "trigger": "advance",
                                                            "source": "interactWithTree",
                                                            "dest": "myCurrentTree",
                                                        },
                    {
                        "trigger": "advance",
                        "source": "tree",
                        "dest": "treeIntro",
                        "conditions": "is_going_to_treeIntro",
                    },
                                {
                                    "trigger": "advance",
                                    "source": "treeIntro",
                                    "dest": "tree",
                                },
        {
            "trigger": "advance",
            "source": "spending",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "tree",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        #{"trigger": "go_back", "source": ["spending", "tree"], "dest": "menu"},
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

#goal = 0

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        date = datetime.fromtimestamp(event.timestamp / 1000)
        globals.day = date.day
        globals.month = date.month
        globals.year = date.year
        if event.type == "follow":
            machine.advance(event)
            continue
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        #if not isinstance(event.message.text, str):
        #    continue
        print(f"\nFSM STATE: {machine.state}")
        #print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        
        #print("\n\ngoal = " + str(goal) + "\n\n")
        #if(machine.state == "storeGoal"):
        #    goal = int(event.message.text)
        #print(f"\n\ngoal = {globals.goal}\nrecord = {globals.spending}\n\n")
        if response == False:
            if event.message.text == "fsm":
                send_image(event.reply_token, "https://i.imgur.com/B8VMEvQ.png")
            else:
                send_text_message(event.reply_token, "未知的指令，請確認輸入是否正確")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    print("ji")
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    globals.initGlobals()
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
