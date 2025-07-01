import json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '8076554171:AAEsddV3TulkEXaSoktwCMxTLngcZxtP9qQ'  # 텔레그램 봇 토큰 입력

# 텔레그램 봇 처리 함수
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('안녕하세요! 텔레그램 마켓플레이스 봇입니다.')

def bot_handler(request):
    if request.method == 'POST':
        data = request.json
        update = Update.de_json(data, bot)
        bot.process_update(update)
        return json.dumps({"status": "ok"})
    return json.dumps({"status": "error"})

# 웹훅 설정 함수
def set_webhook():
    url = f'https://{Vercel_URL}/api/bot'
    webhook_url = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}'
    requests.get(webhook_url)

if __name__ == "__main__":
    bot = Updater(TOKEN)
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    
    bot.start_polling()
