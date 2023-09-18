
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import math
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)



def display_wave(length):

    s = ""
    high = 7

    end_flag = 0
    c = 0
    while ( not end_flag ):
        for i in range(1, high+1):
            s += "\\" * (i-1) + "\\\n"
            c+=1
            if c >= length:
                end_flag = 1
                break

        if end_flag:
            break
        for i in range(high, 0, -1):
            s += "/" * (i-1) + "/\n"
            c+=1
            if c >= length:
                end_flag = 1
                break

    return s
    
 
def calc_pm(angle, velocity, g):

    max_high = (velocity**2 + math.sin(math.radians(angle))**2)/2/g
    max_high_time = velocity * math.sin(math.radians(angle)) / g
    land = 2 * velocity * math.sin(math.radians(angle)) / g
    R = 2 * (velocity)**2 * math.sin(math.radians(angle)) * math.cos(math.radians(angle)) / g

    r = f"仰角: {angle}度\n初速度: {veloctiy}m/s\n加速度: {g}m/s2\n計算結果如下\n\n最高點高度: {max_high}m\n最高點時間: {max_hgh_time}\n著地時間: {land}s\n射程: {R}\n"
    return r

def message_response(text):

    response = ""

    if "斜拋" in text:
        response =  "Projectile motion!!!\n\n如果想要使用斜拋計算功能，請輸入 \'pm angle velocity g\'\n比如: pm 30 10 9.8\n代表計算仰角30度，初速度10，加速度為9.8的斜拋所有資訊"
    elif "pm" in text:
        # further test

        try:
            angle = int(text.split()[1])
        except:
            return "Projectile motion!!!\n\n如果想要使用斜拋計算功能，請輸入 \'pm angle velocity g\'\n比如: pm 30 10 10\n代表計算仰角30度，初速度10，加速度為10的斜拋所有資訊"
        try:
            velocity = int(text.split()[2])
        except:
            return "Projectile motion!!!\n\n如果想要使用斜拋計算功能，請輸入 \'pm angle velocity g\'\n比如: pm 30 10 10\n代表計算仰角30度，初速度10，加速度為10的斜拋所有資訊"
        try:
            g = int(text.split()[3])
        except:
            return "Projectile motion!!!\n\n如果想要使用斜拋計算功能，請輸入 \'pm angle velocity g\'\n比如: pm 30 10 10\n代表計算仰角30度，初速度10，加速度為10的斜拋所有資訊"


        response = calc_pm(angle, velocity, g)
        return response

    elif "wave" in text:

        try:
            length = int(text.split()[1])
        except:
            return "顯示波浪，請輸入 \'wave length\'\n比如: wave 20\n代表顯示20行的波浪"

        return f"輸出{length}行\n" + display_wave(length)

    elif text == "help":
        return "I will help you\n請先答對1,2,3題以解鎖新功能\n輸入\"第一題\"開始作答\n若答案正確則會自動跳到下一題\n(想使用新功能嗎?趕快開始吧!)"

    elif text == "第一題":
        return "小明的家在（6，7），而他希望能在離他家距離25公尺、在座標點上，且和y軸和x軸的距離不會超過13的地方開一家早餐店。請問早餐店的座標可能為何？\n(答案為負整數點)\n答案請輸入\n(x,y)\n(不用空格)"

    elif text == "(-9,-13)":
        return "恭喜答對第一題\n\n第二題如下:\n\n222"

    else:
        response = "輸入 \"help\""

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
