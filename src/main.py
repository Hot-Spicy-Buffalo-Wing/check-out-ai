from enum import Enum
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from lookbook import get_lookbook
from image import image_service

app = FastAPI()

class Gender(str, Enum):
    female="여자"
    male="남자"
    none="논바이너리"

class AgeRange(str, Enum):
    early_teens="10대 초반"
    late_teens="10대 후반"
    early_twenties="20대 초반"
    late_twenties="20대 후반"
    early_thirties="30대 초반"
    late_thirties="30대 후반"
    early_forties="40대 초반"
    late_forties="40대 후반"
    early_fifties="50대 초반"
    late_fifties="50대 후반"

class Area(BaseModel):
    province: str
    city: str
    district: str


class Item(BaseModel):
    gender: Gender
    ageRange: AgeRange
    area: Area
    TPO: list[str]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/lookbook")
async def get_lookbook_endpoint(item: Item):
    # return {"gender": f"{gender.value}", "ageRange": f"{ageRange.value}", "area": f"{area.model_dump()}", "TPO": f"{type(TPO)}"}
    prompt, url= get_lookbook(item.gender.value, item.ageRange.value, item.area.model_dump(), item.TPO.copy())
    # print("prompt done")
# 
    # try:
        # image_uuid = image_service(url="https://via.placeholder.com/150x150")
        # image_uuid = image_service(url=url)
    return {"prompt": prompt, "url": url}
    # except Exception as e:
        # print(e)
        # raise HTTPException(status_code=422, detail="Image upload error\n" + str(e))