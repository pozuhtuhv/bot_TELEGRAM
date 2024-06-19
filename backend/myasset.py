# 자산정보

import jwt
import requests
import uuid

async def myasset(SERVER_URL, UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY):
    payload = {
    'access_key': UPBIT_ACCESS_KEY,
    'nonce': str(uuid.uuid4()),
    }
    jwt_token = jwt.encode(payload, UPBIT_SECRET_KEY)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }
    res = requests.get(SERVER_URL, headers=headers)
    data = res.json()

    output_lines = []

    # 각 코인의 정보를 한 줄씩 리스트에 추가합니다
    for item in data:
        output_lines.append(f"보유코인: {item['currency']}\n보유자산: {item['balance']}\n매수평균가: {item['avg_buy_price']}\n")

    return '\n'.join(output_lines)