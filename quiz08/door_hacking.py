import itertools
import zipfile
import string
import os
import multiprocessing
from datetime import datetime

# 전역 설정
folder_path = '/Users/kogun/Desktop/Codyssey_dev/quiz08'
zip_filename = 'Emergency Storage Key.zip'
zip_path = os.path.join(folder_path, zip_filename)
password_file_path = os.path.join(folder_path, 'password.txt')
checkpoint_path = os.path.join(folder_path, 'checkpoint.txt')

# 흔한 비밀번호 리스트
common_passwords = [
    '123456', 'password', 'abc123', '111111', '000000', 'qwerty',
    'letmein', 'football', 'iloveyou', 'admin', 'welcome'
]

# 문자 + 숫자 smart brute force 생성기
def smart_brute_force():
    letters = string.ascii_lowercase
    digits = string.digits
    for first in itertools.product(letters, repeat=3):
        for second in itertools.product(digits, repeat=3):
            yield ''.join(first) + ''.join(second)

# 체크포인트 저장
def save_checkpoint(password):
    with open(checkpoint_path, 'w') as f:
        f.write(password)

# 체크포인트 불러오기
def load_checkpoint():
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'r') as f:
            return f.read().strip()
    return None

# 비밀번호 시도하는 함수 (멀티프로세싱용)
def try_password(password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(pwd=password.encode('utf-8'))
            return password
    except:
        return None

def unlock_zip():
    print(f"🔓 Zip 파일 암호 해제 시작: {zip_path}")
    
    # 1. Wordlist 우선 시도
    print("📚 Wordlist로 시도 중...")
    for password in common_passwords:
        result = try_password(password)
        if result:
            found_password(result)
            return

    print("⚡ Wordlist 실패. Smart Brute Force로 넘어갑니다...")

    # 2. Smart Brute Force 시도
    all_passwords = list(smart_brute_force())

    # 체크포인트 불러오기
    last_tried_password = load_checkpoint()
    if last_tried_password:
        print(f"⏩ 체크포인트 발견. {last_tried_password}부터 이어서 시작.")
        try:
            last_idx = all_passwords.index(last_tried_password)
            all_passwords = all_passwords[last_idx + 1:]
        except ValueError:
            pass  # 체크포인트에 문제가 있으면 처음부터

    # 병렬 처리 시작
    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpu_count)
    print(f"🚀 병렬처리 시작 (CPU {cpu_count}개)")

    chunk_size = 100000
    for idx, password in enumerate(pool.imap_unordered(try_password, all_passwords, chunksize=chunk_size)):
        if password:
            pool.terminate()
            found_password(password)
            return

        # 1000개마다 체크포인트 저장
        if idx % 100000 == 0:
            save_checkpoint(all_passwords[idx])
            print(f"💾 체크포인트 저장: {all_passwords[idx]} (시도 {idx}개)")

    pool.close()
    pool.join()

    print("❌ 모든 조합 시도했지만 비밀번호를 찾지 못했습니다.")

def found_password(password):
    found_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(password_file_path, 'w') as f:
        f.write(f"비밀번호: {password}\n찾은 시간: {found_time}")
    print(f"\n✅ 비밀번호 찾음! 👉 {password}")
    print(f"✅ password.txt 파일 저장 완료: {password_file_path}")
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)  # 성공하면 체크포인트 삭제

if __name__ == "__main__":
    unlock_zip()
