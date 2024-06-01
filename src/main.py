from enum import Enum
from pydantic import BaseModel

from fastapi import FastAPI
from lookbook import get_lookbook

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/lookbook/")
async def get_lookbook_endpoint(gender: Gender, ageRange: AgeRange, area: Area, TPO: list[str]):
    # return {"gender": f"{gender.value}", "ageRange": f"{ageRange.value}", "area": f"{area.model_dump()}", "TPO": f"{type(TPO)}"}
    prompt, url= get_lookbook(gender.value, ageRange.value, area.model_dump(), TPO.copy())
    return {"prompt": prompt, "url": url}