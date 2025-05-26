# Caesar.py

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


def get_all_caesar_shifts(target_text: str) -> list:
    """
    Caesar Cipher로 0~25 shift에 대해 복호화한 결과를 리스트로 반환합니다.
    """
    decoded_list = []
    for shift in range(26):
        decoded = ""
        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char
        decoded_list.append(decoded)
    return decoded_list


def show_all_decoded_results(decoded_list: list) -> None:
    """
    모든 시프트 값(0~25)에 대해 복호화된 문자열을 출력합니다.
    """
    print("\n📜 Caesar Cipher 복호화 결과\n" + "=" * 50)
    for idx, decoded in enumerate(decoded_list):
        print(f"[SHIFT {idx:02d}] {decoded}")
    print("=" * 50)


def save_result_to_file(text: str, filepath='result.txt') -> None:
    """
    최종 선택된 복호 문자열을 result.txt에 저장합니다.
    예외 발생 시 경고 메시지를 출력합니다.
    """
    try:
        with open(filepath, 'w') as f:
            f.write(text)
        print(f"[INFO] 복호 결과가 {filepath}에 저장되었습니다.")
    except Exception as e:
        print(f"[ERROR] 파일 저장 중 문제가 발생했습니다: {e}")


if __name__ == '__main__':
    encrypted_text = read_password_file()

    if encrypted_text:
        decoded_list = get_all_caesar_shifts(encrypted_text)
        show_all_decoded_results(decoded_list)

        try:
            shift_input = int(input("\n👀 읽기 쉬운 복호 결과의 시프트 번호를 입력하세요 (0~25): "))
            if 0 <= shift_input < 26:
                selected_result = decoded_list[shift_input]
                save_result_to_file(selected_result)
            else:
                print("[ERROR] 유효하지 않은 시프트 번호입니다. 0~25 사이로 입력해주세요.")
        except ValueError:
            print("[ERROR] 숫자를 입력해야 합니다.")
