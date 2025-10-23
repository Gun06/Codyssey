# Quiz 06: HTML 이메일 전송 프로그램

## 개요

HTML 형식의 이메일을 CSV 파일의 수신자 목록을 통해 전송하는 프로그램입니다.

## 주요 기능

- HTML 형식 이메일 전송
- CSV 파일에서 수신자 목록 읽기
- 두 가지 전송 방식 지원:
  - 일괄 전송 (모든 수신자가 서로의 이메일 주소를 볼 수 있음)
  - 개별 전송 (각자에게 개별적으로 전송)
- Gmail 및 네이버 SMTP 지원
- 첨부 파일 지원

## 파일 구조

```
quiz06/
├── main.py                 # 메인 실행 프로그램
├── smtp_sender.py          # SMTP 이메일 전송 모듈
├── csv_handler.py          # CSV 파일 처리 모듈
├── email_templates.py      # HTML 이메일 템플릿 모듈
├── mail_target_list.csv    # 수신자 목록 CSV 파일 (자동 생성)
├── email_template.html     # HTML 이메일 템플릿 (자동 생성)
└── README.md              # 이 파일
```

## CSV 파일 형식

`mail_target_list.csv` 파일은 다음과 같은 형식이어야 합니다:

```csv
이름,이메일
김철수,kimcs@example.com
이영희,leeyh@example.com
박민수,parkms@example.com
```

## 사용법

### 1. 프로그램 실행

```bash
python main.py
```

### 2. 설정 입력

- 발신자 이메일 주소 입력
- 발신자 이메일 비밀번호 입력
- SMTP 서버 선택 (Gmail 또는 네이버)
- 전송 방식 선택 (일괄 전송 또는 개별 전송)

### 3. 전송 방식 비교

#### 일괄 전송 (CC 방식)

- **장점**: 한 번의 SMTP 연결로 모든 수신자에게 전송
- **단점**: 모든 수신자가 서로의 이메일 주소를 볼 수 있음
- **적합한 경우**: 공개적인 공지사항이나 팀 내부 소통

#### 개별 전송

- **장점**: 각 수신자의 개인정보 보호, 개인화된 메시지 가능
- **단점**: 각 수신자마다 별도의 SMTP 연결 필요
- **적합한 경우**: 개인적인 메시지나 개인정보가 중요한 경우

## SMTP 서버 설정

### Gmail

- SMTP 서버: smtp.gmail.com
- 포트: 587
- 보안: TLS
- **주의**: Gmail 앱 비밀번호를 사용해야 합니다.

### 네이버

- SMTP 서버: smtp.naver.com
- 포트: 587 (TLS) 또는 465 (SSL)
- 보안: TLS/SSL
- **주의**:
  - 네이버 메일 계정의 비밀번호를 사용합니다.
  - 네이버 메일 환경설정에서 POP3/IMAP 설정을 활성화해야 합니다.
  - 프로그램이 자동으로 TLS(587)와 SSL(465) 포트를 모두 시도합니다.

## HTML 이메일 템플릿

프로그램은 자동으로 `email_template.html` 파일을 생성합니다. 이 파일을 수정하여 원하는 HTML 이메일 디자인을 만들 수 있습니다.

### 개인화 변수

- `{이름}`: 수신자의 이름으로 자동 치환됩니다.

## 예제 HTML 이메일

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>HTML 이메일</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
      }
      .header {
        background-color: #4caf50;
        color: white;
        padding: 20px;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>안녕하세요, {이름}님!</h1>
    </div>
    <div class="content">
      <p>HTML 형식의 이메일입니다.</p>
    </div>
  </body>
</html>
```

## 요구사항

- Python 3.6 이상
- 인터넷 연결
- Gmail 또는 네이버 메일 계정

## 제약사항

- Python 기본 라이브러리만 사용 (smtplib, csv, email, os)
- PEP 8 스타일 가이드 준수
- 경고 메시지 없이 실행되어야 함

## 문제 해결

### Gmail 인증 오류

1. Gmail 2단계 인증이 활성화되어 있는지 확인
2. 앱 비밀번호를 생성하여 사용
3. "보안 수준이 낮은 앱의 액세스" 설정 확인

### 네이버 인증 오류

1. 네이버 메일 계정의 비밀번호가 정확한지 확인
2. 네이버 메일 설정에서 SMTP 사용이 허용되어 있는지 확인

### CSV 파일 오류

1. 파일이 UTF-8 인코딩으로 저장되어 있는지 확인
2. CSV 형식이 정확한지 확인 (이름,이메일)
3. 파일 경로가 올바른지 확인

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
