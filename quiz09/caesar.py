# caesar.py

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


def caesar_cipher_decode(target_text: str) -> None:
    """
    Caesar Cipher 방식으로 target_text를 복호화하여
    시프트 수(0~25)에 따라 출력합니다.
    """
    if not target_text:
        print("[WARN] 복호화할 문자열이 비어있습니다.")
        return

    print("\n=== Caesar Cipher 복호화 시도 ===\n")
    for shift in range(26):
        decoded = ""
        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char
        print(f"[{shift:02d}] {decoded}")


if __name__ == '__main__':
    encrypted_text = read_password_file()
    caesar_cipher_decode(encrypted_text)