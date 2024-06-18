import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from backend.info import info  # info 함수 직접 import
from backend.price import price  # price 함수 직접 import
import time

# .env 파일 활성화
load_dotenv()

UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

price_running = False
price_list = []

# Chat info 명령어 진행
class TelegramBotHandler:
    
    @classmethod
    async def command(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Command List')
        msg = '''command info
command - 커맨드 정보
price - 가격 정보 알림
info - 코인 가격 정보
pricelist - 불러올 코인 리스트
priceadd - 불러올 코인 리스트에 추가
pricedel - 불러올 코인 리스트에 삭제
        '''
        await update.message.reply_text(msg)

    # 계좌정보 불러오기
    @classmethod
    async def info(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Upbit Info Load Command')
        msg = info(context)
        await update.message.reply_text(msg)

    @classmethod
    async def pricelist(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        global price_list
        await update.message.reply_text(f'현재 코인 확인 리스트:\n- ' + '\n- '.join(price_list))
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Command')

    @classmethod
    async def priceadd(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Add Command')
        global price_list
        args = context.args
        if args:
            coin = args[0]
            if coin not in price_list:
                price_list.append(coin)
                await update.message.reply_text(f'{coin} 코인을 리스트에 추가하였습니다.')
            else:
                await update.message.reply_text(f'{coin} 코인은 이미 리스트에 있습니다.')
            
            # 코인 리스트가 비어있지 않은 경우에만 리스트 출력
            if price_list:
                await asyncio.sleep(2)
                await update.message.reply_text(f'현재 코인 확인 리스트:\n- ' + '\n- '.join(price_list))
        else:
            await update.message.reply_text('추가할 코인의 코드를 입력하세요.')

    @classmethod
    async def pricedel(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Coin List Del Command')
        global price_list
        args = context.args
        if args:
            coin = args[0]
            if coin in price_list:
                price_list.remove(coin)
                await update.message.reply_text(f'{coin} 코인을 리스트에서 삭제하였습니다.')
            else:
                await update.message.reply_text(f'{coin} 코인은 리스트에 없습니다.')
            
            # 코인 리스트가 비어있지 않은 경우에만 리스트 출력
            if price_list:
                await asyncio.sleep(2)
                await update.message.reply_text(f'현재 코인 확인 리스트:\n- ' + '\n- '.join(price_list))
        else:
            await update.message.reply_text('삭제할 코인의 코드를 입력하세요.')

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

    @classmethod
    async def send_price_updates(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        global price_running
        while price_running:
            msg = price(context.args)
            await update.message.reply_text(msg)
            await asyncio.sleep(5)

# 명령어 인식
def main():
    try:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler('command', TelegramBotHandler.command))
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