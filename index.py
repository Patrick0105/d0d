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
        run = func.search_product(pdName)
        a = {"type": "carousel", "contents": [{"type": "bubble", "size": "kilo", "hero": {"type": "image", "url": "https://cdn1.cybassets.com/media/W1siZiIsIjE4ODk5L3Byb2R1Y3RzLzM3MDA2NzYyLzE2NTQwNzk3OTRfOGMwYjI2MzA3ZDI3Nzg2YWM4Y2YuanBlZyJdLFsicCIsInRodW1iIiwiNjAweDYwMCJdXQ.jpeg?sha=54187ef95c3f3339", "size": "full", "aspectMode": "cover", "aspectRatio": "320:213"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "\u3010\u4ec1\u548c\u9b91\u9b5a\u3011\u6912\u9ebb\u4e5d\u5b54\u7f50\u982d", "weight": "bold", "size": "lg", "wrap": true}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u552e\u50f9", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "NT$220", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u92b7\u91cf", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "\u5df2\u92b7\u552e\uff1a4", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u7de8\u865f", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "37006762", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}], "margin": "10px", "spacing": "4px"}], "spacing": "sm", "paddingAll": "13px"}, "action": {"type": "uri", "label": "action", "uri": "https://www.bobselection.shop//products/\u4ec1\u548c\u9b91\u9b5a\u6912\u9ebb\u4e5d\u5b54\u7f50\u982d"}}, {"type": "bubble", "size": "kilo", "hero": {"type": "image", "url": "https://cdn1.cybassets.com/media/W1siZiIsIjE4ODk5L3Byb2R1Y3RzLzM0MDg4NzcwLzE2MjY5NDE0OTVfNDIwODg4NTBhMjkxMTc3ZDY3MTkuanBlZyJdLFsicCIsInRodW1iIiwiNjAweDYwMCJdXQ.jpeg?sha=e7215ffd1430f8f9", "size": "full", "aspectMode": "cover", "aspectRatio": "320:213"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "\u3010\u4ec1\u548c\u9b91\u9b5a\u3011\u9bae\u51cd\u4e5d\u5b54", "weight": "bold", "size": "lg", "wrap": true}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u552e\u50f9", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "NT$500", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u92b7\u91cf", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "\u5df2\u92b7\u552e\uff1a49", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u7de8\u865f", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "34088770", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}], "margin": "10px", "spacing": "4px"}], "spacing": "sm", "paddingAll": "13px"}, "action": {"type": "uri", "label": "action", "uri": "https://www.bobselection.shop//products/freshabalone"}}, {"type": "bubble", "size": "kilo", "hero": {"type": "image", "url": "https://cdn1.cybassets.com/media/W1siZiIsIjE4ODk5L3Byb2R1Y3RzLzM0MDg4Njg3LzE2MjY5NDAyNzNfODBhNDJkNWE1ZDdlMjI2MWQxNjkuanBlZyJdLFsicCIsInRodW1iIiwiNjAweDYwMCJdXQ.jpeg?sha=2bf36f8591e4829b", "size": "full", "aspectMode": "cover", "aspectRatio": "320:213"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "\u3010\u4ec1\u548c\u9b91\u9b5a\u3011\u9bae\u6f2c\u4e5d\u5b54", "weight": "bold", "size": "lg", "wrap": true}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u552e\u50f9", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "NT$600", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u92b7\u91cf", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "\u5df2\u92b7\u552e\uff1a44", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u7de8\u865f", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "34088687", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}], "margin": "10px", "spacing": "4px"}], "spacing": "sm", "paddingAll": "13px"}, "action": {"type": "uri", "label": "action", "uri": "https://www.bobselection.shop//products/soysauceabalone-20210722155106"}}, {"type": "bubble", "size": "kilo", "hero": {"type": "image", "url": "https://cdn1.cybassets.com/media/W1siZiIsIjE4ODk5L3Byb2R1Y3RzLzM0MDg4NjE1LzE2NzMzNDE2NDZfZTA3M2UxOGM5NjdmN2UwOWI4ZDkuanBlZyJdLFsicCIsInRodW1iIiwiNjAweDYwMCJdXQ.jpeg?sha=4f5ec73a3fea88f3", "size": "full", "aspectMode": "cover", "aspectRatio": "320:213"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "\u3010\u4ec1\u548c\u9b91\u9b5a\u3011\u4e5d\u5b54\u91ac", "weight": "bold", "size": "lg", "wrap": true}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u552e\u50f9", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "NT$400\nNT$450", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u92b7\u91cf", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "\u5df2\u92b7\u552e\uff1a75", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}, {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [{"type": "text", "text": "\u7de8\u865f", "wrap": true, "color": "#2480a4", "size": "md", "flex": 2, "align": "center"}, {"type": "text", "text": "34088615", "wrap": true, "color": "#8c8c8c", "size": "md", "flex": 5, "align": "start"}]}], "margin": "10px", "spacing": "4px"}], "spacing": "sm", "paddingAll": "13px"}, "action": {"type": "uri", "label": "action", "uri": "https://www.bobselection.shop//products/abalonesauce"}}]}
        if run == 1:
            line_bot_api.reply_message(
                event.reply_token,
            TextSendMessage(text=f'沒有關於 {pdName} 的商品哦~')
        )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage('找到一些好料的!',a)
            )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我不懂你在說什麼，請再說一次')
        )



if __name__ == "__main__":
    app.run()