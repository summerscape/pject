from fastapi import FastAPI

import ai, ai2, weatherAPI, location, new_location


app = FastAPI()

@app.get("/")
async def root():
    return {"hello world"}

@app.get("/code")
async def root():
    # return ai.recommendations
    return ai2.response_text

@app.get("/weather")
async def root():
    return {
            '강수형태' : weatherAPI.pty, 
            '습도' : weatherAPI.reh, 
            '1시간 강수량' : weatherAPI.rn1, 
            '기온': weatherAPI.t1h,
            '동서바람성분' : weatherAPI.uuu,
            '풍향' : weatherAPI.vec,
            '남북바람성분' : weatherAPI.vvv,
            '풍속' : weatherAPI.wsd,
            '현재날짜' : weatherAPI.today,
            '현재시간': weatherAPI.time,
            '현재위치x좌표' : location.nx,
            '현재위치y좌표' : location.ny,
            '현재위치위도' : location.lat_nx,
            '현재위치경도' : location.lng_ny,
            
             
            'n현재위치위도' : new_location.lat,
            'n현재위치경도' : new_location.lng,
            'n현재위치x좌표' : new_location.n_nx,
            'n현재위치y좌표' : new_location.n_ny,

                
            }
           



