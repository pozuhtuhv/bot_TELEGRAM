# 코인 현재 가격정보
import requests
import json

tokenAddresses = "0x28561b8a2360f463011c16b6cc0b0cbef8dbbcad,0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"

response = requests.get(
    f"https://api.dexscreener.com/latest/dex/tokens/{tokenAddresses}",
    headers={},
)
data = response.json()

with open('history.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# price_load
    for item in data:
        labels = item.get('labels', [])
        print(labels)
        # for label in labels:
            # result = i['labels']


    #     if 'v3' in result:
    #         print(i['priceUsd'])