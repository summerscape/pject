import urllib.parse
from datetime import datetime
import requests
import xmltodict
import json

import new_location


# 인코딩된 URL 부분
encoded_url = "nrxOcHmlUJ8nOfL00imPXGuJox5Cg8obpJ4BF6MfRZGo9AnpcSMZxZd2YcEer1PoA4LNiFw%2FSlnU89h66tdKkA%3D%3D"

# URL 디코딩
decoded_url = urllib.parse.unquote(encoded_url)

today =datetime.today().strftime("%Y%m%d") # 시스템상 오늘 날짜
time =datetime.today().strftime("%H") + "00"  # 시스템상 현재 시간(분은 제외함)

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params ={'serviceKey' : decoded_url, # 서비스키
         'pageNo' : '10',             # 페이지번호
         'numOfRows' : '2000',       # 한페이지 결과 수
         'dataType' : 'XML',         # 응답자료형식
         'base_date' : {today},      #발표일자 #현재날짜 출력
         'base_time' : {time},       #발표시각 #현재 시각 출력 시간단위 1400 형태
         'nx' : {new_location.n_nx},                # 예보지점 X좌표 # x좌표값
         'ny' : {new_location.n_ny} }              # 예보지점 Y좌표 # y좌표값


response = requests.get(url, params=params)
xmlData = response.text  # xml데이터
jsonStr = json.dumps(xmltodict.parse(xmlData), indent=4) # xml to json
dict = json.loads(jsonStr)

print(response)

# print(dict)
data = dict

# 불러온 데이터가  None 일 경우 오류남 예외처리 해야됨 
# 아마 api  갱신되는 시점에서 딜레이가 있는 듯 

# dict['response']['header']['resultMsg'] == 'NORMAL_SERVICE'  # true
# dict['response']['header']['resultMsg'] == 'NO_DATA'  # false












class WeatherData:
    def __init__(self):
        pass

weather_data = WeatherData()

# category와 obsrValue만 추출하여 변수로 설정
for item in data['response']['body']['items']['item']:
    category = item['category']
    value = item['obsrValue']
    setattr(weather_data, category, value)


pty = weather_data.PTY
reh = weather_data.REH
rn1 = weather_data.RN1
t1h = weather_data.T1H
vec = weather_data.VEC
vvv = weather_data.VVV
wsd = weather_data.WSD
uuu = weather_data.UUU






# 강수형태 PTY 없음0, 비1, 비/눈2, 눈3, 밧방울5, 빗방울눈날림6, 눈날림7 

# 강수량 RN1
# -, null, 0값은 강수없음
# 0.1 ~1.0mm 미만 1.0mm미만
# 1.0mm 이상 30.0mm미만 실수값 +mm(1.0mm ~ 29.9mm)
# 30.0mm 이상 50.0mm미만 30.0 ~ 50.0mm
# 50.0mm 이상 50.0mm이상


# '''
# 'PTY': '강수형태',
#  'REH': '습도',
#  'RN1': '1시간강수량',
#  'T1H': '기온',
#  'UUU': '동서바람성분',
#  'VEC': '풍향',
#  'VVV': '남북바람성분',
#  'WSD': '풍속'

#  '''

# print(f'강수형태 : {pty} \n 습도 :{reh} \n 1시간강수량{rn1} \n 기온 {t1h}  \n 풍속{ wsd}')