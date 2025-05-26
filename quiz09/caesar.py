# door_hacking.py

def read_password_file(filepath='password.txt') -> str:
    """
    password.txt 파일에서 암호화된 문자열을 읽어옵니다.
    """
    try:
        with open(filepath, 'r') as f:
            password = f.read().strip()
        print(f"[INFO] password.txt에서 읽은 문자열: {password}")
        return password
    except FileNotFoundError:
        print(f"[ERROR] 파일을 찾을 수 없습니다: {filepath}")
        return ""


if __name__ == '__main__':
    encrypted_text = read_password_file()
    # 이후 caesar_cipher_decode(encrypted_text) 같은 함수를 연결할 예정
