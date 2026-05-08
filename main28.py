# -----------------------------------
# 라이브러리 import
# -----------------------------------

import urllib.request   # HTTP 요청을 보내기 위한 라이브러리
import json             # JSON 데이터 처리를 위한 라이브러리


# -----------------------------------
# OpenWeatherMap API Key 설정
# -----------------------------------

api_key = "Enter your API key here"


# -----------------------------------
# 날씨 예보 API 요청 URL
# - 서울 지역 기준
# - 섭씨 단위 사용
# - 최대 8개 예보 데이터 요청
# -----------------------------------

url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"


# -----------------------------------
# API 서버에 요청 후 데이터 수신
# -----------------------------------

with urllib.request.urlopen(url) as r:

    # JSON 형식 데이터를 Python 객체로 변환
    data = json.loads(r.read())


# -----------------------------------
# 날씨 예보 데이터 출력
# -----------------------------------

for i in range(8):

    item = data['list'][i]

    # UTC 시간을 한국 시간으로 변환
    hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)

    # 온도 정보
    temp = item['main']['temp']

    # 습도 정보
    humi = item['main']['humidity']

    # 날씨 상태 설명
    desc = item['weather'][0]['description']

    # 결과 출력
    print(f"({hour}h {temp}C {humi}% {desc})")
