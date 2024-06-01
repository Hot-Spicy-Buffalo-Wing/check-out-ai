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

    return highest_sensed_temperature, lowest_sensed_temperature

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
        uv_level="낮음"
    elif 3<=highest_uv<=5:
        uv_level="보통"
    elif 6<=highest_uv<=7:
        uv_level="높음"
    elif 8<=highest_uv<=10:
        uv_level="매우높음"
    elif 11<=highest_uv:
        uv_level="위험"

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
    highest_sensed_temperature, lowest_sensed_temperature=get_sensed_temperature(areaNo)
    
    TPO_string=""
    for i in range(len(TPO)):
        TPO_string+=(TPO[i]+" "+TPO_template[TPO[i]]+" ")
    prompt=f"{get_uv(areaNo)} 수준의 자외선, 최대 {highest_sensed_temperature}도, 최저 {lowest_sensed_temperature}인 날씨에 덥거나 춥지 않게 입을 수 있고, {ageRange} {gender}가 {TPO_string}입기 좋은 옷을 입은 한국인 모델이, 깔끔한 배경에 자연스러운 포즈를 취한 머리, 무릎, 신발까지 포함한 가로가 짧고 세로가 긴 형태의 사진을 생성해주세요. 사진은 편집 없이 모델 한 명의 모습만 담겨야합니다."
    
    response=client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1792",
        n=1
    )

    return (prompt, response.data[0].url)

# %%
# ---- optional features ---
# TODO: add your clothes - search the clothes type

# TODO: 