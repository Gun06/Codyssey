def read_file(filename):
    """
    주어진 텍스트 파일을 읽어서 문자열로 반환합니다.
    예외 발생 시 에러 메시지를 출력하고 빈 문자열을 반환합니다.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[에러] 파일을 찾을 수 없습니다: {filename}")
        return ''
    except Exception as e:
        print(f"[에러] {filename} 파일을 읽는 중 문제가 발생했습니다: {e}")
        return ''


def write_file(filename, content):
    """
    주어진 내용을 텍스트 파일로 저장합니다.
    예외 발생 시 에러 메시지를 출력합니다.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[성공] 결과가 {filename}에 저장되었습니다.")
    except Exception as e:
        print(f"[에러] 결과 파일을 저장하는 중 문제가 발생했습니다: {e}")


def get_all_caesar_shifts(text):
    """
    Caesar Cipher로 0~25 시프트에 대해 복호화된 문자열 리스트를 반환합니다.
    """
    decoded_list = []
    for shift in range(26):
        result = ''
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base - shift) % 26 + base)
            else:
                result += char
        decoded_list.append(result)
    return decoded_list


def caesar_cipher_decode_with_dictionary(target_text):
    """
    dictionary.txt에 존재하는 단어가 복호화된 문자열에 포함되면 자동 종료하고,
    포함되지 않을 경우 수동 입력을 받아 복호화 결과를 저장합니다.
    """
    dict_words = set()
    dictionary_text = read_file('dictionary.txt')
    if dictionary_text:
        for word in dictionary_text.splitlines():
            dict_words.add(word.strip().lower())

    decoded_list = get_all_caesar_shifts(target_text)

    print("\n[정보] Caesar Cipher 복호화 결과 (shift 0~25):\n" + "=" * 50)
    for idx, decoded in enumerate(decoded_list):
        print(f"[{idx:02d}] {decoded}")

        # 단어 단위로 나눈 후 사전과 일치 여부 확인
        words = decoded.lower().split()
        if any(word in dict_words for word in words):
            print(f"\n[자동 감지] 사전 단어가 포함된 결과 발견 (shift={idx})")
            write_file('result.txt', decoded)
            return
    print("=" * 50)

    # 수동 입력 fallback
    try:
        key = int(input("\n해독된 것으로 보이는 shift 값을 입력하세요 (0~25): "))
        if 0 <= key < 26:
            write_file('result.txt', decoded_list[key])
        else:
            print("[오류] 0부터 25 사이의 숫자를 입력해야 합니다.")
    except ValueError:
        print("[오류] 숫자를 입력해야 합니다.")
    except Exception as e:
        print(f"[오류] 입력 처리 중 예외 발생: {e}")


if __name__ == '__main__':
    cipher_text = read_file('password.txt')
    if cipher_text:
        caesar_cipher_decode_with_dictionary(cipher_text)