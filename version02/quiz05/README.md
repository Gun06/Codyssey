# Gmail SMTP 이메일 전송 스크립트

Python의 기본 제공 라이브러리를 사용하여 Gmail SMTP를 통해 이메일을 전송하는 스크립트입니다.

## 주요 기능

- ✉️ Gmail SMTP를 통한 이메일 전송
- 📎 첨부 파일 지원 (보너스 기능)
- 🔒 TLS 암호화 지원
- 🛡️ 완벽한 예외 처리
- 📝 PEP 8 스타일 가이드 준수

## SMTP 서버 정보

- **SMTP 서버**: smtp.gmail.com
- **포트 번호**: 587 (TLS)
- **암호화**: STARTTLS

## 사용된 Python 패키지

모두 Python 기본 제공 라이브러리입니다:

- `smtplib`: SMTP 프로토콜 클라이언트
- `email.mime.text`: 텍스트 메시지 생성
- `email.mime.multipart`: 멀티파트 메시지 생성
- `email.mime.base`: 첨부 파일 처리
- `email.encoders`: Base64 인코딩
- `os`: 파일 시스템 작업

## Gmail 앱 비밀번호 생성 방법

Gmail에서 2단계 인증을 사용하는 경우 앱 비밀번호를 생성해야 합니다:

1. Google 계정 관리 페이지로 이동
2. 보안 섹션으로 이동
3. "Google에 로그인" 섹션에서 "앱 비밀번호" 선택
4. 앱 및 기기 선택 (메일, 기타)
5. 생성된 16자리 비밀번호 복사

## 사용 방법

### 기본 사용법

```bash
python3 sendmail.py
```

실행 후 다음 정보를 입력:

- 발신자 Gmail 주소
- 발신자 Gmail 앱 비밀번호
- 수신자 이메일 주소
- 이메일 제목
- 이메일 본문
- 첨부 파일 경로 (선택사항)

### 코드 예제

```python
from sendmail import GmailSender

# Gmail Sender 인스턴스 생성
sender = GmailSender('your_email@gmail.com', 'your_app_password')

# 이메일 전송
success = sender.send_email(
    receiver_email='receiver@example.com',
    subject='테스트 메일',
    body='안녕하세요, 테스트 메일입니다.',
    attachments=['file1.pdf', 'file2.txt']  # 선택사항
)

if success:
    print('이메일 전송 성공!')
```

## 주요 클래스 및 메서드

### GmailSender 클래스

- `__init__(sender_email, sender_password)`: 초기화
- `connect_smtp_server()`: SMTP 서버 연결 및 로그인
- `create_message(receiver_email, subject, body, attachments)`: 메시지 생성
- `attach_file(message, file_path)`: 파일 첨부
- `send_email(receiver_email, subject, body, attachments)`: 이메일 전송
- `disconnect_smtp_server()`: 연결 종료

## 예외 처리

다음과 같은 예외들이 처리됩니다:

- `SMTPAuthenticationError`: 인증 실패
- `SMTPConnectError`: 서버 연결 실패
- `SMTPRecipientsRefused`: 수신자 주소 거부
- `SMTPDataError`: 데이터 전송 오류
- `SMTPException`: 일반 SMTP 오류
- `IOError`: 파일 읽기 오류
- `Exception`: 기타 예상치 못한 오류

## 첨부 파일 제한사항

- 최대 파일 크기: 25MB
- 지원 형식: 모든 파일 형식
- 다중 파일 첨부 가능

## 보안 주의사항

1. **앱 비밀번호 사용**: 일반 Gmail 비밀번호 대신 앱 비밀번호 사용
2. **2단계 인증 활성화**: Gmail 계정의 2단계 인증 권장
3. **비밀번호 보안**: 코드에 비밀번호를 하드코딩하지 마세요
4. **환경 변수 사용**: 민감한 정보는 환경 변수로 관리

## 문제 해결

### "인증 실패" 오류

- Gmail 앱 비밀번호를 사용하고 있는지 확인
- 2단계 인증이 활성화되어 있는지 확인
- 이메일 주소와 비밀번호가 정확한지 확인

### "서버 연결 실패" 오류

- 인터넷 연결 확인
- 방화벽 설정 확인
- SMTP 포트(587)가 차단되지 않았는지 확인

### "파일 첨부 실패" 오류

- 파일 경로가 정확한지 확인
- 파일이 존재하는지 확인
- 파일 크기가 25MB 이하인지 확인

## 코드 스타일

PEP 8 스타일 가이드를 준수합니다:

- 함수명: `snake_case`
- 클래스명: `PascalCase`
- 문자열: 작은따옴표(`'`) 기본 사용
- 들여쓰기: 공백 4칸
- 대입문: `=` 앞뒤 공백

## 라이선스

이 스크립트는 교육 목적으로 작성되었습니다.
