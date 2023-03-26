from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
# import func
import os
import pygsheets
import random
import json
true = True
false = False
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

def load_sheet():
    global sht
    gc = pygsheets.authorize(service_file='json/d0d_sheet_oa.json')
    sht = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/157Xh_YBiFKY9VrGPDZZxjnifWD5gSryh49basyhMcpc/'
    )
    


def what_today_eat():
    # global flexmsg
    load_sheet()
    wks = sht.worksheet_by_title('今天吃什麼')
    dataCount = int(wks.cell('K7').value)
    bingoNum = random.randint(1,dataCount)
    flexmsg = {
"type": "bubble",
"hero": {
    "type": "image",
    "url": wks.cell(f'E{bingoNum}').value,
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
        "type": "uri",
        "uri": "http://linecorp.com/"
    }
    },
    "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
        {
        "type": "text",
        "text": wks.cell(f'A{bingoNum}').value,
        "weight": "bold",
        "size": "xl"
        },
        {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
            {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                "type": "text",
                "text": "品牌",
                "color": "#2480A4",
                "size": "sm",
                "flex": 1
                },
                {
                "type": "text",
                "text": wks.cell(f'B{bingoNum}').value,
                "wrap": true,
                "color": "#E4A86A",
                "size": "sm",
                "flex": 5
                }
            ]
            },
            {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                "type": "text",
                "text": "理念",
                "color": "#2480A4",
                "size": "sm",
                "flex": 1
                },
                {
                "type": "text",
                "text": wks.cell(f'D{bingoNum}').value,
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 5
                }
            ]
            },
            {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                "type": "text",
                "text": "介紹",
                "color": "#2480A4",
                "size": "sm",
                "flex": 1
                },
                {
                "type": "text",
                "text": wks.cell(f'C{bingoNum}').value,
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 5
                }
            ]
            }
        ]
        }
    ]
    },
    "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
        {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
            "type": "uri",
            "label": "馬上嚐鮮",
            "uri": wks.cell(f'F{bingoNum}').value
        }
        }
    ],
    "flex": 0
    }
}
    return flexmsg


# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def what2Eat(event):
    if '今天吃什麼' in event.message.text:
        # flexMsg = json.dumps(func.what_today_eat())
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage('今天吃這個吧！',what_today_eat())
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我不懂你在說什麼，請再說一次')
        )



if __name__ == "__main__":
    app.run()