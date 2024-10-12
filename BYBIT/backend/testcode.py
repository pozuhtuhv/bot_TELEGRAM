# 코인 현재 가격정보
import requests
import json

tokenAddresses = "0x28561b8a2360f463011c16b6cc0b0cbef8dbbcad,0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"

tokenAddressesLIST = [
    "0x28561B8A2360F463011c16b6Cc0B0cbEF8dbBcad",  # 예시 주소
    "0xAnotherTokenAddressHere"
]

response = requests.get(
    f"https://api.dexscreener.com/latest/dex/tokens/{tokenAddresses}",
    headers={},
)
data = response.json()

with open('history.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

    pairs_data = data['pairs']

    # 각 pair에서 'labels'가 'v3'인 경우 'baseToken'의 'name' 출력
    for pair in pairs_data:
        labels = pair.get('labels', [])
        chain_id = pair.get('chainId', '')
        base_token_address = pair.get('baseToken', {}).get('address', '')

        if 'v3' in labels and chain_id == 'ethereum' and base_token_address in tokenAddressesLIST:
            base_token_name = pair.get('baseToken', {}).get('name', '이름 없음')
            print(f"토큰 이름: {base_token_name}")