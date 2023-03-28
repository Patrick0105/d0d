
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
  try:
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

        bubbleMsg = {"type": "bubble",
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
            "wrap": True
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
                    "wrap": True,
                    "color": "#2480a4",
                    "size": "md",
                    "flex": 2,
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": price,
                    "wrap": True,
                    "color": "#e4a86a",
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
                    "wrap": True,
                    "color": "#2480a4",
                    "size": "md",
                    "flex": 2,
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": sold_count,
                    "wrap": True,
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
                    "wrap": True,
                    "color": "#2480a4",
                    "size": "md",
                    "flex": 2,
                    "align": "center"
                  },
                  {
                    "type": "text",
                    "text": product_id,
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "md",
                    "flex": 5,
                    "align": "start"
                  }
                ]
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
  except:
    return 1
  
def get_coupon():
  return {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn1.cybassets.com/s/files/18899/theme/64072/assets/img/1658221501_f33b3a4e_main_slider_item_4_lg.jpg?1658221501",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://www.bobselection.shop/search?q=%E8%8A%9D%E9%BA%BB"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "芝麻食品 85折",
        "wrap": true,
        "weight": "bold",
        "gravity": "center",
        "size": "xl",
        "color": "#E4A86A",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": []
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
                "text": "優惠代碼",
                "color": "#2480a4",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "C8763",
                "wrap": true,
                "color": "#E4A86A",
                "size": "sm",
                "flex": 4
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
                "text": "使用期限",
                "color": "#2480a4",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "Monday 25, 9:00PM",
                "wrap": true,
                "size": "sm",
                "color": "#E4A86A",
                "flex": 4
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
                "text": "使用門檻",
                "color": "#2480a4",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "訂單金額滿足 $8763 元",
                "wrap": true,
                "color": "#E4A86A",
                "size": "sm",
                "flex": 4
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "contents": [
          {
            "type": "image",
            "url": "https://stonetestweb.azurewebsites.net/img.aspx?custid=1&username=public&codetype=QR&EClevel=1&logo=&data=https%3a%2f%2fcdn.bella.tw%2findex_image%2fSIXlRaTmfMy5HlCHixB9BrxUUJEO0RsHCitEVCpV.jpeg",
            "aspectMode": "cover",
            "size": "xl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "優惠代碼僅可使用一次",
            "color": "#aaaaaa",
            "wrap": true,
            "margin": "xxl",
            "size": "xs",
            "align": "center",
            "gravity": "center"
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "領取優惠",
              "uri": "https://assets.matters.news/embed/dfa5ea2a-24c0-4607-9951-ba525e8013f7.jpeg"
            },
            "color": "#e4a86a",
            "gravity": "center",
            "style": "primary",
            "margin": "10px"
          }
        ]
      }
    ],
    "backgroundColor": "#053036"
  }
}