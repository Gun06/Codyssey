#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 이메일 전송 메인 프로그램
"""

from smtp_sender import HTMLEmailSender
from csv_handler import read_csv_recipients, create_sample_csv, validate_csv_format
from email_templates import get_default_html_template, create_sample_html_template


def get_user_input():
    """사용자로부터 이메일 설정 입력받기"""
    print('=== HTML 이메일 전송 프로그램 ===\n')
    
    sender_email = input('발신자 이메일 주소: ')
    sender_password = input('발신자 이메일 비밀번호: ')
    
    print('\nSMTP 서버를 선택하세요:')
    print('1. Gmail')
    print('2. 네이버')
    smtp_choice = input('선택 (1 또는 2): ')
    smtp_type = 'gmail' if smtp_choice == '1' else 'naver'
    
    return sender_email, sender_password, smtp_type


def select_send_method():
    """전송 방식 선택"""
    print('\n전송 방식을 선택하세요:')
    print('1. 일괄 전송 (모든 수신자가 서로의 이메일 주소를 볼 수 있음)')
    print('2. 개별 전송 (각자에게 개별적으로 전송)')
    send_choice = input('선택 (1 또는 2): ')
    return send_choice


def send_emails(sender_email, sender_password, smtp_type, send_method):
    """이메일 전송 실행"""
    try:
        # HTML 이메일 전송기 생성
        email_sender = HTMLEmailSender(sender_email, sender_password, smtp_type)
        
        # CSV 파일에서 수신자 목록 읽기
        recipients = read_csv_recipients('mail_target_list.csv')
        if not recipients:
            print('수신자 목록이 없습니다.')
            return False
        
        # HTML 이메일 본문
        html_body = get_default_html_template()
        subject = 'HTML 형식 이메일 테스트'
        
        print('\n' + '=' * 50)
        
        if send_method == '1':
            # 일괄 전송
            print('일괄 전송 모드로 전송합니다...')
            success = email_sender.send_html_email_batch(recipients, subject, html_body)
            if success:
                print(f'✓ {len(recipients)}명에게 이메일이 성공적으로 전송되었습니다.')
            else:
                print('✗ 이메일 전송에 실패했습니다.')
        else:
            # 개별 전송
            print('개별 전송 모드로 전송합니다...')
            success_count = email_sender.send_html_email_individual(recipients, subject, html_body)
            print(f'✓ {success_count}/{len(recipients)}명에게 이메일이 성공적으로 전송되었습니다.')
        
        print('=' * 50)
        return True
        
    except Exception as e:
        print(f'이메일 전송 중 오류 발생: {e}')
        return False


def main():
    """메인 함수"""
    try:
        # 샘플 파일 생성
        print('샘플 파일을 생성합니다...')
        create_sample_csv()
        create_sample_html_template()
        
        # CSV 파일 형식 검증
        if not validate_csv_format('mail_target_list.csv'):
            print('CSV 파일 형식에 문제가 있습니다.')
            return
        
        # 사용자 입력
        sender_email, sender_password, smtp_type = get_user_input()
        send_method = select_send_method()
        
        # 이메일 전송
        send_emails(sender_email, sender_password, smtp_type, send_method)
        
    except KeyboardInterrupt:
        print('\n\n사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'\n예상치 못한 오류 발생: {e}')


if __name__ == '__main__':
    main()
