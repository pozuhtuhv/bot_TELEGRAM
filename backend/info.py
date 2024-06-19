# 코인 현재 가격정보

import requests
from datetime import datetime, timezone

def info(code, SERVER_URL):
    # 명령어 뒤에 입력된 인수를 받아옴.
    if code:
        headers = {"accept": "application/json"}
        response = requests.get(SERVER_URL+"?markets="+code, headers=headers)
        data = response.json()
        msg = []
        timestamp_set = int(data[0]['timestamp']) / 1000
        current_time_utc = datetime.fromtimestamp(timestamp_set).strftime('%Y-%m-%d %H:%M:%S UTC')
        for item in data:
            msg.append(f"코드: {item['market']}\현재가: {item['trade_price']}\n진행: {item['change']}\n변화값: {item['change_price']}\n변동율: {item['change_rate']}\n시간: {current_time_utc}")
    else:
        headers = {"accept": "application/json"}
        response = requests.get(SERVER_URL+"??markets=KRW-BTC", headers=headers)
        data = response.json()
        msg = []
        timestamp_set = int(data[0]['timestamp']) / 1000
        current_time_utc = datetime.fromtimestamp(timestamp_set).strftime('%Y-%m-%d %H:%M:%S UTC')
        for item in data:
            msg.append(f"코드: {item['market']}\현재가: {item['trade_price']}\n진행: {item['change']}\n변화값: {item['change_price']}\n변동율: {item['change_rate']}\n시간: {current_time_utc}")
    return msg