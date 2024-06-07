# %%
# TODO: generation of lookbook given mood and condition
import requests
import os
import datetime as dt

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

import areaNo as areaNo_py

client=OpenAI()
# %% 2024060101 형태의 시간 
def format_current_time():
    now=dt.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    hour=now.hour

    formatted_time=f"{year}{month:02}{day:02}{hour:02}"
    return formatted_time

# print(format_current_time())

# %% weather API
# 입력값: serviceKey, dataType=JSON, areaNo={areaNo.py에서 지역번호 호출}, time={format_current_time()}, requestCode=A44
# 자외선: [h0, h3, h6, h9] 값을 보고 최대 값을 기준으로 {위험: 11 이상, 매우높음: 8~10, 높음: 6~7, 보통: 3~5, 낮음: 0~2}으로 분류 => prompt 입력값
# 체감온도: 현재 시각을 기준으로 [h1, h2, h3, h4, h5, h6, h7, h8, h9] 값을 보고 최대 및 최저 값을 prompt에 입력
def get_sensed_temperature(areaNo: str) -> tuple[int, int]:
    base_url="http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4"
    params={
        "serviceKey": os.getenv("WEATHER_API_KEY"),
        "dataType": "JSON",
        "areaNo": areaNo,
        "time": format_current_time(),
        "requestCode": "A46"
    }
    response=requests.get(base_url+"/getSenTaIdxV4", params=params)
    got_sensed_temperature=response.json()

    highest_sensed_temperature=0
    lowest_sensed_temperature=100
    for i in range(1, 10):
        highest_sensed_temperature=max(highest_sensed_temperature, int(got_sensed_temperature["response"]["body"]["items"]["item"][0][f"h{i}"]))
        lowest_sensed_temperature=min(lowest_sensed_temperature, int(got_sensed_temperature["response"]["body"]["items"]["item"][0][f"h{i}"]))

    if highest_sensed_temperature<21:
        return "선선한"
    elif 21<=highest_sensed_temperature<25:
        return "온화한"
    elif 25<=highest_sensed_temperature<28:
        return "더운"
    elif 28<=highest_sensed_temperature<31:
        return "매우 더운"
    elif 31<=highest_sensed_temperature:
        return "극심하게 더운"

#get_sensed_temperature("1100000000")
# %%
def get_uv(areaNo: str):
    base_url="http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4"
    params={
        "serviceKey": os.getenv("WEATHER_API_KEY"),
        "dataType": "JSON",
        "areaNo": areaNo,
        "time": format_current_time()
    }
    response=requests.get(base_url+"/getUVIdxV4", params=params)
    got_uv=response.json()

    highest_uv=0
    for i in range(0, 10, 3):
        highest_uv=max(highest_uv, int(got_uv["response"]["body"]["items"]["item"][0][f"h{i}"]))

    if 0<=highest_uv<=2:
        uv_level="약하고"
    elif 3<=highest_uv<=5:
        uv_level="적당하고"
    elif 6<=highest_uv<=7:
        uv_level="강하고"
    elif 8<=highest_uv<=10:
        uv_level="매우 강하고"
    elif 11<=highest_uv:
        uv_level="위험한 수준이고"

    return uv_level

#get_uv("1100000000")
# %%
# gender=["남자", "여자", None], ageRange=["10대 초반", "10대 후반", "20대 초반", ...], TPO=[데이트, 여행, 출근, 결혼식 하객으로 참석]할 때 입기 좋은 [꾸안꾸, 여름코디, 캠퍼스룩, 데일리] 스타일로 입기 좋은 [휴양지, 놀이공원, 카페, 운동하러, 축제, 파티, 소개팅] 갈 때 입기 좋은
TPO_template={
    "데이트": "할 때 ",
    "여행": "할 때 ",
    "출근": "할 때 ",
    "결혼식 하객으로 참석": "할 때 ",
    "꾸안꾸": "스타일로 ",
    "여름코디": "스타일로 ",
    "캠퍼스룩": "스타일로 ",
    "데일리": "스타일로 ",
    "휴양지": "갈 때 ",
    "놀이공원": "갈 때 ",
    "카페": "갈 때 ",
    "운동하러": "갈 때 ",
    "축제": "갈 때 ",
    "파티": "갈 때 ",
    "소개팅": "갈 때 "
}
# %%
def get_lookbook(gender: str= "", ageRange: str= "", area: dict[str, str]= {"province":"", "city":"", "district":""}, TPO: list[str]= [""] ) -> str:
    areaNo=areaNo_py.get_areaNo(area["province"], area["city"], area["district"])
    sensed_temperature=get_sensed_temperature(areaNo)
    
    TPO_string=""
    for i in range(len(TPO)):
        TPO_string+=(TPO[i]+" "+TPO_template[TPO[i]]+" ")
    prompt=f"""
# 룩북 생성기

## 필요 요소
- 자외선 농도
- 날씨
- 상황
- 나이
- 성별

## 출력 결과
- 1024x1792픽셀
- 깔끔한 배경에서 찍은 전신 사진
- 머리부터 발끝까지 나온 전신 하나
- 사람 외에 다른 사물은 없어야 함
- 한국인 모델 한명
- 전신 사진 외 다른 구도는 없어야 함

## 입력
- 자외선 농도: '{get_uv(areaNo)}'
- 날씨: '{sensed_temperature}'
- 상황: '{TPO_string}'
- 나이: '{ageRange}'
- 성별: '{gender}'
    """.strip()
    
    try:
        response=client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            n=1
        )
    except Exception as e:
        return (prompt, str(e))

    return (prompt, response.data[0].url)

# %%
# ---- optional features ---
# TODO: add your clothes - search the clothes type

# TODO: 
