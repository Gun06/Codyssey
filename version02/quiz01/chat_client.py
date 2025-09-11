#!/usr/bin/env python3
"""
TCP/IP 소켓 채팅 클라이언트
서버에 연결하여 다른 클라이언트들과 메시지를 주고받을 수 있습니다.
"""

import socket
import threading
import sys


class ChatClient:
    """채팅 클라이언트 클래스"""
    
    def __init__(self, host='localhost', port=12345):
        """
        클라이언트 초기화
        
        Args:
            host (str): 서버 호스트 주소
            port (int): 서버 포트 번호
        """
        self.host = host
        self.port = port
        self.socket = None
        self.name = None
        self.running = False
    
    def connect_to_server(self):
        """서버에 연결"""
        try:
            # 소켓 생성 및 서버 연결
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # 서버로부터 이름 입력 요청 수신
            name_prompt = self.socket.recv(1024).decode('utf-8')
            print(name_prompt, end='')
            
            # 이름 입력
            self.name = input()
            self.socket.send(self.name.encode('utf-8'))
            
            print(f'\n{self.host}:{self.port}에 연결되었습니다.')
            print('메시지를 입력하세요. (종료: /종료, 귀속말: /st 사용자명 메시지)')
            print('-' * 50)
            
            self.running = True
            
            # 메시지 수신을 위한 쓰레드 시작
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # 메시지 전송
            self.send_messages()
            
        except ConnectionRefusedError:
            print('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.')
        except Exception as e:
            print(f'연결 중 오류가 발생했습니다: {e}')
        finally:
            self.disconnect()
    
    def receive_messages(self):
        """서버로부터 메시지 수신"""
        try:
            while self.running:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                # 메시지 출력
                print(f'\r{message}')
                print(f'{self.name}> ', end='', flush=True)
                
        except ConnectionResetError:
            print('\n서버와의 연결이 끊어졌습니다.')
        except Exception as e:
            print(f'\n메시지 수신 중 오류: {e}')
        finally:
            self.running = False
    
    def send_messages(self):
        """사용자 입력 메시지 전송"""
        try:
            while self.running:
                message = input(f'{self.name}> ')
                
                if not self.running:
                    break
                
                if message == '/종료':
                    self.socket.send(message.encode('utf-8'))
                    break
                
                self.socket.send(message.encode('utf-8'))
                
        except KeyboardInterrupt:
            print('\n클라이언트를 종료합니다...')
            self.socket.send('/종료'.encode('utf-8'))
        except Exception as e:
            print(f'메시지 전송 중 오류: {e}')
        finally:
            self.running = False
    
    def disconnect(self):
        """서버 연결 해제"""
        self.running = False
        if self.socket:
            self.socket.close()


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'
    
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = 12345
    
    client = ChatClient(host, port)
    client.connect_to_server()


if __name__ == '__main__':
    main()
