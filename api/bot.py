import json
import os
import urllib.request
import urllib.parse

def handler(request):
    """
    Vercel 서버리스 함수 - 단일 매개변수만 사용
    """
    try:
        # 요청 메서드 확인
        method = getattr(request, 'method', 'GET')
        
        # GET 요청 - 헬스체크
        if method == 'GET':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'status': 'Bot is running!',
                    'message': 'Telegram marketplace bot is alive'
                })
            }
        
        # POST 요청 - 웹훅 처리
        elif method == 'POST':
            return process_webhook(request)
        
        # 기타 메서드
        else:
            return error_response(405, 'Method not allowed')
            
    except Exception as e:
        print(f"Main handler error: {e}")
        return error_response(500, f'Server error: {str(e)}')

def process_webhook(request):
    """텔레그램 웹훅 처리"""
    try:
        # 봇 토큰 확인
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            print("ERROR: TELEGRAM_BOT_TOKEN not found")
            return error_response(500, 'Bot token not configured')
        
        # 요청 본문 가져오기
        body = get_request_body(request)
        if not body:
            return error_response(400, 'Empty request body')
        
        # JSON 파싱
        try:
            update_data = json.loads(body)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return error_response(400, 'Invalid JSON format')
        
        print(f"Received update: {json.dumps(update_data, indent=2)}")
        
        # 메시지 처리
        if 'message' in update_data:
            return handle_message(bot_token, update_data['message'])
        else:
            # 메시지가 없는 경우도 성공으로 처리
            return success_response('Update processed (no message)')
            
    except Exception as e:
        print(f"Webhook processing error: {e}")
        return error_response(500, f'Processing error: {str(e)}')

def get_request_body(request):
    """요청 본문을 안전하게 가져오기"""
    try:
        # 다양한 방식으로 본문 가져오기 시도
        if hasattr(request, 'body'):
            body = request.body
        elif hasattr(request, 'data'):
            body = request.data  
        elif hasattr(request, 'get_data'):
            body = request.get_data()
        elif hasattr(request, 'read'):
            body = request.read()
        else:
            return None
        
        # 바이트를 문자열로 변환
        if isinstance(body, bytes):
            body = body.decode('utf-8')
            
        return body
        
    except Exception as e:
        print(f"Error getting request body: {e}")
        return None

def handle_message(bot_token, message):
    """메시지 처리 및 응답"""
    try:
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        
        if not chat_id:
            return error_response(400, 'No chat ID found')
        
        print(f"Processing message '{text}' from chat {chat_id}")
        
        # 응답 메시지 생성
        reply = create_reply(text)
        
        # 텔레그램으로 메시지 전송
        if send_message(bot_token, chat_id, reply):
            print("Message sent successfully")
            return success_response('Message sent')
        else:
            print("Failed to send message")
            return error_response(500, 'Failed to send message')
            
    except Exception as e:
        print(f"Message handling error: {e}")
        return error_response(500, f'Message handling error: {str(e)}')

def create_reply(user_text):
    """사용자 입력에 따른 응답 생성"""
    user_text = user_text.strip()
    
    responses = {
        '/start': '''🎉 안녕하세요! 텔레그램 마켓플레이스 봇입니다.

/help 명령어로 사용법을 확인하세요!''',
        
        '/help': '''📋 사용 가능한 명령어:

🚀 /start - 봇 시작
❓ /help - 도움말
🛒 /products - 상품 목록 (준비중)
➕ /sell - 상품 등록 (준비중)

더 많은 기능이 곧 추가됩니다!''',
        
        '/products': '🛒 상품 목록 기능을 준비 중입니다. 조금만 기다려주세요!',
        '/sell': '➕ 상품 등록 기능을 준비 중입니다. 조금만 기다려주세요!'
    }
    
    return responses.get(user_text, f'''❓ "{user_text}"는 알 수 없는 명령어입니다.

/help를 입력해서 사용 가능한 명령어를 확인하세요.''')

def send_message(bot_token, chat_id, text):
    """텔레그램 API로 메시지 전송"""
    try:
        api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        
        # 전송 데이터
        payload = {
            'chat_id': str(chat_id),
            'text': text
        }
        
        # URL 인코딩
        data = urllib.parse.urlencode(payload).encode('utf-8')
        
        # HTTP 요청
        req = urllib.request.Request(api_url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        # 요청 실행
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                print(f"✅ Message sent to chat {chat_id}")
                return True
            else:
                print(f"❌ Telegram API error: {result}")
                return False
                
    except Exception as e:
        print(f"❌ Send message error: {e}")
        return False

def success_response(message):
    """성공 응답 생성"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'status': 'success', 'message': message})
    }

def error_response(status_code, message):
    """에러 응답 생성"""
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'status': 'error', 'message': message})
    }