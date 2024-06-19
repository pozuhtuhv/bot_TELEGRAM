import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from backend.info import info
from backend.price import price
from backend.priceadd import priceadd
from backend.pricedel import pricedel
from backend.myasset import myasset
import time

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
    async def command(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Command List')
        msg = '''Upbit 코인 알림 봇입니다.
command - 커맨드 정보
myasset - 코인자산정보
info - 코인 현재 가격정보
price - 가격 정보 알림 / default 1분
priceset - 가격 정보 알림 시간 설정
pricelist - 불러올 코인 리스트
priceadd - 불러올 코인 리스트에 추가
pricedel - 불러올 코인 리스트에 삭제
        '''
        await update.message.reply_text(msg)

    # 자산정보 불러오기
    @classmethod
    async def myasset(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Upbit Info Load Command')
        msg = await myasset()
        await update.message.reply_text(msg)

    # 코인 현재 가격정보 불러오기
    @classmethod
    async def info(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Upbit Info Load Command')
        msg = await info(context)
        await update.message.reply_text(msg)

    # 가격정보 불러오기
    @classmethod
    async def price(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                asyncio.create_task(cls.send_price_updates(update, context))
        else:
            await update.message.reply_text('ON, OFF 명령어로 작성해주세요')

    @classmethod
    async def send_price_updates(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        global price_running
        while price_running:
            msg = await price(context.args, price_list)  # await 키워드 추가
            await update.message.reply_text(msg)
            await asyncio.sleep(timeset)

    # 가격정보 리스트
    @classmethod
    async def pricelist(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Command')
        global price_list
        if not price_list:
            await update.message.reply_text(f'현재 추가된 코인이 없습니다')
        else:
            await update.message.reply_text(f'현재 코인 확인 리스트:\n- ' + '\n- '.join(price_list))

    # 가격정보 리스트 추가
    @classmethod
    async def priceadd(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Add Command')
        await priceadd(update, context, price_list)


    # 가격정보 리스트 삭제
    @classmethod
    async def pricedel(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Del Command')
        await pricedel(update, context, price_list)

# 명령어 인식
def main():
    try:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler('command', TelegramBotHandler.command))
        application.add_handler(CommandHandler('myasset', TelegramBotHandler.myasset))
        application.add_handler(CommandHandler('info', TelegramBotHandler.info))
        application.add_handler(CommandHandler('price', TelegramBotHandler.price))
        application.add_handler(CommandHandler('priceadd', TelegramBotHandler.priceadd))
        application.add_handler(CommandHandler('pricedel', TelegramBotHandler.pricedel))
        application.add_handler(CommandHandler('pricelist', TelegramBotHandler.pricelist))
        application.run_polling()
    except KeyboardInterrupt:
        return True

if __name__ == '__main__':
    main()