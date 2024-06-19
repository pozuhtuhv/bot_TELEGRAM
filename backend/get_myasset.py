# 자산정보

import jwt
import uuid
import httpx

async def get_myasset(SERVER_URL, UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY):
    payload = {
        'access_key': UPBIT_ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }
    jwt_token = jwt.encode(payload, UPBIT_SECRET_KEY, algorithm='HS256')
    authorization = f'Bearer {jwt_token}'
    headers = {
        'Authorization': authorization,
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(SERVER_URL, headers=headers)
        data = res.json()

    output_lines = []

    # 각 코인의 정보를 한 줄씩 리스트에 추가합니다
    for item in data:
        output_lines.append(
            f"보유코인: {item['currency']}\n"
            f"보유자산: {item['balance']}\n"
            f"매수평균가: {item['avg_buy_price']}\n"
        )

    return '\n'.join(output_lines)