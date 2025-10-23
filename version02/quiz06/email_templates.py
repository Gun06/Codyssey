#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 이메일 템플릿 관리 모듈
"""


def get_default_html_template():
    """기본 HTML 이메일 템플릿 반환"""
    return '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML 이메일</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }
        .content {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 0 0 5px 5px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 10px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>안녕하세요, {이름}님!</h1>
    </div>
    <div class="content">
        <p>HTML 형식의 이메일을 성공적으로 전송했습니다.</p>
        
        <div class="highlight">
            <strong>이메일 전송 기능:</strong>
            <ul>
                <li>HTML 형식 지원</li>
                <li>CSV 파일에서 수신자 목록 읽기</li>
                <li>개별 전송 및 일괄 전송 지원</li>
                <li>Gmail 및 네이버 SMTP 지원</li>
            </ul>
        </div>
        
        <p>이 이메일은 Python의 smtplib를 사용하여 전송되었습니다.</p>
        
        <p>감사합니다!</p>
    </div>
    <div class="footer">
        <p>이 이메일은 자동으로 생성되었습니다.</p>
    </div>
</body>
</html>'''


def create_sample_html_template():
    """샘플 HTML 이메일 템플릿 파일 생성"""
    html_template = get_default_html_template()
    
    with open('email_template.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print('샘플 HTML 템플릿이 생성되었습니다: email_template.html')


def personalize_html(html_template, name):
    """
    HTML 템플릿에 개인화 정보 적용
    
    Args:
        html_template: HTML 템플릿 문자열
        name: 수신자 이름
    
    Returns:
        개인화된 HTML 문자열
    """
    return html_template.replace('{이름}', name)
