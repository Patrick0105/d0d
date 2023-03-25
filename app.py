import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('4jblcI1eMPIATBEsyycC6uoWwtB2w4rS9N8WjDsrSdPaPbdkzIVlxwgsQU+4cMkIMC3nmtJJKbJ9p3nantYWdjJasTdrUVinQjXN5BEiMhr3oA60D6OPZxoZwpC/jM2ftcXIwCwld/o74iEoZnwnpgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('088a1f2d53fec5f57362b8732b17811b')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
