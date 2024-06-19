import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import time
# 따로 보는게 맞을거같아서 모듈 완전 분리
from backend.get_info import get_info
from backend.get_price import get_price
from backend.get_priceadd import get_priceadd
from backend.get_pricedel import get_pricedel
from backend.get_myasset import get_myasset


# .env 파일 활성화
load_dotenv()

UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

price_running = False
price_list = []
timeset = 60 # default

# Chat info 명령어 진행
class TelegramBotHandler:
    
    @classmethod
    async def command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Command List')
        msg = '''Upbit 코인 알림 봇입니다.
command - 커맨드 정보
myasset - 코인자산정보
info - 코인 현재 가격정보 (ex. KRW-BTC, BTC-ETH)
price - 가격 정보 알림 / default 1분
priceset - 가격 정보 알림 시간 설정
pricelist - 불러올 코인 리스트
priceadd - 불러올 코인 리스트에 추가
pricedel - 불러올 코인 리스트에 삭제
        '''
        await update.message.reply_text(msg)

    # 자산정보 불러오기
    @classmethod
    async def myasset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Asset Load Command')
        SERVER_URL = 'https://api.upbit.com/v1/accounts'
        msg = await get_myasset(SERVER_URL, UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
        await update.message.reply_text(msg)

    # 코인 현재 가격정보 불러오기
    @classmethod
    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Upbit Info Load Command')
        SERVER_URL = 'https://api.upbit.com/v1/ticker'
        args = context.args
        code = args[0] if args else 'KRW-BTC'
        
        msg = await get_info(code, SERVER_URL)
        await update.message.reply_text('\n'.join(msg))

    # 가격정보 불러오기
    @classmethod
    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin info Command')
        global price_running
        args = context.args
        if args and args[0].upper() == 'OFF':
            price_running = False
            await update.message.reply_text('가격 정보 중지')
        elif args and args[0].upper() == 'ON':
            if not price_running:
                price_running = True
                await update.message.reply_text('가격 정보 시작')
                asyncio.create_task(self.send_price_updates(update, context))
        else:
            await update.message.reply_text('ON, OFF 명령어로 작성해주세요')

    @classmethod
    async def send_price_updates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        global price_running
        while price_running:
            msg = await get_price(context.args, price_list, UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)  # await 키워드 추가
            await update.message.reply_text(msg)
            await asyncio.sleep(timeset)

    # 가격정보 리스트
    @classmethod
    async def pricelist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Command')
        global price_list
        if not price_list:
            await update.message.reply_text(f'현재 추가된 코인이 없습니다')
        else:
            await update.message.reply_text(f'현재 코인 확인 리스트:\n- ' + '\n- '.join(price_list))

    # 가격정보 리스트 추가
    @classmethod
    async def priceadd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Add Command')
        await get_priceadd(update, context, price_list)


    # 가격정보 리스트 삭제
    @classmethod
    async def pricedel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Del Command')
        await get_pricedel(update, context, price_list)

# 명령어 인식
def main():
    try:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler('command', TelegramBotHandler.command)) # 완료
        application.add_handler(CommandHandler('myasset', TelegramBotHandler.myasset)) # 완료
        application.add_handler(CommandHandler('info', TelegramBotHandler.info))
        application.add_handler(CommandHandler('price', TelegramBotHandler.price))
        application.add_handler(CommandHandler('priceadd', TelegramBotHandler.priceadd)) # 완료
        application.add_handler(CommandHandler('pricedel', TelegramBotHandler.pricedel)) # 완료
        application.add_handler(CommandHandler('pricelist', TelegramBotHandler.pricelist)) # 완료
        application.run_polling()
    except KeyboardInterrupt:
        return True

if __name__ == '__main__':
    main()