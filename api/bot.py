import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

# 이미 처리한 update_id를 추적하여 중복 응답을 방지
processed_update_ids = set()

class handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.state = {}  # 사용자 진행 상태를 저장하는 변수
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """GET 요청 처리 - 헬스체크 및 상품 목록"""
        try:
            path = urllib.parse.urlparse(self.path).path
            if path == '/products':
                products = self.get_products()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'products': products}).encode())
                return

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

            update_id = update_data.get('update_id')
            if update_id in processed_update_ids:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ignored', 'message': 'Duplicate update'}).encode())
                return
            
            # 메시지 처리
            if 'message' in update_data:
                success = self.handle_message(bot_token, update_data['message'])
                if success:
                    processed_update_ids.add(update_id)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'message': 'Message sent'}).encode())
                else:
                    self.send_error(500, 'Failed to send message')
            else:
                # 메시지가 없는 경우도 성공으로 처리
                processed_update_ids.add(update_id)
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
            
            # 상품 등록 시작
            if text.lower() == '/sell':
                self.start_product_registration(bot_token, chat_id)
                return True

            # 상품 목록 요청 처리
            if text.lower() == '/products':
                products = self.get_products()  # 데이터베이스에서 상품 목록 가져오기
                product_list = "\n".join([f"{product['title']} - {product['price']}원" for product in products])
                reply = f"상품 목록:\n{product_list}"
                self.send_message(bot_token, chat_id, reply)
                return True

            # 상품 검색 처리
            if text.lower().startswith('/search'):
                parts = text.split(maxsplit=1)
                if len(parts) == 1:
                    self.send_message(bot_token, chat_id, '사용법: /search 검색어')
                else:
                    keyword = parts[1]
                    results = self.search_products(keyword)
                    if results:
                        result_list = "\n".join([f"{p['title']} - {p['price']}원" for p in results])
                        reply = f"검색 결과:\n{result_list}"
                    else:
                        reply = '검색 결과가 없습니다.'
                    self.send_message(bot_token, chat_id, reply)
                return True

            reply = self.create_reply(text)
            self.send_message(bot_token, chat_id, reply)
        
        except Exception as e:
            print(f"Message handling error: {e}")
            return False

    def start_product_registration(self, bot_token, chat_id):
        """상품 등록 프로세스 시작"""
        self.send_message(bot_token, chat_id, "상품 등록을 시작합니다. 상품명을 입력해주세요.")
        self.state[chat_id] = {"step": "name"}  # 사용자가 진행 중인 단계 추적

    def process_product_registration(self, bot_token, chat_id, text):
        """상품 등록 처리"""
        step = self.state[chat_id].get("step", "")

        if step == "name":
            self.state[chat_id]["name"] = text
            self.send_message(bot_token, chat_id, "가격을 입력해주세요.")
            self.state[chat_id]["step"] = "price"

        elif step == "price":
            self.state[chat_id]["price"] = text
            self.send_message(bot_token, chat_id, "상품 설명을 입력해주세요.")
            self.state[chat_id]["step"] = "description"

        elif step == "description":
            self.state[chat_id]["description"] = text
            self.send_message(bot_token, chat_id, "거래 위치를 입력해주세요.")
            self.state[chat_id]["step"] = "location"

        elif step == "location":
            self.state[chat_id]["location"] = text
            self.finalize_product_registration(bot_token, chat_id)

    def finalize_product_registration(self, bot_token, chat_id):
        """상품 등록 완료 및 데이터베이스에 저장"""
        product = self.state[chat_id]
        
        # 여기에서 상품을 데이터베이스에 저장하는 코드를 작성해야 합니다.
        # 예시: self.save_to_database(product)
        
        self.send_message(bot_token, chat_id, f"상품 등록이 완료되었습니다!\n"
                                               f"상품명: {product['name']}\n"
                                               f"가격: {product['price']}원\n"
                                               f"설명: {product['description']}\n"
                                               f"위치: {product['location']}")
        
        del self.state[chat_id]  # 등록 종료 후 상태 삭제

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

    def get_products(self):
        """샘플 상품 목록 반환"""
        # 실제 데이터베이스 연결을 통해 상품을 가져오는 방식으로 구현해야 함
        return [
            {"title": "iPhone 15 Pro", "price": 1200000},
            {"title": "나이키 에어맥스", "price": 150000},
            {"title": "클린 코드 도서", "price": 25000}
        ]

    def search_products(self, keyword):
        """키워드로 상품 검색"""
        keyword_lower = keyword.lower()
        return [
            product for product in self.get_products()
            if keyword_lower in product['title'].lower()
        ]
    
    def create_reply(self, user_text):
        """사용자 입력에 따른 응답 생성"""
        user_text = user_text.strip()
        
        responses = {
            '/start': '''🎉 안녕하세요! 텔레그램 마켓플레이스 봇입니다.

/help 명령어로 사용법을 확인하세요!''',
            
            '/help': '''📋 사용 가능한 명령어:

🚀 /start - 봇 시작
❓ /help - 도움말
🛒 /products - 상품 목록
🔎 /search 키워드 - 상품 검색
➕ /sell - 상품 등록

더 많은 기능이 곧 추가됩니다!'''
        }
        
        return responses.get(user_text, f'''❓ "{user_text}"는 알 수 없는 명령어입니다.

/help를 입력해서 사용 가능한 명령어를 확인하세요.''')
