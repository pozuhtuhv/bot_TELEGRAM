# 코인 현재 가격정보

import httpx
from datetime import datetime, timezone

async def get_info(code, SERVER_URL, headers):
    msg = []
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVER_URL}?markets={code}", headers=headers)
        data = response.json()

    timestamp_set = int(data[0]['timestamp']) / 1000
    current_time_utc = datetime.fromtimestamp(timestamp_set).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    for item in data:
        msg.append(
            f"코드: {item['market']}\n"
            f"현재가: {item['trade_price']}\n"
            f"진행: {item['change']}\n"
            f"변화값: {item['change_price']}\n"
            f"변동율: {item['change_rate']}\n"
            f"시간: {current_time_utc}"
        )
    
    return msg
