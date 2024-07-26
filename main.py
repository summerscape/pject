from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import ai2, weatherAPI, new_location

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청을 허용합니다. 특정 도메인만 허용하려면 ["http://example.com"]처럼 지정합니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용합니다. 특정 메서드만 허용하려면 ["GET", "POST"]처럼 지정합니다.
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용합니다. 특정 헤더만 허용하려면 ["Content-Type"]처럼 지정합니다.
)






@app.get("/")
async def root():
    return {"hello world"}

@app.get("/code")
async def root():
    return ai2.data_dict

@app.get("/weather")
async def root():
    return {
            '강수형태' : weatherAPI.pty, 
            '습도' : weatherAPI.reh, 
            '강수량' : weatherAPI.rn1, 
            '기온': weatherAPI.t1h,
            '동서바람성분' : weatherAPI.uuu,
            '풍향' : weatherAPI.vec,
            '남북바람성분' : weatherAPI.vvv,
            '풍속' : weatherAPI.wsd,
            '현재날짜' : weatherAPI.today,
            '현재시간': weatherAPI.time,

            '현재위치위도' : new_location.lat,
            '현재위치경도' : new_location.lng,
            '현재위치x좌표' : new_location.n_nx,
            '현재위치y좌표' : new_location.n_ny,

                
            }
           



