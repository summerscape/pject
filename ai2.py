import os
from dotenv import load_dotenv
import google.generativeai as genai
import weatherAPI

load_dotenv()
google_gemini_api_key = os.environ.get('google_gemini_api_key')

genai.configure(api_key=google_gemini_api_key)


# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.25,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)



def get_outfit_recommendation(temperature, humidity, precipitation, precipitation_type):
    # Prepare the query based on the weather data
    query = (
        f"현재 기온은 {temperature}도, 습도 {humidity}%, 강수량 {precipitation}mm, 날씨는 {precipitation_type}입니다. "
        "캐주얼, 포멀, 스포티 스타일별로 추천 옷차림을 상의, 하의, 신발, 악세서리 형태로 알려주세요. 각 스타일별 옷차림의 종류는 다음과 같습니다:\n"
        "Casual:\n"
        "- 상의: 패딩, 가디건, 가죽자켓, 원피스, 후드티, 긴팔니트, 긴팔티셔츠, 남방, 맨투맨, 반팔남방, 반팔셔츠, 반팔카라티, 반팔티셔츠, 민소매\n"
        "- 하의: 긴바지, 긴치마, 치마, 반바지\n"
        "- 신발: 로퍼, 샌들, 운동화, 워커, 장화, 털신발\n"
        "- 악세사리: 목도리, 선글라스, 우비, 우산, 장갑, 캡모자, 털모자\n"
        "Formal:\n"
        "- 상의: 코트, 가디건, 수트자켓, 긴팔니트, 긴팔셔츠, 정장원피스, 반팔셔츠, 반팔카라티\n"
        "- 하의: 슬랙스, 반바지슬랙스, 정장치마\n"
        "- 신발: 로퍼, 정장구두\n"
        "- 악세사리: 우비, 우산, 장갑, 목도리\n"
        "Sporty:\n"
        "- 상의: 패딩, 바람막이, 야구잠바, 후드티, 맨투맨, 반팔티셔츠\n"
        "- 하의: 트레이닝 긴바지, 트레이닝 반바지\n"
        "- 신발: 스포츠샌들, 운동화\n"
        "- 악세사리: 선글라스, 우비, 우산, 캡모자\n"
        "- 각 항목에서 아이템은 한가지씩만 응답합니다\n"
        "- 출력형태는 딕셔너리 형태로 응답\n"

        
        "위의 정보를 기반으로 응답해 주세요."
        
    )
    
    response = model.generate_content([{'role': 'user', 'parts': [query]}])
    
    return response.text

       

T1H = weatherAPI.t1h
REH = weatherAPI.reh
RN1 = weatherAPI.rn1
WSD = weatherAPI.wsd
PTY = weatherAPI.pty


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


# # 예시 사용
# PTY = 1  # 강수 형태를 설정
# print(weather_description(PTY))  # "비" 출력

# 강수량 RN1
# -, null, 0값은 강수없음
# 0.1 ~1.0mm 미만 1.0mm미만
# 1.0mm 이상 30.0mm미만 실수값 +mm(1.0mm ~ 29.9mm)
# 30.0mm 이상 50.0mm미만 30.0 ~ 50.0mm
# 50.0mm 이상 50.0mm이상


# 강수형태 PTY 없음0, 비1, 비/눈2, 눈3, 밧방울5, 빗방울눈날림6, 눈날림7 

def weather_description(PTY):
    if PTY == '0':
        return "맑음"
    elif PTY == '1':
        return "비"
    elif PTY == '2':
        return "비와 눈"
    elif PTY == '3':
        return "눈"
    elif PTY == '5':
        return "빗방울"
    elif PTY == '6':
        return "빗방울과 눈날림"
    elif PTY == '7':
        return "눈날림"
    else:
        return "알수없음"
    

user_queries = [
    {'role': 'user', 'parts': [f"현재 기온은 {T1H} 도, 습도 {REH}%, 강수량 {RN1}mm, 날씨는 {weather_description(PTY)}입니다. 각 스타일별로 추천 옷차림을 알려주세요."]},
]

history = []

for user_query in user_queries:
    history.append(user_query)
    # print(f'[사용자]: {user_query["parts"][0]}')
    
    # Extract weather data from the query
    temperature = T1H
    humidity = REH
    precipitation = RN1
    precipitation_type = weather_description(PTY)
    
    response_text = get_outfit_recommendation(temperature, humidity, precipitation, precipitation_type)
    
    # print(f'[모델]: {response_text}')
    
    history.append({'role': 'assistant', 'parts': [response_text]})



import json

# 백틱이 포함된 JSON 문자열
json_string_with_backticks = response_text

# 문자열에서 백틱 제거
json_string = json_string_with_backticks.replace('```', '').strip()

# JSON 문자열을 파이썬 딕셔너리로 변환
data_dict = json.loads(json_string)

# 변환된 딕셔너리 출력
print(data_dict)

