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

# 문자3+숫자3 Smart Brute Force 생성기
def smart_brute_force():
    letters = string.ascii_lowercase
    digits = string.digits
    for first in itertools.product(letters, repeat=3):
        for second in itertools.product(digits, repeat=3):
            yield ''.join(first) + ''.join(second)

# 전체 6자리 조합 생성기 (소문자 + 숫자)
def full_brute_force():
    characters = string.ascii_lowercase + string.digits
    return (''.join(p) for p in itertools.product(characters, repeat=6))

# 체크포인트 저장
def save_checkpoint(mode, password):
    with open(checkpoint_path, 'w') as f:
        f.write(f"{mode}:{password}")

# 체크포인트 불러오기
def load_checkpoint():
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'r') as f:
            data = f.read().strip()
            if ':' in data:
                mode, password = data.split(':', 1)
                return mode, password
    return None, None

# 비밀번호 시도 함수
def try_password(password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(pwd=password.encode('utf-8'))
            return password
    except:
        return None

def found_password(password):
    found_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(password_file_path, 'w') as f:
        f.write(f"비밀번호: {password}\n찾은 시간: {found_time}")
    print(f"\n✅ 비밀번호 찾음! 👉 {password}")
    print(f"✅ password.txt 파일 저장 완료: {password_file_path}")
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)

def unlock_zip():
    print(f"🔓 Zip 파일 암호 해제 시작: {zip_path}")

    # 0. 체크포인트 불러오기
    last_mode, last_password = load_checkpoint()

    # 1. Wordlist 우선 시도
    if last_mode is None or last_mode == 'wordlist':
        print("📚 Wordlist로 시도 중...")
        for password in common_passwords:
            if last_password and password <= last_password:
                continue  # 체크포인트 이후만 진행
            result = try_password(password)
            if result:
                found_password(result)
                return
            save_checkpoint('wordlist', password)
        print("⚡ Wordlist 실패. Smart Brute Force로 넘어갑니다.")
        last_mode = 'smart'
        last_password = None  # Smart로 넘어갈 때 초기화

    # 2. Smart Brute Force (문자3+숫자3)
    if last_mode == 'smart':
        print("🎯 Smart Brute Force(문자3+숫자3) 진행 중...")
        all_passwords = list(smart_brute_force())

        if last_password:
            try:
                last_idx = all_passwords.index(last_password)
                all_passwords = all_passwords[last_idx + 1:]
            except ValueError:
                pass  # 못 찾으면 처음부터

        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)

        chunk_size = 100000
        for idx, password in enumerate(pool.imap_unordered(try_password, all_passwords, chunksize=chunk_size)):
            if password:
                pool.terminate()
                found_password(password)
                return
            if idx % 100000 == 0 and idx < len(all_passwords):
                save_checkpoint('smart', all_passwords[idx])
                print(f"💾 Smart 체크포인트 저장: {all_passwords[idx]} (시도 {idx}개)")

        pool.close()
        pool.join()

        print("⚡ Smart Brute Force 실패. 전체 6자리 브루트포스로 넘어갑니다.")
        last_mode = 'full'
        last_password = None  # Full로 넘어갈 때 초기화

    # 3. 전체 6자리 완전탐색 (소문자+숫자)
    if last_mode == 'full':
        print("🌎 전체 6자리 조합(Full Brute Force) 진행 중...")
        all_passwords = full_brute_force()

        skip = True if last_password else False

        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)

        chunk_size = 100000
        for idx, password in enumerate(pool.imap_unordered(try_password, all_passwords, chunksize=chunk_size)):
            if skip:
                if password == last_password:
                    skip = False
                continue

            if password:
                pool.terminate()
                found_password(password)
                return
            if idx % 100000 == 0:
                save_checkpoint('full', password)
                print(f"💾 Full 체크포인트 저장: {password} (시도 {idx}개)")

        pool.close()
        pool.join()

    print("❌ 모든 방법을 시도했지만 비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    unlock_zip()
