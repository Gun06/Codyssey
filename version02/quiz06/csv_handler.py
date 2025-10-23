#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV 파일 처리 모듈
"""

import csv


def read_csv_recipients(csv_file_path):
    """
    CSV 파일에서 수신자 목록 읽기
    
    Args:
        csv_file_path: CSV 파일 경로
    
    Returns:
        수신자 정보 리스트 [(이름, 이메일), ...]
    """
    recipients = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get('이름', '').strip()
                email = row.get('이메일', '').strip()
                if name and email:
                    recipients.append((name, email))
                else:
                    print(f'경고: 잘못된 데이터 행 무시됨: {row}')
        
        print(f'CSV에서 {len(recipients)}명의 수신자를 읽었습니다.')
        return recipients
        
    except FileNotFoundError:
        print(f'CSV 파일을 찾을 수 없습니다: {csv_file_path}')
        return []
    except Exception as e:
        print(f'CSV 파일 읽기 오류: {e}')
        return []


def create_sample_csv():
    """샘플 CSV 파일 생성"""
    csv_content = '''이름,이메일
김철수,kimcs@example.com
이영희,leeyh@example.com
박민수,parkms@example.com
정수진,jeongsj@example.com
최지영,choijy@example.com'''
    
    with open('mail_target_list.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    print('샘플 CSV 파일이 생성되었습니다: mail_target_list.csv')


def validate_csv_format(csv_file_path):
    """
    CSV 파일 형식 검증
    
    Args:
        csv_file_path: CSV 파일 경로
    
    Returns:
        유효성 여부 (True/False)
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # 필수 컬럼 확인
            if '이름' not in reader.fieldnames or '이메일' not in reader.fieldnames:
                print('CSV 파일에 필수 컬럼(이름, 이메일)이 없습니다.')
                return False
            
            # 데이터 행 확인
            row_count = 0
            for row in reader:
                row_count += 1
                name = row.get('이름', '').strip()
                email = row.get('이메일', '').strip()
                if not name or not email:
                    print(f'경고: {row_count}번째 행에 빈 데이터가 있습니다.')
            
            if row_count == 0:
                print('CSV 파일에 데이터가 없습니다.')
                return False
            
            print(f'CSV 파일 형식이 유효합니다. ({row_count}개 행)')
            return True
            
    except Exception as e:
        print(f'CSV 파일 검증 오류: {e}')
        return False
