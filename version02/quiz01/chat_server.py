#!/usr/bin/env python3
"""
멀티 쓰레드 TCP/IP 소켓 채팅 서버
여러 클라이언트와 동시에 통신하며 메시지를 브로드캐스트합니다.
"""

import socket
import threading
import sys


class ChatServer:
    """채팅 서버 클래스"""
    
    def __init__(self, host='localhost', port=12345):
        """
        서버 초기화
        
        Args:
            host (str): 서버 호스트 주소
            port (int): 서버 포트 번호
        """
        self.host = host
        self.port = port
        self.clients = []  # 연결된 클라이언트들의 리스트
        self.client_names = {}  # 클라이언트 소켓과 이름 매핑
        self.server_socket = None
        self.lock = threading.Lock()  # 쓰레드 동기화를 위한 락
        
    def start_server(self):
        """서버 시작"""
        try:
            # 소켓 생성
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f'서버가 {self.host}:{self.port}에서 시작되었습니다.')
            print('클라이언트 연결을 기다리는 중...')
            
            while True:
                # 클라이언트 연결 대기
                client_socket, client_address = self.server_socket.accept()
                print(f'클라이언트가 연결되었습니다: {client_address}')
                
                # 클라이언트 이름 입력 요청
                client_socket.send('이름을 입력하세요: '.encode('utf-8'))
                client_name = client_socket.recv(1024).decode('utf-8').strip()
                
                # 클라이언트 정보 저장
                with self.lock:
                    self.clients.append(client_socket)
                    self.client_names[client_socket] = client_name
                
                # 입장 메시지 브로드캐스트
                self.broadcast_message(f'{client_name}님이 입장하셨습니다.', client_socket)
                
                # 클라이언트 처리를 위한 쓰레드 시작
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_name)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print('\n서버를 종료합니다...')
            self.stop_server()
        except Exception as e:
            print(f'서버 오류: {e}')
            self.stop_server()
    
    def handle_client(self, client_socket, client_name):
        """
        클라이언트 메시지 처리
        
        Args:
            client_socket: 클라이언트 소켓
            client_name (str): 클라이언트 이름
        """
        try:
            while True:
                # 클라이언트로부터 메시지 수신
                message = client_socket.recv(1024).decode('utf-8').strip()
                
                if not message:
                    break
                
                # /종료 명령어 처리
                if message == '/종료':
                    self.remove_client(client_socket, client_name)
                    break
                
                # 귀속말 처리 (예: /st 사용자명 메시지)
                if message.startswith('/st '):
                    self.handle_whisper(client_socket, client_name, message)
                    continue
                
                # 일반 메시지 브로드캐스트
                formatted_message = f'{client_name}> {message}'
                self.broadcast_message(formatted_message, client_socket)
                
        except ConnectionResetError:
            print(f'{client_name}의 연결이 끊어졌습니다.')
        except Exception as e:
            print(f'{client_name} 처리 중 오류: {e}')
        finally:
            self.remove_client(client_socket, client_name)
    
    def handle_whisper(self, sender_socket, sender_name, message):
        """
        귀속말 처리
        
        Args:
            sender_socket: 메시지를 보낸 클라이언트 소켓
            sender_name (str): 메시지를 보낸 클라이언트 이름
            message (str): 귀속말 메시지
        """
        try:
            # 메시지 파싱: /st 대상자 메시지내용
            parts = message.split(' ', 2)
            if len(parts) < 3:
                error_msg = '귀속말 형식: /st 대상자 메시지'
                sender_socket.send(error_msg.encode('utf-8'))
                print(f'귓속말 형식 오류: {sender_name} - {message}')
                return
            
            target_name = parts[1]
            whisper_message = parts[2]
            
            print(f'귓속말 시도: {sender_name} -> {target_name}: {whisper_message}')
            
            # 대상자 찾기
            target_socket = None
            for socket_obj, name in self.client_names.items():
                if name == target_name:
                    target_socket = socket_obj
                    break
            
            if target_socket is None:
                error_msg = f'{target_name}님을 찾을 수 없습니다. 현재 접속자: {list(self.client_names.values())}'
                sender_socket.send(error_msg.encode('utf-8'))
                print(f'대상자 없음: {target_name}')
                return
            
            # 귀속말 전송
            whisper_to_target = f'[귓속말] {sender_name}: {whisper_message}'
            whisper_to_sender = f'[귓속말] {sender_name} -> {target_name}: {whisper_message}'
            
            target_socket.send(whisper_to_target.encode('utf-8'))
            sender_socket.send(whisper_to_sender.encode('utf-8'))
            
            print(f'귓속말 전송 완료: {sender_name} -> {target_name}')
            
        except Exception as e:
            print(f'귀속말 처리 중 오류: {e}')
            error_msg = '귓속말 전송 중 오류가 발생했습니다.'
            try:
                sender_socket.send(error_msg.encode('utf-8'))
            except:
                pass
    
    def broadcast_message(self, message, sender_socket=None):
        """
        모든 클라이언트에게 메시지 브로드캐스트
        
        Args:
            message (str): 브로드캐스트할 메시지
            sender_socket: 메시지를 보낸 클라이언트 소켓 (자기 자신 제외용)
        """
        with self.lock:
            disconnected_clients = []
            
            for client_socket in self.clients:
                try:
                    if client_socket != sender_socket:
                        client_socket.send(f'{message}'.encode('utf-8'))
                except ConnectionResetError:
                    disconnected_clients.append(client_socket)
                except Exception as e:
                    print(f'메시지 전송 중 오류: {e}')
                    disconnected_clients.append(client_socket)
            
            # 연결이 끊어진 클라이언트들 정리
            for client_socket in disconnected_clients:
                self.remove_client_cleanup(client_socket)
    
    def remove_client(self, client_socket, client_name):
        """
        클라이언트 제거 및 퇴장 메시지 브로드캐스트
        
        Args:
            client_socket: 제거할 클라이언트 소켓
            client_name (str): 제거할 클라이언트 이름
        """
        with self.lock:
            self.remove_client_cleanup(client_socket)
        
        # 퇴장 메시지 브로드캐스트
        self.broadcast_message(f'{client_name}님이 퇴장하셨습니다.')
        print(f'{client_name}님이 퇴장했습니다.')
        
        # 클라이언트 소켓 닫기
        try:
            client_socket.close()
        except:
            pass
    
    def remove_client_cleanup(self, client_socket):
        """
        클라이언트 정리 (락 내부에서 호출)
        
        Args:
            client_socket: 정리할 클라이언트 소켓
        """
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        if client_socket in self.client_names:
            del self.client_names[client_socket]
    
    def stop_server(self):
        """서버 종료"""
        if self.server_socket:
            self.server_socket.close()
        
        with self.lock:
            for client_socket in self.clients:
                try:
                    client_socket.close()
                except:
                    pass
        
        sys.exit(0)


def main():
    """메인 함수"""
    server = ChatServer()
    server.start_server()


if __name__ == '__main__':
    main()
