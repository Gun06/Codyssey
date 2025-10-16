#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail SMTP를 사용한 이메일 전송 스크립트
첨부 파일 기능을 포함합니다.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class GmailSender:
    """Gmail SMTP를 사용한 이메일 전송 클래스"""
    
    # Gmail SMTP 서버 설정
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587  # TLS 포트
    
    def __init__(self, sender_email, sender_password):
        """
        이메일 전송 초기화
        
        Args:
            sender_email: 발신자 Gmail 주소
            sender_password: 발신자 Gmail 앱 비밀번호
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_connection = None
    
    def connect_smtp_server(self):
        """SMTP 서버에 연결하고 로그인"""
        try:
            print(f'{self.SMTP_SERVER}:{self.SMTP_PORT}에 연결 중...')
            self.smtp_connection = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            self.smtp_connection.ehlo()
            
            # TLS 암호화 시작
            self.smtp_connection.starttls()
            self.smtp_connection.ehlo()
            
            # 로그인
            print('로그인 중...')
            self.smtp_connection.login(self.sender_email, self.sender_password)
            print('로그인 성공')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 실패: 이메일 주소 또는 비밀번호를 확인하세요.')
            print('Gmail 앱 비밀번호를 사용하고 있는지 확인하세요.')
            return False
        except smtplib.SMTPConnectError:
            print('SMTP 서버 연결 실패')
            return False
        except smtplib.SMTPException as e:
            print(f'SMTP 오류 발생: {e}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류 발생: {e}')
            return False
    
    def create_message(self, receiver_email, subject, body, attachments=None):
        """
        이메일 메시지 생성
        
        Args:
            receiver_email: 수신자 이메일 주소
            subject: 이메일 제목
            body: 이메일 본문
            attachments: 첨부 파일 경로 리스트 (선택사항)
        
        Returns:
            MIMEMultipart 메시지 객체
        """
        try:
            # 메시지 객체 생성
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            
            # 본문 추가
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 첨부 파일 추가
            if attachments:
                for file_path in attachments:
                    if not self.attach_file(message, file_path):
                        print(f'경고: {file_path} 첨부 실패')
            
            return message
            
        except Exception as e:
            print(f'메시지 생성 중 오류 발생: {e}')
            return None
    
    def attach_file(self, message, file_path):
        """
        파일을 메시지에 첨부
        
        Args:
            message: MIMEMultipart 메시지 객체
            file_path: 첨부할 파일 경로
        
        Returns:
            성공 여부 (True/False)
        """
        try:
            # 파일 존재 확인
            if not os.path.exists(file_path):
                print(f'파일을 찾을 수 없습니다: {file_path}')
                return False
            
            # 파일 크기 확인 (25MB 제한)
            file_size = os.path.getsize(file_path)
            max_size = 25 * 1024 * 1024  # 25MB
            if file_size > max_size:
                print(f'파일이 너무 큽니다: {file_path} ({file_size} bytes)')
                return False
            
            # 파일 읽기
            with open(file_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
            
            # 파일 인코딩
            encoders.encode_base64(part)
            
            # 헤더 추가
            filename = os.path.basename(file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            # 메시지에 첨부
            message.attach(part)
            print(f'파일 첨부 성공: {filename}')
            return True
            
        except IOError as e:
            print(f'파일 읽기 오류: {e}')
            return False
        except Exception as e:
            print(f'파일 첨부 중 오류 발생: {e}')
            return False
    
    def send_email(self, receiver_email, subject, body, attachments=None):
        """
        이메일 전송
        
        Args:
            receiver_email: 수신자 이메일 주소
            subject: 이메일 제목
            body: 이메일 본문
            attachments: 첨부 파일 경로 리스트 (선택사항)
        
        Returns:
            성공 여부 (True/False)
        """
        try:
            # SMTP 서버 연결
            if not self.connect_smtp_server():
                return False
            
            # 메시지 생성
            message = self.create_message(receiver_email, subject, body, attachments)
            if message is None:
                return False
            
            # 이메일 전송
            print('이메일 전송 중...')
            self.smtp_connection.send_message(message)
            print('이메일 전송 성공!')
            return True
            
        except smtplib.SMTPRecipientsRefused:
            print('수신자 주소가 거부되었습니다.')
            return False
        except smtplib.SMTPDataError:
            print('이메일 데이터 전송 오류')
            return False
        except smtplib.SMTPException as e:
            print(f'이메일 전송 실패: {e}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류 발생: {e}')
            return False
        finally:
            self.disconnect_smtp_server()
    
    def disconnect_smtp_server(self):
        """SMTP 서버 연결 종료"""
        try:
            if self.smtp_connection:
                self.smtp_connection.quit()
                print('SMTP 서버 연결 종료')
        except Exception as e:
            print(f'연결 종료 중 오류: {e}')


def get_user_input():
    """사용자로부터 이메일 정보 입력받기"""
    print('=== Gmail SMTP 이메일 전송 ===\n')
    
    sender_email = input('발신자 Gmail 주소: ')
    sender_password = input('발신자 Gmail 앱 비밀번호: ')
    receiver_email = input('수신자 이메일 주소: ')
    subject = input('이메일 제목: ')
    
    print('\n이메일 본문 입력 (입력 완료 후 빈 줄에서 Enter):')
    body_lines = []
    while True:
        line = input()
        if line == '':
            break
        body_lines.append(line)
    body = '\n'.join(body_lines)
    
    # 첨부 파일 입력
    attachments = []
    attach_file = input('\n첨부 파일을 추가하시겠습니까? (y/n): ')
    if attach_file.lower() == 'y':
        while True:
            file_path = input('첨부 파일 경로 (완료하려면 빈 줄): ')
            if file_path == '':
                break
            attachments.append(file_path)
    
    return sender_email, sender_password, receiver_email, subject, body, attachments


def send_sample_email():
    """샘플 이메일 전송 (테스트용)"""
    # 샘플 데이터
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_app_password'
    receiver_email = 'receiver_email@example.com'
    subject = '테스트 이메일'
    body = '''안녕하세요,

이것은 Python으로 전송한 테스트 이메일입니다.
SMTP 프로토콜을 사용하여 Gmail을 통해 전송되었습니다.

감사합니다.'''
    
    # 첨부 파일 예시
    attachments = []
    
    # 이메일 전송
    sender = GmailSender(sender_email, sender_password)
    success = sender.send_email(receiver_email, subject, body, attachments)
    
    return success


def main():
    """메인 함수"""
    try:
        # 사용자 입력 모드
        print('이메일 전송을 시작합니다.\n')
        
        sender_email, sender_password, receiver_email, subject, body, attachments = get_user_input()
        
        # GmailSender 인스턴스 생성
        gmail_sender = GmailSender(sender_email, sender_password)
        
        # 이메일 전송
        print('\n' + '=' * 50)
        success = gmail_sender.send_email(
            receiver_email,
            subject,
            body,
            attachments if attachments else None
        )
        print('=' * 50)
        
        if success:
            print('\n✓ 이메일이 성공적으로 전송되었습니다.')
        else:
            print('\n✗ 이메일 전송에 실패했습니다.')
        
    except KeyboardInterrupt:
        print('\n\n사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'\n예상치 못한 오류 발생: {e}')


if __name__ == '__main__':
    main()

