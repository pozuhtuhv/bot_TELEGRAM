### bot_bybit_telegram (~ ing)

### NOT BUY, NOT SELL, JUST ONLY ALERT

#### 바이비트 연동 텔레그램 봇 알림

- [x] TELEGRAM BOT 설정
- [x] Command 종류 구성
- [ ] Price Info Alert ON, OFF 구성
- [ ] Price Info (add, del, list) 구성
- [ ] Price Info Trace Auto Alert Setting
- [ ] Price Info Trace Auto Alert Time Setting(delete)

#### STEP

git clone https://github.com/pozuhtuhv/bot_TELEGRAM.git

folder -> New file -> '.env'
```
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
pip install -r requirements.txt
python -u bit_load.py
```