
import pygsheets
import random
import requests
from bs4 import BeautifulSoup
import json

true = True
false = False


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
    "layout": "horizontal",
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
        },
        "color": "#E4A86A"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "換口味",
          "text": "吃膩ㄌ啦"
        },
        "color": "#2480A4"
      }
    ],
    "flex": 0
  }
}
    return flexmsg
  
def search_product(pdName):
    url = f'https://www.bobselection.shop/search?q={pdName}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_results_div = soup.find('div', {'class': 'col product_results'})
    product_items = product_results_div.select('div.col-lg-3.col-sm-4.col-6.item')

    data = {
        "type": "carousel",
        "contents": []
    }

    for item in product_items:
        product_id = item.find('div', {'class': 'product'})['product_id']
        product_name = item.find('div', {'class': 'product_title'}).text.strip()
        sold_count = item.find('div', {'class': 'product_sold'}).text.strip()
        price = item.find('div', {'class': 'product_price'}).text.strip()
        image_url = item.find('img', {'class': 'img-lazy'})['data-src']
        product_url = item.find('a', {'class': 'productClick'})['href']

        bubbleMsg = {"type":"bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": f"https:{image_url}",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": product_name,
            "weight": "bold",
            "size": "lg",
            "wrap": true
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "售價",
                    "wrap": true,
                    "color": "#2480a4",
                    "size": "md",
                    "flex": 2,
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": price,
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "md",
                    "flex": 5,
                    "align": "start"
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
                    "text": "銷量",
                    "wrap": true,
                    "color": "#2480a4",
                    "size": "md",
                    "flex": 2,
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": sold_count,
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "md",
                    "flex": 5,
                    "align": "start"
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
                    "text": "編號",
                    "wrap": true,
                    "color": "#2480a4",
                    "size": "md",
                    "flex": 2,
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": product_id,
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "md",
                    "flex": 5,
                    "align": "start"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "官網看看",
                  "uri": f"https://www.bobselection.shop/{product_url}"
                },
                "color": "#e4a86a"
              }
            ],
            "margin": "10px",
            "spacing": "4px"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    }
        data["contents"].append(bubbleMsg)
    
    return data