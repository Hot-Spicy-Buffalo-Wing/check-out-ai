# %%
import pandas as pd

areaNo_df=pd.read_excel("./data/areaNo.xlsx", sheet_name="final_formatted")
# %%
#areaNo_df=areaNo_df.drop(columns=["구분", "격자 X", "격자 Y", "경도(시)", "경도(분)", "경도(초)", "위도(시)", "위도(분)", "위도(초)", "위도(초/100)", "위치업데이트", "경도(초/100)"])
#areaNo_df.to_excel("./data/areaNo.xlsx", sheet_name="final_formatted", index=False)
# %%
province=areaNo_df["1단계"].unique().tolist()
city=areaNo_df["2단계"].unique().tolist()
district=areaNo_df["3단계"].unique().tolist()
# %%
def get_areaNo(province=None, city=None, district=None):
    if province:
        filtered_areaNo_df=areaNo_df[areaNo_df["1단계"]==province]
        if city:
            filtered_areaNo_df=filtered_areaNo_df[filtered_areaNo_df["2단계"]==city]
            if district:
                filtered_areaNo_df=filtered_areaNo_df[filtered_areaNo_df["3단계"]==district]
    return filtered_areaNo_df["행정구역코드"].values[0]
# %%
#get_areaNo("서울특별시", "강남구")["행정구역코드"].values[0]
# %%
