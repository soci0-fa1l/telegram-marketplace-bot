import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

# Vercel에서 사용할 메인 핸들러 함수
def handler(request):
    """Vercel용 핸들러 함수"""
    # GET 요청 처리
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'Bot is alive!', 
                'method': 'GET',
                'message': 'Telegram bot is running on Vercel'
            })
        }
    
    # POST 요청 처리 (웹훅)
    elif request.method == 'POST':
        try:
            # 환경변수에서 토큰 가져오기
            token = os.environ.get('TELEGRAM_BOT_TOKEN')
            if not token:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Bot token not configured'})
                }
            
            # 요청 본문 읽기
            if hasattr(request, 'body'):
                body = request.body
            else:
                body = request.get_body()
            
            if not body:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Empty request body'})
                }
            
            # JSON 파싱
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            update = json.loads(body)
            
            # 메시지 처리
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')
                
                # 응답 메시지 결정
                reply_text = get_reply_text(text)
                
                # 텔레그램으로 메시지 전송
                success = send_telegram_message(token, chat_id, reply_text)
                
                if success:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'status': 'ok', 'message': 'Message sent successfully'})
                    }
                else:
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Failed to send message'})
                    }
            else:
                # 메시지가 없는 업데이트 (정상 처리)
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'status': 'ok', 'message': 'Update processed'})
                }
                
        except json.JSONDecodeError as e:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Invalid JSON: {str(e)}'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Internal error: {str(e)}'})
            }
    
    # 지원하지 않는 메서드
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'})
        }

def get_reply_text(text):
    """메시지에 따른 응답 텍스트 반환"""
    if text == '/start':
        return '🎉 안녕하세요! 텔레그램 마켓플레이스 봇입니다.\n\n사용법을 보려면 /help를 입력하세요.'
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
        return f'❓ "{text}"는 알 수 없는 명령어입니다.\n\n사용 가능한 명령어를 보려면 /help를 입력하세요.'

def send_telegram_message(token, chat_id, text):
    """텔레그램 API로 메시지 전송"""
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = {
            'chat_id': str(chat_id),
            'text': text,
            'parse_mode': 'HTML'
        }
        
        # POST 데이터 인코딩
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        
        # HTTP 요청 생성
        req = urllib.request.Request(
            url, 
            data=encoded_data, 
            method='POST'
        )
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        # 요청 실행
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('ok', False)
            
    except Exception as e:
        print(f"Error sending message: {e}")
        return False