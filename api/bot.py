import json
import os
import urllib.request
import urllib.parse

def handler(request, context):
    """
    Vercel용 서버리스 함수
    request: 요청 객체
    context: 컨텍스트 객체
    """
    try:
        # GET 요청 처리 (헬스체크)
        if request.method == 'GET':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'status': 'Bot is alive!', 
                    'method': 'GET',
                    'message': 'Telegram bot is running on Vercel'
                })
            }
        
        # POST 요청 처리 (텔레그램 웹훅)
        elif request.method == 'POST':
            return handle_webhook(request)
        
        # 다른 메서드는 허용하지 않음
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        print(f"Handler error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }

def handle_webhook(request):
    """텔레그램 웹훅 처리"""
    try:
        # 환경변수에서 봇 토큰 가져오기
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not token:
            print("ERROR: Bot token not found in environment variables")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Bot token not configured'})
            }
        
        # 요청 본문 읽기
        try:
            if hasattr(request, 'body'):
                body = request.body
            elif hasattr(request, 'data'):
                body = request.data
            else:
                body = request.get_data()
            
            # 바이트를 문자열로 변환
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            if not body:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Empty request body'})
                }
            
            # JSON 파싱
            update = json.loads(body)
            print(f"Received update: {update}")
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Invalid JSON: {str(e)}'})
            }
        
        # 메시지가 있는 업데이트 처리
        if 'message' in update and 'text' in update['message']:
            message = update['message']
            chat_id = message['chat']['id']
            text = message['text']
            
            print(f"Processing message: {text} from chat: {chat_id}")
            
            # 응답 메시지 생성
            reply_text = get_reply_message(text)
            
            # 텔레그램으로 메시지 전송
            success = send_telegram_message(token, chat_id, reply_text)
            
            if success:
                print("Message sent successfully")
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'status': 'ok', 'message': 'Message sent successfully'})
                }
            else:
                print("Failed to send message")
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Failed to send message'})
                }
        else:
            # 메시지가 없는 업데이트도 정상 처리
            print("Update without text message - processed")
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'ok', 'message': 'Update processed'})
            }
            
    except Exception as e:
        print(f"Webhook handling error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal error: {str(e)}'})
        }

def get_reply_message(text):
    """사용자 메시지에 따른 응답 생성"""
    text = text.strip()
    
    if text == '/start':
        return '''🎉 안녕하세요! 텔레그램 마켓플레이스 봇입니다.

사용법을 보려면 /help를 입력하세요.'''
    
    elif text == '/help':
        return '''📋 사용 가능한 명령어:

🚀 /start - 봇 시작하기
❓ /help - 도움말 보기
🛒 /products - 상품 목록 보기 (준비중)
➕ /sell - 상품 등록하기 (준비중)

더 많은 기능이 곧 추가될 예정입니다!'''
    
    elif text == '/products':
        return '🛒 상품 목록 기능은 준비 중입니다. 곧 만나보세요!'
    
    elif text == '/sell':
        return '➕ 상품 등록 기능은 준비 중입니다. 곧 만나보세요!'
    
    else:
        return f'''❓ "{text}"는 알 수 없는 명령어입니다.

사용 가능한 명령어를 보려면 /help를 입력하세요.'''

def send_telegram_message(token, chat_id, text):
    """텔레그램 API를 통해 메시지 전송"""
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        
        # 전송할 데이터 준비
        data = {
            'chat_id': str(chat_id),
            'text': text,
            'parse_mode': 'HTML'
        }
        
        # URL 인코딩
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        
        # HTTP 요청 생성
        request = urllib.request.Request(
            url,
            data=encoded_data,
            method='POST'
        )
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        # 요청 실행
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                print(f"Message sent successfully to chat {chat_id}")
                return True
            else:
                print(f"Telegram API error: {result}")
                return False
                
    except Exception as e:
        print(f"Error sending telegram message: {str(e)}")
        return False