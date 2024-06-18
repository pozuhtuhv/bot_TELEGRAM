import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from backend.info import info  # info 함수 직접 import
from backend.price import price  # price 함수 직접 import

# .env 파일 활성화
load_dotenv()

UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

price_running = False

# Chat info 명령어 진행
class TelegramBotHandler:
    
    @classmethod
    async def command(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = '''* command info
         - /price ON : 가격 정보 시작
         - /price OFF : 가격 정보 중지
         - /info <CODE> : 코인 가격 정보
        '''
        await update.message.reply_text(msg)

    # 계좌정보 불러오기
    @classmethod
    async def info(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = info(context)
        await update.message.reply_text(msg)

    # 가격정보 불러오기
    @classmethod
    async def price(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        application.run_polling()
    except KeyboardInterrupt:
        return True

if __name__ == '__main__':
    main()