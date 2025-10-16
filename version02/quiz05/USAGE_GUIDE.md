# sendmail.py 사용 가이드

## 빠른 시작

### 1단계: Gmail 앱 비밀번호 생성

1. https://myaccount.google.com/ 접속
2. 왼쪽 메뉴에서 "보안" 클릭
3. "Google에 로그인" 섹션으로 스크롤
4. "2단계 인증" 활성화 (아직 안 되어 있다면)
5. "앱 비밀번호" 클릭
6. 앱 선택: "메일", 기기 선택: "기타(맞춤 이름)"
7. 이름 입력: "Python SMTP"
8. "생성" 클릭
9. 16자리 비밀번호를 복사 (예: abcd efgh ijkl mnop)

### 2단계: 프로그램 실행

```bash
cd /Users/kogun/Desktop/Codyssey/version02/quiz05
python3 sendmail.py
```

### 3단계: 정보 입력

프로그램이 다음 정보를 요청합니다:

```
=== Gmail SMTP 이메일 전송 ===

발신자 Gmail 주소: your_email@gmail.com
발신자 Gmail 앱 비밀번호: abcdefghijklmnop
수신자 이메일 주소: receiver@example.com
이메일 제목: 안녕하세요

이메일 본문 입력 (입력 완료 후 빈 줄에서 Enter):
안녕하세요,
테스트 메일입니다.
잘 받아보세요!
[빈 줄에서 Enter]

첨부 파일을 추가하시겠습니까? (y/n): y
첨부 파일 경로 (완료하려면 빈 줄): sample_attachment.txt
첨부 파일 경로 (완료하려면 빈 줄): [Enter]
```

## 실행 예제

### 예제 1: 기본 텍스트 메일

```
발신자 Gmail 주소: myemail@gmail.com
발신자 Gmail 앱 비밀번호: ****************
수신자 이메일 주소: friend@example.com
이메일 제목: Python으로 보내는 첫 메일

이메일 본문 입력:
안녕하세요,
Python으로 메일을 보내는 테스트입니다.

첨부 파일을 추가하시겠습니까? (y/n): n
```

### 예제 2: 첨부 파일이 있는 메일

```
발신자 Gmail 주소: myemail@gmail.com
발신자 Gmail 앱 비밀번호: ****************
수신자 이메일 주소: friend@example.com
이메일 제목: 문서 전달드립니다

이메일 본문 입력:
안녕하세요,
요청하신 문서를 첨부파일로 보내드립니다.

첨부 파일을 추가하시겠습니까? (y/n): y
첨부 파일 경로: /Users/kogun/Desktop/report.pdf
첨부 파일 경로: /Users/kogun/Desktop/data.xlsx
첨부 파일 경로: [Enter]
```

## 코드에서 직접 사용하기

### 방법 1: 간단한 메일 전송

```python
from sendmail import GmailSender

# 발신자 정보
sender = GmailSender('myemail@gmail.com', 'my_app_password')

# 메일 전송
success = sender.send_email(
    receiver_email='friend@example.com',
    subject='Hello!',
    body='안녕하세요, 테스트 메일입니다.'
)

if success:
    print('메일 전송 완료!')
```

### 방법 2: 첨부 파일이 있는 메일

```python
from sendmail import GmailSender

sender = GmailSender('myemail@gmail.com', 'my_app_password')

attachments = [
    'document.pdf',
    'image.png',
    'data.csv'
]

success = sender.send_email(
    receiver_email='friend@example.com',
    subject='문서 전달',
    body='첨부 파일을 확인해주세요.',
    attachments=attachments
)
```

### 방법 3: 여러 사람에게 전송

```python
from sendmail import GmailSender

sender = GmailSender('myemail@gmail.com', 'my_app_password')

recipients = [
    'person1@example.com',
    'person2@example.com',
    'person3@example.com'
]

for recipient in recipients:
    success = sender.send_email(
        receiver_email=recipient,
        subject='공지사항',
        body='중요한 공지사항입니다.'
    )
    if success:
        print(f'{recipient}에게 전송 완료')
```

## 환경 변수 사용 (권장)

비밀번호를 코드에 직접 넣지 않고 환경 변수를 사용하는 것이 안전합니다.

### .env 파일 생성

