import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """GET 요청 핸들러 - 헬스체크"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = json.dumps({
            'status': 'Bot is alive!', 
            'method': 'GET',
            'message': 'Telegram bot is running on Vercel'
        })
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        """POST 요청 핸들러 - 웹훅"""
        try:
            # 환경변수에서 토큰 가져오기
            token = os.environ.get('TELEGRAM_BOT_TOKEN')
            if not token:
                self.send_error(500, 'Bot token not configured')
                return
            
            # 요청 본문 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, 'Empty request body')
                return
                
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data.decode('utf-8'))
            
            # 메시지 처리
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')
                
                # 응답 메시지 결정
                if text == '/start':
                    reply_text = '🎉 안녕하세요! 텔레그램 마켓플레이스 봇입니다.\n\n사용법을 보려면 /help를 입력하세요.'
                elif text == '/help':
                    reply_text = '''📋 사용 가능한 명령어:

🚀 /start - 봇 시작하기
❓ /help - 도움말 보기
🛒 /products - 상품 목록 보기 (준비중)
➕ /sell - 상품 등록하기 (준비중)

더 많은 기능이 곧 추가될 예정입니다!'''
                elif text == '/products':
                    reply_text = '🛒 상품 목록 기능은 준비 중입니다. 곧 만나보세요!'
                elif text == '/sell':
                    reply_text = '➕ 상품 등록 기능은 준비 중입니다. 곧 만나보세요!'
                else:
                    reply_text = f'❓ "{text}"는 알 수 없는 명령어입니다.\n\n사용 가능한 명령어를 보려면 /help를 입력하세요.'
                
                # 텔레그램으로 메시지 전송
                success = self.send_telegram_message(token, chat_id, reply_text)
                
                if success:
                    # 성공 응답
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'status': 'ok', 'message': 'Message sent successfully'})
                    self.wfile.write(response.encode('utf-8'))
                else:
                    self.send_error(500, 'Failed to send message')
            else:
                # 메시지가 없는 업데이트 (정상 처리)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'status': 'ok', 'message': 'Update processed'})
                self.wfile.write(response.encode('utf-8'))
                
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')
        except Exception as e:
            self.send_error(500, f'Internal error: {str(e)}')

    def send_telegram_message(self, token, chat_id, text):
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

    def send_error(self, code, message):
        """에러 응답 전송"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = json.dumps({'error': message, 'code': code})
        self.wfile.write(response.encode('utf-8'))

    def log_message(self, format, *args):
        """로그 메시지 (Vercel 로그에 출력)"""
        print(f"[{self.address_string()}] {format % args}")