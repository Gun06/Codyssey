import itertools
import zipfile
import string
import os
from datetime import datetime

def unlock_zip():
    # 1. zip 파일 경로 설정
    folder_path = '/Users/kogun/Desktop/Codyssey_dev/quiz08'
    zip_filename = 'Emergency Storage Key.zip'
    zip_path = os.path.join(folder_path, zip_filename)

    # 2. 비밀번호 후보 문자: 소문자 + 숫자
    characters = string.ascii_lowercase + string.digits

    success = False  # 성공 여부 플래그

    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # 3. 모든 6자리 조합 생성
        for idx, password_tuple in enumerate(itertools.product(characters, repeat=6), start=1):
            password = ''.join(password_tuple)  # 튜플을 문자열로 변환
            try:
                # 4. 비밀번호 시도
                zip_file.extractall(pwd=password.encode('utf-8'))
                success = True
                break  # 성공했으면 루프 탈출
            except:
                if idx % 1000 == 0:
                    print(f"시도 {idx}번째: 현재 비밀번호 {password}")

    # 5. 성공했을 때 password.txt 작성
    if success:
        password_file_path = os.path.join(folder_path, 'password.txt')
        found_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(password_file_path, 'w') as f:
            f.write(f"비밀번호: {password}\n찾은 시간: {found_time}")

        print(f"\n 비밀번호 찾음! 👉 {password}")
        print(f" password.txt 파일 저장 완료: {password_file_path}")
    else:
        print("\n 모든 조합 시도했지만 비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    unlock_zip()
