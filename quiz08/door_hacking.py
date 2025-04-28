import itertools
import zipfile
import string
import os
import multiprocessing
from datetime import datetime

# 경로 설정
folder_path = '/Users/kogun/Desktop/Codyssey_dev/quiz08'
zip_filename = 'Emergency Storage Key.zip'
zip_path = os.path.join(folder_path, zip_filename)
password_file_path = os.path.join(folder_path, 'password.txt')
checkpoint_path = os.path.join(folder_path, 'checkpoint.txt')

# Wordlist
common_passwords = [
    '123456', 'password', 'abc123', '111111', '000000', 'qwerty',
    'letmein', 'football', 'iloveyou', 'admin', 'welcome'
]

# Smart Brute Force: 문자 3자리 + 숫자 3자리
def smart_brute_force():
    letters = string.ascii_lowercase
    digits = string.digits
    for first in itertools.product(letters, repeat=3):
        for second in itertools.product(digits, repeat=3):
            yield ''.join(first) + ''.join(second)

# Full Brute Force: 소문자 + 숫자 6자리
def full_brute_force():
    characters = string.ascii_lowercase + string.digits
    return (''.join(p) for p in itertools.product(characters, repeat=6))

# Checkpoint 저장
def save_checkpoint(mode, last_try, status='trying', found_password=None, found_time=None):
    with open(checkpoint_path, 'w') as f:
        f.write(f"mode:{mode}\n")
        f.write(f"last_try:{last_try}\n")
        f.write(f"status:{status}\n")
        if found_password:
            f.write(f"found_password:{found_password}\n")
        if found_time:
            f.write(f"found_time:{found_time}\n")

# Checkpoint 불러오기
def load_checkpoint():
    if os.path.exists(checkpoint_path):
        data = {}
        with open(checkpoint_path, 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    data[key] = value
        return data
    return {}

# 비밀번호 시도
def try_password(password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(pwd=password.encode('utf-8'))
            return password
    except:
        return None

# 비밀번호 찾았을 때 처리
def found_password(password, mode):
    found_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(password_file_path, 'w') as f:
        f.write(f"비밀번호: {password}\n찾은 시간: {found_time}")

    save_checkpoint(mode, password, status='success', found_password=password, found_time=found_time)

    print(f"\n✅ 비밀번호 찾음! 👉 {password}")
    print(f"✅ password.txt 파일 저장 완료: {password_file_path}")

def unlock_zip():
    print(f"🔓 Zip 파일 암호 해제 시작: {zip_path}")

    checkpoint = load_checkpoint()
    last_mode = checkpoint.get('mode')
    last_try = checkpoint.get('last_try')
    last_status = checkpoint.get('status')

    # 1. Wordlist 시도
    if last_mode is None or last_mode == 'wordlist':
        print("📚 Wordlist로 시도 중...")
        start_idx = 0
        if last_mode == 'wordlist' and last_try in common_passwords:
            start_idx = common_passwords.index(last_try) + 1

        for idx, password in enumerate(common_passwords[start_idx:], start=start_idx):
            result = try_password(password)
            if result:
                found_password(result, 'wordlist')
                return
            if idx % 5 == 0:
                save_checkpoint('wordlist', password)
                print(f"💾 Wordlist 체크포인트 저장: {password}")

        print("⚡ Wordlist 실패. Smart Brute Force로 넘어갑니다.")
        last_mode = 'smart'
        last_try = None

    # 2. Smart Brute Force 시도
    if last_mode == 'smart':
        print("🎯 Smart Brute Force(문자3+숫자3) 진행 중...")
        all_passwords = list(smart_brute_force())

        if last_try:
            try:
                last_idx = all_passwords.index(last_try)
                all_passwords = all_passwords[last_idx + 1:]
            except ValueError:
                pass

        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)
        chunk_size = 100000

        for idx, password_attempt in enumerate(all_passwords):
            result = pool.apply_async(try_password, (password_attempt,))
            found = result.get()
            if found:
                pool.terminate()
                found_password(found, 'smart')
                return

            if idx % 100000 == 0:
                save_checkpoint('smart', password_attempt)
                print(f"💾 Smart 체크포인트 저장: {password_attempt} (시도 {idx}개)")

        pool.close()
        pool.join()

        print("⚡ Smart Brute Force 실패. Full Brute Force로 넘어갑니다.")
        last_mode = 'full'
        last_try = None

    # 3. Full Brute Force 시도
    if last_mode == 'full':
        print("🌎 전체 6자리 조합(Full Brute Force) 진행 중...")
        all_passwords = list(full_brute_force())

        if last_try:
            try:
                last_idx = all_passwords.index(last_try)
                all_passwords = all_passwords[last_idx + 1:]
            except ValueError:
                pass

        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)
        chunk_size = 100000

        for idx, password_attempt in enumerate(all_passwords):
            result = pool.apply_async(try_password, (password_attempt,))
            found = result.get()
            if found:
                pool.terminate()
                found_password(found, 'full')
                return

            if idx % 100000 == 0:
                save_checkpoint('full', password_attempt)
                print(f"💾 Full 체크포인트 저장: {password_attempt} (시도 {idx}개)")

        pool.close()
        pool.join()

    print("❌ 모든 방법을 시도했지만 비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    unlock_zip()
