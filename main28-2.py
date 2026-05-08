# -----------------------------------
# 라이브러리 import
# -----------------------------------

import urllib.request
import json
import datetime
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
# 알림 전송 시간 설정
# -----------------------------------

ALERT_HOURS = [7, 10, 13, 16, 19, 22]

# 특정 시각 알림 설정
ALERT_TIMES = ["08:30", "14:45"]


# -----------------------------------
# 날씨 정보를 가져오는 함수
# -----------------------------------

def getWeather():

    # OpenWeatherMap API 요청 URL
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

    # API 요청 및 응답 수신
    with urllib.request.urlopen(url) as r:

        # JSON 데이터 변환
        data = json.loads(r.read())

    text = ""

    # 예보 데이터 반복 처리
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

        # 메시지 문자열 생성
        text += f"({hour}h {temp}C {humi}% {desc})\n"

    return text


# -----------------------------------
# Telegram 자동 알림 함수
# -----------------------------------

async def main():

    try:

        # 무한 반복 실행
        while True:

            # 현재 시간 확인
            now = datetime.datetime.now()

            # 시:분 형식 저장
            hm = now.strftime('%H:%M')

            # 정시 알림 조건
            is_alert_hour = (
                now.hour in ALERT_HOURS
                and now.minute == 0
                and now.second == 0
            )

            # 특정 시각 알림 조건
            is_alert_time = (
                hm in ALERT_TIMES
                and now.second == 0
            )

            # 조건 만족 시 메시지 전송
            if is_alert_hour or is_alert_time:

                # 날씨 정보 가져오기
                msg = getWeather()

                # 콘솔 출력
                print(msg)

                # Telegram 메시지 전송
                await bot.send_message(
                    chat_id=telegram_id,
                    text=msg
                )

            # 1초 대기
            await asyncio.sleep(1)

    # Ctrl + C 입력 시 종료
    except KeyboardInterrupt:
        pass


# -----------------------------------
# 프로그램 실행
# -----------------------------------

asyncio.run(main())
