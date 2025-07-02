import json
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# 환경변수에서 토큰 가져오기
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# 봇 인스턴스 생성
bot = Bot(token=TOKEN)

# 명령어 핸들러
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    await update.message.reply_text('안녕하세요! 텔레그램 마켓플레이스 봇입니다.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
사용 가능한 명령어:
/start - 봇 시작
/help - 도움말 보기
"""
    await update.message.reply_text(help_text)

# Vercel 핸들러 함수
async def handler(request):
    """Main handler for Vercel serverless function"""
    try:
        # POST 요청만 처리
        if request.method != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # 요청 본문 파싱
        body = await request.json() if hasattr(request, 'json') else json.loads(request.body)
        
        # 텔레그램 업데이트 객체 생성
        update = Update.de_json(body, bot)
        
        # Application 인스턴스 생성
        application = Application.builder().token(TOKEN).build()
        
        # 핸들러 등록
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        # 업데이트 처리
        await application.process_update(update)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ok'})
        }
        
    except Exception as e:
        print(f"Error processing update: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Vercel에서 요구하는 기본 핸들러 (동기 버전)
def main(request):
    """Synchronous wrapper for the async handler"""
    import asyncio
    
    # 이벤트 루프가 이미 실행 중인지 확인
    try:
        loop = asyncio.get_running_loop()
        # 이미 실행 중인 경우 새 태스크로 실행
        return loop.run_until_complete(handler(request))
    except RuntimeError:
        # 실행 중인 루프가 없는 경우 새로 생성
        return asyncio.run(handler(request))