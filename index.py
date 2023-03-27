from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import func
import os

true = True
false = False
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


@line_handler.add(MessageEvent, message=TextMessage)
def what2Eat(event):
    if '今天吃什麼' in event.message.text or '吃膩ㄌ啦' in event.message.text:
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage('今天吃這個吧！',func.what_today_eat())
        )
    if '我想吃' in event.message.text:
        # 儲存 pdName 變數，下一次傳送訊息時使用
        pdName = event.message.text.replace('我想吃', '').strip()
        # 在下一次傳送訊息時呼叫 search_product(pdName) 函數
        line_bot_api.reply_message(
                event.reply_token,
            TextSendMessage(text=func.search_product(pdName))
        )
            # line_bot_api.reply_message(
            #     event.reply_token,
            #     FlexSendMessage('找到一些好料的!',func.search_product(pdName))
            # )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我不懂你在說什麼，請再說一次')
        )



if __name__ == "__main__":
    app.run()