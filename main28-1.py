# -----------------------------------
# 라이브러리 import
# -----------------------------------

import urllib.request
import json
import asyncio
from telegram import Bot


# -----------------------------------
# Telegram Bot 및 API 정보 설정
# -----------------------------------

telegram_id = "Enter your chat ID here"
my_token = "Enter your bot token here"
api_key = "Enter your API key here"


# -----------------------------------
# Telegram Bot 객체 생성
# -----------------------------------

bot = Bot(token=my_token)


# -----------------------------------
# 날씨 정보를 가져오는 함수
# -----------------------------------

def getWeather():

    # OpenWeatherMap API 요청 URL
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

    # API 요청 및 데이터 수신
    with urllib.request.urlopen(url) as r:

        # JSON 데이터 변환
        data = json.loads(r.read())

    text = ""

    # 예보 데이터 8개 출력
    for i in range(8):

        item = data['list'][i]

        # 한국 시간 변환
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)

        # 온도
        temp = item['main']['temp']

        # 습도
        humi = item['main']['humidity']

        # 날씨 설명
        desc = item['weather'][0]['description']

        # 문자열 구성
        text += f"({hour}h {temp}C {humi}% {desc})\n"

    return text


# -----------------------------------
# Telegram 메시지 전송 함수
# -----------------------------------

async def main():

    # 날씨 정보 가져오기
    msg = getWeather()

    # 콘솔 출력
    print(msg)

    # Telegram 메시지 전송
    await bot.send_message(
        chat_id=telegram_id,
        text=msg
    )


# -----------------------------------
# 프로그램 실행
# -----------------------------------

asyncio.run(main())
