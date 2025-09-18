#!/usr/bin/env python3
"""
HTTP 서버 구현
우주 해적 소개 웹페이지를 제공하는 HTTP 서버
"""

import http.server
import socketserver
import datetime
import json
import urllib.request
import urllib.parse
import socket
import threading
import time


class PirateServer(http.server.SimpleHTTPRequestHandler):
    """우주 해적 웹페이지를 제공하는 HTTP 서버 핸들러"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """GET 요청 처리"""
        try:
            # 접속 로그 출력
            self.log_access()
            
            # 200 OK 응답 헤더 전송
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Server', 'PirateServer/1.0')
            self.end_headers()
            
            # index.html 파일 읽기 및 전송
            self.serve_index_html()
            
        except Exception as e:
            print(f'요청 처리 중 오류 발생: {e}')
            self.send_error(500, 'Internal Server Error')
    
    def serve_index_html(self):
        """index.html 파일을 읽어서 클라이언트에게 전송"""
        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
                self.wfile.write(html_content.encode('utf-8'))
        except FileNotFoundError:
            error_html = self.get_error_html('index.html 파일을 찾을 수 없습니다.')
            self.wfile.write(error_html.encode('utf-8'))
        except Exception as e:
            error_html = self.get_error_html(f'파일 읽기 오류: {e}')
            self.wfile.write(error_html.encode('utf-8'))
    
    def get_error_html(self, error_message):
        """오류 발생 시 표시할 HTML 생성"""
        return f'''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>오류 발생</title>
        </head>
        <body>
            <h1>🚨 오류 발생</h1>
            <p>{error_message}</p>
            <p>서버 관리자에게 문의하세요.</p>
        </body>
        </html>
        '''
    
    def log_access(self):
        """접속 로그 출력"""
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        print(f'[{current_time}] 접속 - IP: {client_ip}')
        print(f'  User-Agent: {user_agent}')
        print(f'  요청 경로: {self.path}')
        print('-' * 50)
        
        # IP 기반 위치 정보 조회 (보너스 기능)
        self.get_location_info(client_ip)
    
    def get_location_info(self, ip_address):
        """IP 주소 기반 위치 정보 조회 (보너스 기능)"""
        try:
            # 로컬 IP인지 확인
            if ip_address in ['127.0.0.1', '::1', 'localhost']:
                print(f'  위치: 로컬호스트 (개발 환경)')
                return
            
            # 외부 IP인 경우 위치 정보 조회
            if not self.is_private_ip(ip_address):
                location_info = self.fetch_ip_location(ip_address)
                if location_info:
                    print(f'  위치: {location_info}')
                else:
                    print(f'  위치: 정보를 가져올 수 없음')
            else:
                print(f'  위치: 사설 네트워크')
                
        except Exception as e:
            print(f'  위치 정보 조회 오류: {e}')
    
    def is_private_ip(self, ip_address):
        """사설 IP 주소인지 확인"""
        try:
            ip = ip_address.split('.')
            if len(ip) == 4:
                first_octet = int(ip[0])
                # 사설 IP 대역 확인
                if (first_octet == 10 or 
                    (first_octet == 172 and 16 <= int(ip[1]) <= 31) or
                    (first_octet == 192 and int(ip[1]) == 168)):
                    return True
            return False
        except:
            return False
    
    def fetch_ip_location(self, ip_address):
        """IP 주소로부터 위치 정보 조회"""
        try:
            # ip-api.com 서비스 사용 (무료, 제한 있음)
            url = f'http://ip-api.com/json/{ip_address}'
            
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('status') == 'success':
                    country = data.get('country', 'Unknown')
                    region = data.get('regionName', 'Unknown')
                    city = data.get('city', 'Unknown')
                    isp = data.get('isp', 'Unknown')
                    
                    location = f'{country}'
                    if region != 'Unknown' and region != country:
                        location += f', {region}'
                    if city != 'Unknown' and city != region:
                        location += f', {city}'
                    
                    return f'{location} (ISP: {isp})'
                else:
                    return None
                    
        except Exception as e:
            print(f'  위치 정보 API 오류: {e}')
            return None


class SpacePirateServer:
    """우주 해적 웹서버 메인 클래스"""
    
    def __init__(self, port=8080, host='localhost'):
        """
        서버 초기화
        
        Args:
            port (int): 서버 포트 번호
            host (str): 서버 호스트 주소
        """
        self.port = port
        self.host = host
        self.server = None
        self.server_thread = None
        self.running = False
    
    def start_server(self):
        """서버 시작"""
        try:
            # HTTP 서버 생성
            self.server = socketserver.TCPServer((self.host, self.port), PirateServer)
            self.running = True
            
            print('=' * 60)
            print('🏴‍☠️  우주 해적 웹서버 시작! 🏴‍☠️')
            print('=' * 60)
            print(f'서버 주소: http://{self.host}:{self.port}')
            print(f'시작 시간: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            print('=' * 60)
            print('웹 브라우저에서 위 주소로 접속하세요!')
            print('서버를 종료하려면 Ctrl+C를 누르세요.')
            print('=' * 60)
            
            # 서버 실행
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print('\n\n서버를 종료합니다...')
            self.stop_server()
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f'오류: 포트 {self.port}이 이미 사용 중입니다.')
                print('다른 포트를 사용하거나 기존 서버를 종료하세요.')
            else:
                print(f'서버 시작 오류: {e}')
        except Exception as e:
            print(f'예상치 못한 오류: {e}')
        finally:
            self.running = False
    
    def stop_server(self):
        """서버 종료"""
        self.running = False
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        print('서버가 종료되었습니다.')


def main():
    """메인 함수"""
    print('우주 해적 웹서버를 시작합니다...')
    
    # 서버 생성 및 시작
    server = SpacePirateServer(port=8080, host='localhost')
    server.start_server()


if __name__ == '__main__':
    main()
