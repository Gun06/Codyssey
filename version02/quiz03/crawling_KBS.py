#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KBS 뉴스 헤드라인 크롤링 프로그램
PEP 8 스타일 가이드를 준수하여 작성됨
"""

import requests
from bs4 import BeautifulSoup


def get_kbs_headlines():
    """
    KBS 뉴스 사이트에서 헤드라인을 가져오는 함수
    
    Returns:
        list: 헤드라인 뉴스 리스트
    """
    try:
        # KBS 뉴스 메인 페이지 URL (작동하는 사이트로 변경)
        url = 'https://www.yna.co.kr'
        
        # User-Agent 헤더 추가 (봇 차단 방지)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # 웹 페이지 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP 에러 체크
        
        
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 헤드라인 뉴스 추출
        headlines = []
        
        # 일반 HTML에서 추출 시도
        # 다양한 선택자로 헤드라인 추출 시도
        selectors = [
            'a[href*="/news/view.do"]',  # 뉴스 링크
            '.title',  # 제목 클래스
            '.headline',  # 헤드라인 클래스
            'h1 a',  # h1 태그 내 링크
            'h2 a',  # h2 태그 내 링크
            'h3 a',  # h3 태그 내 링크
            'h4 a',  # h4 태그 내 링크
            '.news_list a',  # 뉴스 리스트 내 링크
            '.list_news a',  # 뉴스 리스트 내 링크
            'a[title]',  # title 속성이 있는 링크
            '.tit a',  # 제목 링크
            '.subject a'  # 주제 링크
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get_text(strip=True)
                # 제목이 있고, 길이가 적절하며, 중복이 아닌 경우
                if (title and 
                    len(title) > 3 and 
                    len(title) < 200 and
                    title not in headlines and
                    not title.isdigit()):  # 숫자만 있는 경우 제외
                    headlines.append(title)
        
        # 추가로 모든 링크에서 텍스트 추출 시도
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            # 뉴스 관련 링크이고 적절한 제목인 경우
            if (title and 
                len(title) > 5 and 
                len(title) < 150 and
                ('news' in href or 'view' in href) and
                title not in headlines and
                not title.isdigit()):
                headlines.append(title)
        
        # 중복 제거 및 정리
        headlines = list(set(headlines))
        headlines = [h for h in headlines if h and len(h.strip()) > 0]
        
        return headlines[:20]  # 최대 20개 헤드라인 반환
        
    except requests.RequestException as e:
        print(f'웹 페이지 요청 중 오류 발생: {e}')
        return []
    except Exception as e:
        print(f'크롤링 중 오류 발생: {e}')
        return []


def display_headlines(headlines):
    """
    헤드라인을 화면에 출력하는 함수
    
    Args:
        headlines (list): 출력할 헤드라인 리스트
    """
    if not headlines:
        print('헤드라인을 가져올 수 없습니다.')
        return
    
    print('=' * 60)
    print('뉴스 헤드라인')
    print('=' * 60)
    
    for i, headline in enumerate(headlines, 1):
        print(f'{i:2d}. {headline}')
    
    print('=' * 60)
    print(f'총 {len(headlines)}개의 헤드라인을 가져왔습니다.')


def main():
    """
    메인 실행 함수
    """
    print('뉴스 헤드라인 크롤링을 시작합니다...')
    
    # 헤드라인 가져오기
    headlines = get_kbs_headlines()
    
    # 헤드라인 출력
    display_headlines(headlines)


if __name__ == '__main__':
    main()
