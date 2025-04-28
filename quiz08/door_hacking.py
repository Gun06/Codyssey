import itertools
import zipfile
import string
import os

def unlock_zip():
    # 1. zip 파일 경로 설정
    folder_path = '/Users/kogun/Desktop/Codyssey_dev/quiz08'
    zip_filename = 'Emergency Storage Key.zip'
    zip_path = os.path.join(folder_path, zip_filename)

    # 2. zip 파일 열기
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # 3. 비밀번호 후보 문자: 소문자 + 숫자
        characters = string.ascii_lowercase + string.digits

        # 4. 모든 6자리 조합 생성
        for idx, password_tuple in enumerate(itertools.product(characters, repeat=6), start=1):
            password = ''.join(password_tuple)  # 튜플을 문자열로 변환
            try:
                # 5. 비밀번호 시도
                zip_file.extractall(pwd=password.encode('utf-8'))
                print(f"\n비밀번호 찾음! 👉 {password}")
                return password  # 비밀번호를 찾으면 리턴하고 함수 종료
            except:
                if idx % 100000 == 0:
                    print(f"시도 {idx}번째: 현재 비밀번호 {password}")

    print("\n모든 조합 시도했지만 비밀번호를 찾지 못했습니다.")
    return None

# 함수 호출 예시
if __name__ == "__main__":
    unlock_zip()
