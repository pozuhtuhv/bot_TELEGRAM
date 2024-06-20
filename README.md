### bot_upbit_telegram

### NOT BUY, NOT SELL, JUST ONLY ALERT

#### 업비트 연동 텔레그램 봇 알림

- [x] UPBIT API KEY 설정
- [x] TELEGRAM BOT 설정
- [x] Command 종류 구성
- [x] Price Info Alert ON, OFF 구성
- [x] Price Info (add, del, list) 구성
- [x] Upbit Asset Connect
- [x] Price Info Upbit Connect
- [x] httpx Connect
- [x] Price Info Trace Auto Alert Setting
- [ ] Price Info Trace Auto Alert Time Setting(delete)

#### STEP

git clone https://github.com/pozuhtuhv/bot_upbit_telegram.git

folder -> New file -> '.env'
```
UPBIT_ACCESS_KEY = 'YOUR_UPBIT_ACCESS_KEY'
UPBIT_SECRET_KEY = 'YOUR_UPBIT_SECRET_KEY'
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_TOKEN'
ROOM_ID = 'YOUR_ROOM_ID'
HTTP = 'https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates' -> YOUR_ROOM_ID_CONFIRM
```

```
ROOM_ID_CONFIRM
{
    "ok": true,
    "result": [
        {
            "update_id": ******,
            "message": {
                "message_id": ******,
                "from": {
                    "id": {ROOM_ID}, <--- THIS
```
AND
```
python -u bit_load.py
```