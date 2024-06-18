import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# .env 파일 활성화
load_dotenv()

UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ROOM_ID = os.getenv('ROOM_ID')

# Chat info 명령어 진행
class TelegramBotHandler:
    
    @classmethod
    async def info(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # 명령어 뒤에 입력된 인수를 받아옵니다.
        args = context.args
        if args:
            msg = f"info: {' '.join(args)}"
        else:
            msg = "info가 입력되지 않았습니다. '/info <내용>' 형식으로 입력해주세요."
        await update.message.reply_text(msg)

# 명령어 인식
def main():
    try:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler('info', TelegramBotHandler.info))
        application.run_polling()
    except KeyboardInterrupt:
        return True

if __name__ == '__main__':
    main()