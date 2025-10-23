#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMTP 이메일 전송 모듈
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class HTMLEmailSender:
    """HTML 형식 이메일 전송 클래스"""
    
    # Gmail SMTP 서버 설정
    GMAIL_SMTP_SERVER = 'smtp.gmail.com'
    GMAIL_SMTP_PORT = 587
    
    # 네이버 SMTP 서버 설정
    NAVER_SMTP_SERVER = 'smtp.naver.com'
    NAVER_SMTP_PORT = 587  # TLS 포트
    NAVER_SMTP_SSL_PORT = 465  # SSL 포트
    
    def __init__(self, sender_email, sender_password, smtp_type='gmail'):
        """
        이메일 전송 초기화
        
        Args:
            sender_email: 발신자 이메일 주소
            sender_password: 발신자 이메일 비밀번호
            smtp_type: SMTP 서버 타입 ('gmail' 또는 'naver')
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_type = smtp_type.lower()
        self.smtp_connection = None
        
        # SMTP 서버 설정
        if self.smtp_type == 'gmail':
            self.smtp_server = self.GMAIL_SMTP_SERVER
            self.smtp_port = self.GMAIL_SMTP_PORT
        elif self.smtp_type == 'naver':
            self.smtp_server = self.NAVER_SMTP_SERVER
            self.smtp_port = self.NAVER_SMTP_PORT
        else:
            raise ValueError('지원하지 않는 SMTP 타입입니다. gmail 또는 naver를 사용하세요.')
    
    def connect_smtp_server(self):
        """SMTP 서버에 연결하고 로그인"""
        try:
            print(f'{self.smtp_server}:{self.smtp_port}에 연결 중...')
            
            # 네이버의 경우 SSL 포트도 시도
            if self.smtp_type == 'naver':
                try:
                    # 먼저 TLS 포트(587)로 시도
                    self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    self.smtp_connection.ehlo()
                    self.smtp_connection.starttls()
                    self.smtp_connection.ehlo()
                except:
                    # TLS 실패 시 SSL 포트(465)로 시도
                    print('TLS 연결 실패, SSL 포트로 재시도 중...')
                    self.smtp_connection = smtplib.SMTP_SSL(self.smtp_server, self.NAVER_SMTP_SSL_PORT)
                    self.smtp_connection.ehlo()
            else:
                # Gmail은 TLS만 사용
                self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
                self.smtp_connection.ehlo()
                self.smtp_connection.starttls()
                self.smtp_connection.ehlo()
            
            # 로그인
            print('로그인 중...')
            self.smtp_connection.login(self.sender_email, self.sender_password)
            print('로그인 성공')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 실패: 이메일 주소 또는 비밀번호를 확인하세요.')
            if self.smtp_type == 'gmail':
                print('Gmail 앱 비밀번호를 사용하고 있는지 확인하세요.')
            elif self.smtp_type == 'naver':
                print('네이버 메일 환경설정에서 POP3/IMAP 설정을 활성화했는지 확인하세요.')
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
    
    def create_html_message(self, receiver_emails, subject, html_body, attachments=None):
        """
        HTML 이메일 메시지 생성
        
        Args:
            receiver_emails: 수신자 이메일 주소 리스트 또는 단일 이메일
            subject: 이메일 제목
            html_body: HTML 형식 이메일 본문
            attachments: 첨부 파일 경로 리스트 (선택사항)
        
        Returns:
            MIMEMultipart 메시지 객체
        """
        try:
            # 메시지 객체 생성
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['Subject'] = subject
            
            # 수신자 설정
            if isinstance(receiver_emails, list):
                message['To'] = ', '.join(receiver_emails)
            else:
                message['To'] = receiver_emails
            
            # HTML 본문 추가
            html_part = MIMEText(html_body, 'html', 'utf-8')
            message.attach(html_part)
            
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
    
    def send_html_email_batch(self, recipients, subject, html_body, attachments=None):
        """
        여러 수신자에게 한 번에 HTML 이메일 전송 (CC 방식)
        
        Args:
            recipients: 수신자 정보 리스트 [(이름, 이메일), ...]
            subject: 이메일 제목
            html_body: HTML 형식 이메일 본문
            attachments: 첨부 파일 경로 리스트 (선택사항)
        
        Returns:
            성공 여부 (True/False)
        """
        try:
            # SMTP 서버 연결
            if not self.connect_smtp_server():
                return False
            
            # 수신자 이메일 주소 추출
            receiver_emails = [email for _, email in recipients]
            
            # 메시지 생성
            message = self.create_html_message(receiver_emails, subject, html_body, attachments)
            if message is None:
                return False
            
            # 이메일 전송
            print(f'{len(recipients)}명에게 이메일 전송 중...')
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
    
    def send_html_email_individual(self, recipients, subject, html_body, attachments=None):
        """
        여러 수신자에게 개별적으로 HTML 이메일 전송
        
        Args:
            recipients: 수신자 정보 리스트 [(이름, 이메일), ...]
            subject: 이메일 제목
            html_body: HTML 형식 이메일 본문
            attachments: 첨부 파일 경로 리스트 (선택사항)
        
        Returns:
            성공한 전송 수
        """
        success_count = 0
        
        for name, email in recipients:
            try:
                # SMTP 서버 연결
                if not self.connect_smtp_server():
                    print(f'{name}({email})에게 전송 실패: SMTP 연결 실패')
                    continue
                
                # 개인화된 HTML 본문 생성
                personalized_html = html_body.replace('{이름}', name)
                
                # 메시지 생성
                message = self.create_html_message(email, subject, personalized_html, attachments)
                if message is None:
                    print(f'{name}({email})에게 전송 실패: 메시지 생성 실패')
                    continue
                
                # 이메일 전송
                print(f'{name}({email})에게 이메일 전송 중...')
                self.smtp_connection.send_message(message)
                print(f'{name}({email})에게 전송 성공!')
                success_count += 1
                
            except smtplib.SMTPRecipientsRefused:
                print(f'{name}({email})에게 전송 실패: 수신자 주소 거부')
            except smtplib.SMTPDataError:
                print(f'{name}({email})에게 전송 실패: 데이터 전송 오류')
            except smtplib.SMTPException as e:
                print(f'{name}({email})에게 전송 실패: {e}')
            except Exception as e:
                print(f'{name}({email})에게 전송 실패: 예상치 못한 오류 - {e}')
            finally:
                self.disconnect_smtp_server()
        
        return success_count
    
    def disconnect_smtp_server(self):
        """SMTP 서버 연결 종료"""
        try:
            if self.smtp_connection:
                self.smtp_connection.quit()
                print('SMTP 서버 연결 종료')
        except Exception as e:
            print(f'연결 종료 중 오류: {e}')
