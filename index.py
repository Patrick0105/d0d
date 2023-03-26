from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import func
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

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


@line_bot_api.add(MessageEvent, message=TextMessage)
def what2Eat(event):
    if '今天吃什麼' in event.message.text:
        msg = func.what_today_eat()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage('今天吃這個吧！',{"type": "bubble", "hero": {"type": "image", "url": "https://cdn1.cybassets.com/media/W1siZiIsIjE4ODk5L3Byb2R1Y3RzLzM0MDY0NjE2LzE2NDczMzA5MzJfNGQ3MTVhOGJmMzEzY2RjNWVjNWEuanBlZyJdLFsicCIsInRodW1iIiwiNjAweDYwMCJdXQ.jpeg?sha=9d5ce2a4668c6d29", "size": "full", "aspectRatio": "20:13", "aspectMode": "cover", "action": {"type": "uri", "uri": "http://linecorp.com/"}}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "\u3010\u4ec1\u548c\u9b91\u9b5a\u3011\u9bae\u51cd\u6d77\u767d\u8766", "weight": "bold", "size": "xl"}, {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": [{"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u54c1\u724c", "color": "#2480A4", "size": "sm", "flex": 1}, {"type": "text", "text": "\u4ec1\u548c\u9b91\u9b5a", "wrap": true, "color": "#E4A86A", "size": "sm", "flex": 5}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u7406\u5ff5", "color": "#2480A4", "size": "sm", "flex": 1}, {"type": "text", "text": "\u5f15\u63a5\u6771\u5317\u89d2\u7d14\u6de8\u6d77\u6c34\u990a\u6b96\uff0c\u7d66\u4e88\u8ddf\u9b91\u9b5a\u4e00\u6a23\u7684\u751f\u9577\u74b0\u5883\uff0c\u767d\u8766\u8089\u8cea\u723d\u8106\u9bae\u751c\u3002", "wrap": true, "color": "#666666", "size": "sm", "flex": 5}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u4ecb\u7d39", "color": "#2480A4", "size": "sm", "flex": 1}, {"type": "text", "text": "\u6771\u5317\u89d2\u6d77\u57df\u7684\u6d77\u6c34\u6eab\u5ea6\u4f4e\uff0c\u9e79\u5ea6\u9ad8\u90543.0~3.5\uff0c\u7d66\u4e88\u767d\u8766\u6dbc\u723d\u990a\u6b96\u74b0\u5883\uff0c\u4ee5\u9b5a\u8089\u9935\u990a\uff0c\u751c\u5ea6\u9ad8\u53c8\u8106\u3002", "wrap": true, "color": "#666666", "size": "sm", "flex": 5}]}]}]}, "footer": {"type": "box", "layout": "vertical", "spacing": "sm", "contents": [{"type": "button", "style": "link", "height": "sm", "action": {"type": "uri", "label": "\u99ac\u4e0a\u5690\u9bae", "uri": "https://www.bobselection.shop/products/%E4%BB%81%E5%92%8C%E9%AE%91%E9%AD%9A%E9%AE%AE%E5%87%8D%E6%B5%B7%E7%99%BD%E8%9D%A6"}}], "flex": 0}})
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我不懂你在說什麼，請再說一次')
        )



if __name__ == "__main__":
    app.run()