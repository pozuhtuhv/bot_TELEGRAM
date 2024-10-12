# 가격 정보 알림

import httpx
import time

# 가격 수집에 대한 요청수 제한에 대한 부분은 따로 공지가 없지만 최대한 무리안가게

async def get_pricetrace(price_list, SERVER_URL, headers):
    msg = []
    headers = {"accept": "application/json"}
    for coin in range(0, len(price_list)):
        time.sleep(0.5)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVER_URL}?markets={price_list[coin]}", headers=headers)
            data = response.json()
            for item in data:
                msg.append(
                    f"코드: {item['market']}\n"
                    f"현재가: {item['trade_price']}\n"
                    f"진행: {item['change']}\n"
                    f"변화값: {item['change_price']}\n"
                    f"변동율: {item['change_rate']}\n"
                )
    return msg


# /priceadd KRW-BTC
# /priceadd BTC-ETH