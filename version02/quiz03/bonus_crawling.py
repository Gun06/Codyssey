#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보너스 과제: 날씨 및 주식 정보 크롤링 프로그램
PEP 8 스타일 가이드를 준수하여 작성됨
"""

import requests
from bs4 import BeautifulSoup


def get_weather_info(city='서울'):
    """
    날씨 정보를 가져오는 함수 (간단한 예제)
    
    Args:
        city (str): 도시명 (기본값: 서울)
    
    Returns:
        dict: 날씨 정보 딕셔너리
    """
    try:
        # 간단한 날씨 정보 (실제로는 API를 사용해야 함)
        weather_data = {
            '서울': {
                'temperature': '15°C',
                'status': '맑음',
                'humidity': '65%',
                'wind': '서풍 2m/s'
            },
            '부산': {
                'temperature': '18°C',
                'status': '구름많음',
                'humidity': '70%',
                'wind': '남동풍 3m/s'
            },
            '대구': {
                'temperature': '17°C',
                'status': '맑음',
                'humidity': '60%',
                'wind': '북서풍 1m/s'
            }
        }
        
        return weather_data.get(city, {
            'temperature': '정보 없음',
            'status': '정보 없음',
            'humidity': '정보 없음',
            'wind': '정보 없음'
        })
        
    except Exception as e:
        print(f'날씨 정보 가져오기 중 오류 발생: {e}')
        return {}


def get_stock_info(stock_code='005930'):  # 삼성전자 기본값
    """
    주식 정보를 가져오는 함수
    
    Args:
        stock_code (str): 주식 코드 (기본값: 005930 - 삼성전자)
    
    Returns:
        dict: 주식 정보 딕셔너리
    """
    try:
        # 네이버 주식 검색 URL
        url = f'https://finance.naver.com/item/main.naver?code={stock_code}'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        stock_info = {}
        
        # 주식명
        name_element = soup.find('h2', class_='wrap_company')
        if name_element:
            stock_info['name'] = name_element.get_text(strip=True)
        
        # 현재가
        price_element = soup.find('p', class_='no_today')
        if price_element:
            stock_info['current_price'] = price_element.get_text(strip=True)
        
        # 전일 대비
        change_element = soup.find('p', class_='no_exday')
        if change_element:
            stock_info['change'] = change_element.get_text(strip=True)
        
        # 거래량
        volume_element = soup.find('span', class_='blind')
        if volume_element:
            stock_info['volume'] = volume_element.get_text(strip=True)
        
        return stock_info
        
    except Exception as e:
        print(f'주식 정보 가져오기 중 오류 발생: {e}')
        return {}


def display_weather_info(weather_info, city):
    """
    날씨 정보를 화면에 출력하는 함수
    
    Args:
        weather_info (dict): 날씨 정보 딕셔너리
        city (str): 도시명
    """
    print('=' * 50)
    print(f'{city} 날씨 정보')
    print('=' * 50)
    
    if not weather_info:
        print('날씨 정보를 가져올 수 없습니다.')
        return
    
    for key, value in weather_info.items():
        print(f'{key}: {value}')
    
    print('=' * 50)


def display_stock_info(stock_info, stock_code):
    """
    주식 정보를 화면에 출력하는 함수
    
    Args:
        stock_info (dict): 주식 정보 딕셔너리
        stock_code (str): 주식 코드
    """
    print('=' * 50)
    print(f'주식 정보 (코드: {stock_code})')
    print('=' * 50)
    
    if not stock_info:
        print('주식 정보를 가져올 수 없습니다.')
        return
    
    for key, value in stock_info.items():
        print(f'{key}: {value}')
    
    print('=' * 50)


def main():
    """
    메인 실행 함수
    """
    print('보너스 과제: 날씨 및 주식 정보 크롤링을 시작합니다...')
    print()
    
    # 날씨 정보 가져오기
    print('1. 날씨 정보 크롤링')
    weather_info = get_weather_info('서울')
    display_weather_info(weather_info, '서울')
    print()
    
    # 주식 정보 가져오기
    print('2. 주식 정보 크롤링')
    stock_info = get_stock_info('005930')  # 삼성전자
    display_stock_info(stock_info, '005930')
    print()
    
    # 다른 도시 날씨 정보
    print('3. 다른 도시 날씨 정보')
    weather_info_busan = get_weather_info('부산')
    display_weather_info(weather_info_busan, '부산')
    print()
    
    # 다른 주식 정보
    print('4. 다른 주식 정보')
    stock_info_sk = get_stock_info('000660')  # SK하이닉스
    display_stock_info(stock_info_sk, '000660')


if __name__ == '__main__':
    main()
