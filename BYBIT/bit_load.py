import asyncio
import os
import time

# 따로 보는게 맞을거같아서 모듈 완전 분리
from backend.get_info import get_info
from backend.get_myasset import get_myasset
from backend.get_priceadd import get_priceadd
from backend.get_pricedel import get_pricedel
from backend.get_pricetrace import get_pricetrace
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# .env 파일 활성화
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

price_running = False
price_list = []
timeset = 10 # default 10sec

# Chat info 명령어 진행
class TelegramBotHandler:
    
    @classmethod
    async def command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(time.strftime('%y-%m-%d %H:%M:%S'), 'Command List')
        msg = '''Upbit 코인 알림 봇입니다.
/command - 커맨드 정보
/pricetrace - 가격 정보 알림 / default 10초
/pricelist - 불러올 코인 리스트
/priceadd - 불러올 코인 리스트에 추가
/pricedel - 불러올 코인 리스트에 삭제
        '''
        await update.message.reply_text(msg)

    # # 가격정보 간격 조정 (불안정)
    # @classmethod
    # async def pricetracetimeset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     global timeset
    #     print(time.strftime('%y-%m-%d %H:%M:%S'), 'Upbit Price Time Set Command')
    #     args = context.args
    #     if args:
    #         settime = int(args[0])
    #         if settime >= 10:
    #             timeset = settime
    #             await update.message.reply_text(f'{timeset}초 설정완료')
    #         else:
    #             await update.message.reply_text('10초 보다는 큰 숫자여야합니다.')
    #     else:
    #         await update.message.reply_text(f'현재 설정된 값 {timeset}')

    # 가격정보 불러오기
    @classmethod
    async def pricetrace(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                await update.message.reply_text(f'설정된 시간 {timeset}')
                asyncio.create_task(self.send_price_updates(update, context))
        else:
            await update.message.reply_text('ON, OFF 명령어로 작성해주세요')

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
        # 코드 실행 확인
        print("Telegram Bot Run")
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler('command', TelegramBotHandler.command)) # 완료
        app.add_handler(CommandHandler('pricetrace', TelegramBotHandler.pricetrace))
        # app.add_handler(CommandHandler('pricetracetimeset', TelegramBotHandler.pricetracetimeset)) # 불안정
        app.add_handler(CommandHandler('priceadd', TelegramBotHandler.priceadd)) # 완료
        app.add_handler(CommandHandler('pricedel', TelegramBotHandler.pricedel)) # 완료
        app.add_handler(CommandHandler('pricelist', TelegramBotHandler.pricelist)) # 완료
        app.run_polling()
    except KeyboardInterrupt:
        return True

if __name__ == '__main__':
    main()