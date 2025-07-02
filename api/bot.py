import json
import os
import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경변수에서 토큰 가져오기
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set")

# 봇 인스턴스 생성
bot = Bot(token=TOKEN) if TOKEN else None

# 명령어 핸들러
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    try:
        await update.message.reply_text('안녕하세요! 텔레그램 마켓플레이스 봇입니다.')
        logger.info("Start command executed successfully")
    except Exception as e:
        logger.error(f"Error in start command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    try:
        help_text = """
사용 가능한 명령어:
/start - 봇 시작
/help - 도움말 보기
"""
        await update.message.reply_text(help_text)
        logger.info("Help command executed successfully")
    except Exception as e:
        logger.error(f"Error in help command: {e}")

# Vercel에서 요구하는 핸들러 함수
def handler(request):
    """Main handler for Vercel serverless function"""
    import asyncio
    
    try:
        # 환경변수 체크
        if not TOKEN:
            logger.error("Bot token not configured")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Bot token not configured'})
            }
        
        # GET 요청 처리 (헬스체크용)
        if request.method == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'Bot is running', 'method': 'GET'})
            }
        
        # POST 요청만 처리
        if request.method != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # 요청 본문 처리
        if hasattr(request, 'get_json'):
            body = request.get_json()
        elif hasattr(request, 'json'):
            body = request.json
        else:
            try:
                body = json.loads(request.body)
            except:
                body = json.loads(request.data.decode('utf-8'))
        
        if not body:
            logger.warning("Empty request body")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Empty request body'})
            }
        
        logger.info(f"Received update: {body}")
        
        # 비동기 처리
        async def process_update():
            try:
                # 텔레그램 업데이트 객체 생성
                update = Update.de_json(body, bot)
                
                if not update:
                    logger.warning("Invalid update object")
                    return False
                
                # Application 인스턴스 생성
                application = Application.builder().token(TOKEN).build()
                
                # 핸들러 등록
                application.add_handler(CommandHandler("start", start))
                application.add_handler(CommandHandler("help", help_command))
                
                # 업데이트 처리
                await application.process_update(update)
                logger.info("Update processed successfully")
                return True
                
            except Exception as e:
                logger.error(f"Error in process_update: {e}")
                return False
        
        # 이벤트 루프 실행
        try:
            # 새 이벤트 루프 생성
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(process_update())
            loop.close()
        except Exception as e:
            logger.error(f"Event loop error: {e}")
            success = False
        
        if success:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'ok'})
            }
        else:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Failed to process update'})
            }
        
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# 기본 엔트리포인트 (Vercel이 찾는 함수명)
def main(request):
    """Entry point for Vercel"""
    return handler(request)