```bash
# .env 파일 내용
GMAIL_ADDRESS=myemail@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
```

### Python 코드

```python
import os
from sendmail import GmailSender

# 환경 변수에서 읽기
sender_email = os.environ.get('GMAIL_ADDRESS')
sender_password = os.environ.get('GMAIL_APP_PASSWORD')

sender = GmailSender(sender_email, sender_password)
sender.send_email(
    receiver_email='friend@example.com',
    subject='안전한 메일',
    body='환경 변수를 사용한 메일 전송'
)
```

## 트러블슈팅

### 문제: "인증 실패" 오류

**원인:**

- 일반 Gmail 비밀번호 사용
- 잘못된 앱 비밀번호
- 2단계 인증 미활성화

**해결방법:**

1. Gmail 2단계 인증 활성화
2. 새로운 앱 비밀번호 생성
3. 앱 비밀번호 16자리를 정확히 입력 (공백 없이)

### 문제: "서버 연결 실패"

**원인:**

- 네트워크 연결 문제
- 방화벽 차단
- 잘못된 포트 번호

**해결방법:**

1. 인터넷 연결 확인
2. 방화벽에서 포트 587 허용
3. smtp.gmail.com 도메인 접근 가능 확인

### 문제: "파일을 찾을 수 없습니다"

**원인:**

- 잘못된 파일 경로
- 파일이 존재하지 않음
- 상대 경로 오류

**해결방법:**

1. 절대 경로 사용: `/Users/kogun/Desktop/file.txt`
2. 파일 존재 확인: `ls /path/to/file`
3. 현재 디렉토리 확인: `pwd`

### 문제: "파일이 너무 큽니다"

**원인:**

- 첨부 파일이 25MB 초과

**해결방법:**

1. 파일 압축
2. 클라우드 링크 공유
3. 여러 메일로 분할

## SMTP 포트 정보

| 포트    | 암호화  | 설명                             |
| ------- | ------- | -------------------------------- |
| 25      | 없음    | 기본 SMTP (보안 취약)            |
| 465     | SSL     | SSL 암호화 (구식)                |
| **587** | **TLS** | **권장 포트 (본 스크립트 사용)** |
| 2525    | TLS     | 대체 포트                        |

## 지원되는 파일 형식

첨부 파일로 모든 형식을 지원합니다:

- 문서: PDF, DOCX, TXT, ODT
- 이미지: JPG, PNG, GIF, BMP
- 압축: ZIP, RAR, 7Z, TAR.GZ
- 스프레드시트: XLSX, CSV, ODS
- 프레젠테이션: PPTX, ODP
- 기타: 모든 바이너리 파일

## 성능 최적화

### 대용량 파일 전송

```python
# 대용량 파일은 압축하여 전송
import zipfile

def compress_file(input_file, output_file):
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_file)

compress_file('large_file.pdf', 'large_file.zip')

sender.send_email(
    receiver_email='friend@example.com',
    subject='대용량 파일',
    body='압축 파일을 첨부합니다.',
    attachments=['large_file.zip']
)
```

### 대량 메일 전송

```python
import time

for i, recipient in enumerate(recipients):
    sender.send_email(recipient, subject, body)
    # 스팸 방지를 위한 딜레이
    if (i + 1) % 10 == 0:
        time.sleep(60)  # 10통마다 1분 대기
```

## 보안 체크리스트

- [ ] Gmail 2단계 인증 활성화
- [ ] 앱 비밀번호 사용
- [ ] 코드에 비밀번호 하드코딩 금지
- [ ] 환경 변수 또는 설정 파일 사용
- [ ] .gitignore에 .env 파일 추가
- [ ] 불필요한 권한 최소화
- [ ] 정기적으로 앱 비밀번호 갱신

## 추가 리소스

- [Gmail SMTP 공식 문서](https://support.google.com/mail/answer/7126229)
- [Python smtplib 문서](https://docs.python.org/3/library/smtplib.html)
- [Python email 패키지 문서](https://docs.python.org/3/library/email.html)
- [PEP 8 스타일 가이드](https://peps.python.org/pep-0008/)

## 문의

문제가 발생하면 다음 정보와 함께 문의하세요:

- Python 버전
- 오류 메시지
- 실행 환경 (OS, 네트워크)
- 재현 단계
