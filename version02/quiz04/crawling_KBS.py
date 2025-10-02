#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 로그인 및 크롤링 스크립트
네이버 메일에서 받은 메일 제목들을 크롤링합니다.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class NaverCrawler:
    """네이버 크롤링을 위한 클래스"""
    
    def __init__(self):
        """크롤러 초기화"""
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Chrome WebDriver 설정"""
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # 헤드리스 모드 비활성화 (로그인 과정을 볼 수 있도록)
            # options.add_argument('--headless')
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            print('WebDriver 설정 완료')
            return True
        except Exception as e:
            print(f'WebDriver 설정 실패: {e}')
            return False
    
    def login_naver(self, user_id, password):
        """네이버 로그인"""
        try:
            # 네이버 메인 페이지 접속
            self.driver.get('https://www.naver.com')
            time.sleep(2)
            
            # 로그인 버튼 클릭
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'link_login'))
            )
            login_button.click()
            time.sleep(2)
            
            # 아이디 입력
            id_input = self.wait.until(
                EC.presence_of_element_located((By.ID, 'id'))
            )
            id_input.clear()
            id_input.send_keys(user_id)
            time.sleep(1)
            
            # 비밀번호 입력
            pw_input = self.driver.find_element(By.ID, 'pw')
            pw_input.clear()
            pw_input.send_keys(password)
            time.sleep(1)
            
            # 로그인 버튼 클릭
            login_submit = self.driver.find_element(By.ID, 'log.login')
            login_submit.click()
            time.sleep(3)
            
            # 로그인 성공 확인
            try:
                # 로그인 후 나타나는 요소 확인 (프로필 영역)
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'MyView-module__link_login___HpHMW'))
                )
                print('로그인 성공')
                return True
            except TimeoutException:
                print('로그인 실패 또는 추가 인증 필요')
                return False
                
        except Exception as e:
            print(f'로그인 과정에서 오류 발생: {e}')
            return False
    
    def get_login_only_content(self):
        """로그인 후에만 보이는 콘텐츠 수집"""
        login_content = []
        
        try:
            # 메인 페이지에서 로그인 후에만 보이는 요소들 수집
            self.driver.get('https://www.naver.com')
            time.sleep(2)
            
            # 1. 내 정보 영역
            try:
                profile_area = self.driver.find_element(By.CLASS_NAME, 'MyView-module__my_area___Lg4U4')
                if profile_area:
                    login_content.append('내 정보 영역 표시됨')
            except NoSuchElementException:
                pass
            
            # 2. 최근 검색어
            try:
                recent_searches = self.driver.find_elements(By.CLASS_NAME, 'ah_item')
                if recent_searches:
                    search_texts = [elem.text for elem in recent_searches[:5]]
                    login_content.extend([f'최근 검색어: {search}' for search in search_texts])
            except NoSuchElementException:
                pass
            
            # 3. 맞춤 뉴스 영역
            try:
                custom_news = self.driver.find_elements(By.CLASS_NAME, 'news_tit')
                if custom_news:
                    news_titles = [elem.text for elem in custom_news[:3]]
                    login_content.extend([f'맞춤 뉴스: {title}' for title in news_titles])
            except NoSuchElementException:
                pass
            
            print(f'로그인 전용 콘텐츠 {len(login_content)}개 수집 완료')
            return login_content
            
        except Exception as e:
            print(f'로그인 전용 콘텐츠 수집 중 오류: {e}')
            return login_content
    
    def crawl_naver_mail(self):
        """네이버 메일에서 받은 메일 제목 크롤링"""
        mail_titles = []
        
        try:
            # 네이버 메일 페이지로 이동
            self.driver.get('https://mail.naver.com')
            time.sleep(3)
            
            # 메일 리스트가 로드될 때까지 대기
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mail_list_item'))
                )
            except TimeoutException:
                print('메일 리스트 로드 시간 초과')
                return mail_titles
            
            # 메일 제목 수집
            mail_items = self.driver.find_elements(By.CLASS_NAME, 'mail_list_item')
            
            for item in mail_items[:10]:  # 최근 10개 메일만 수집
                try:
                    # 메일 제목 찾기
                    title_element = item.find_element(By.CLASS_NAME, 'subject')
                    title = title_element.text.strip()
                    if title:
                        mail_titles.append(title)
                except NoSuchElementException:
                    continue
            
            print(f'메일 제목 {len(mail_titles)}개 수집 완료')
            return mail_titles
            
        except Exception as e:
            print(f'메일 크롤링 중 오류 발생: {e}')
            return mail_titles
    
    def display_results(self, login_content, mail_titles):
        """수집된 결과를 화면에 출력"""
        print('\n=== 수집된 데이터 ===')
        
        print('\n1. 로그인 후에만 보이는 콘텐츠:')
        if login_content:
            for i, content in enumerate(login_content, 1):
                print(f'   {i}. {content}')
        else:
            print('   수집된 로그인 전용 콘텐츠가 없습니다.')
        
        print('\n2. 네이버 메일 제목:')
        if mail_titles:
            for i, title in enumerate(mail_titles, 1):
                print(f'   {i}. {title}')
        else:
            print('   수집된 메일 제목이 없습니다.')
    
    def close_driver(self):
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()
            print('WebDriver 종료')


def main():
    """메인 함수"""
    crawler = NaverCrawler()
    
    try:
        # WebDriver 설정
        if not crawler.setup_driver():
            return
        
        # 네이버 로그인 정보 입력 (실제 사용 시에는 안전한 방법으로 입력받아야 함)
        user_id = input('네이버 아이디를 입력하세요: ')
        password = input('네이버 비밀번호를 입력하세요: ')
        
        # 로그인 시도
        if not crawler.login_naver(user_id, password):
            print('로그인에 실패했습니다. 프로그램을 종료합니다.')
            return
        
        # 로그인 후에만 보이는 콘텐츠 수집
        login_content = crawler.get_login_only_content()
        
        # 네이버 메일 제목 크롤링
        mail_titles = crawler.crawl_naver_mail()
        
        # 결과 출력
        crawler.display_results(login_content, mail_titles)
        
    except KeyboardInterrupt:
        print('\n사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'예상치 못한 오류 발생: {e}')
    finally:
        crawler.close_driver()


if __name__ == '__main__':
    main()
