import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """GET 요청 처리 - 헬스체크"""
        try:
            response_data = {
                'status': 'Bot is running!',
                'message': 'Telegram marketplace bot is alive'
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"GET error: {e}")
            self.send_error(500, f'Server error: {str(e)}')

    def do_POST(self):
        """POST 요청 처리 - 웹훅"""
        try:
            # 봇 토큰 확인
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            if not bot_token:
                print("ERROR: TELEGRAM_BOT_TOKEN not found")
                self.send_error(500, 'Bot token not configured')
                return
            
            # 요청 본문 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, 'Empty request body')
                return
                
            body = self.rfile.read(content_length).decode('utf-8')
            
            # JSON 파싱
            try:
                update_data = json.loads(body)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                self.send_error(400, 'Invalid JSON format')
                return
            
            print(f"Received update: {json.dumps(update_data, indent=2)}")
            
            # 메시지 처리
            if 'message' in update_data:
                success = self.handle_message(bot_token, update_data['message'])
                if success:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'message': 'Message sent'}).encode())
                else:
                    self.send_error(500, 'Failed to send message')
            else:
                # 메시지가 없는 경우도 성공으로 처리
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'message': 'Update processed'}).encode())
                
        except Exception as e:
            print(f"POST error: {e}")
            self.send_error(500, f'Processing error: {str(e)}')

    def handle_message(self, bot_token, message):
        """메시지 처리 및 응답"""
        try:
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            if not chat_id:
                return False
            
            print(f"Processing message '{text}' from chat {chat_id}")
            
            # 응답 메시지 생성
            reply = self.create_reply(text)
            
            # 텔레그램으로 메시지 전송
            return self.send_message(bot_token, chat_id, reply)
            
        except Exception as e:
            print(f"Message handling error: {e}")
            return False

    def create_reply(self, user_text):
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

    def send_message(self, bot_token, chat_id, text):
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