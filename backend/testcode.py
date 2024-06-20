# requests 및 이외 작용 모듈 테스트 공간

import requests

url = "https://api.upbit.com/v1/market/all?isDetails=true"

headers = {"accept": "application/json"}

res = requests.get(url, headers=headers)

print(res.json())