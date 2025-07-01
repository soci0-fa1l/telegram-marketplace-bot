import json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = 'YOUR_BOT_API_TOKEN'  # 텔레그램 봇 API 토큰

# 텔레그램 봇 처리 함수
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('안녕하세요! 텔레그램 마켓플레이스 봇입니다.')

# 웹훅 처리 함수
def bot_handler(request):
    if request.method == 'POST':
        data = request.json
        update = Update.de_json(data, bot)
        bot.process_update(update)
        return json.dumps({"status": "ok"})
    return json.dumps({"status": "error"})


# Vercel에서 사용되는 핸들러
def handler(request):
    # 요청을 bot_handler로 전달
    return bot_handler(request)
