import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
from backend.info import info  # info 함수 직접 import

# .env 파일 활성화
load_dotenv()

UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ROOM_ID = os.getenv('ROOM_ID')

# Chat info 명령어 진행
class TelegramBotHandler:
    
    @classmethod
    async def command(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = '''* command info
         - /price : 계좌 정보
         - /info <CODE> : 코인 가격
        '''
        await update.message.reply_text(msg)

    # 계좌정보 불러오기
    @classmethod
    async def info(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = info(context)
        await update.message.reply_text(msg)

# 명령어 인식
def main():
    try:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler('command', TelegramBotHandler.command))
        application.add_handler(CommandHandler('info', TelegramBotHandler.info))
        application.run_polling()
    except KeyboardInterrupt:
        return True

if __name__ == '__main__':
    main()