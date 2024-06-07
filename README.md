# AI Inputs
> Gender and age range information are set as user's information when the user first enter the service. 
### 1. Gender
- There are `Male / Female / Non binary` options
### 2. Age range
- Options are `early 20's, late 20's, early 30's ... late 50's`

### 3. Location
- Use [Korea Meteorological Administration API](https://www.data.go.kr/data/15085288/openapi.do) (기상청_생활기상지수 조회서비스(3.0)) for retrieving ultraviolet(UV) level and apparent temperature (체감 온도).
- The three types of location information is needed (ex.`광주광역시 / 북구 / 용봉동`)
### 4. Time & Place & Occasion (TPO)
- Circumstance to be considered when making styling.
-  Options are as follows. `[꾸안꾸, 여름코디, 데일리, 데이트, 캠퍼스룩, 여행, 출근룩, 하객룩, 휴양지, 놀이공원, 카페, 운동, 축제, 파티, 소개팅]`
-  Multi choice is possible.

---

### About AI Tech Stack
- Mainly developed with **Python** 
- Image generation with [Dall-e](https://platform.openai.com/docs/guides/images)
- Functions are deployed with (FastAPI)[https://fastapi.tiangolo.com/ko/]
