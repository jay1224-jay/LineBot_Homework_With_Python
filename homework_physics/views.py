
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
def show_pm(angle, velocity):
    # 6x6 grid

    #     o
    #   o  o
    #  o    o
    #        o
    #         o

    s = \
    " o    " + "\n" + \
    "o o   " + "\n" + \
    "   o  " + "\n" + \
    "    o "

    print(s)
    return s 

def message_response(text):

    response = ""

    if "斜拋" in text:
        response =  "Projectile motion!!!\n\n如果想要顯示斜拋模擬圖，請輸入 \'pm angle velocity\'\n比如: pm 30 10\n代表模擬仰角30度，初速度為10的斜拋"
    elif "pm" in text:
        # further test

        try:
            angle = int(text.split()[1])
        except:
            return "如果想要顯示斜拋模擬圖，請輸入 \'pm angle velocity\'\n比如: pm 30 10\n代表模擬仰角30度，初速度為10的斜拋"
        try:
            velocity = int(text.split()[2])
        except:
            return "如果想要顯示斜拋模擬圖，請輸入 \'pm angle velocity\'\n比如: pm 37 5\n代表模擬仰角37度，初速度為5的斜拋"

        response = show_pm(angle, velocity)

    else:
        response = text[::-1]

    return response
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    [ 
                        TextSendMessage(text=message_response(event.message.text))
                    ]
                        
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
