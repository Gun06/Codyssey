import sys
import subprocess
import platform

def check_and_install_pyqt():
    try:
        # PyQt5가 설치되어 있는지 확인
        import PyQt5
        print("PyQt5 is already installed.")
    except ImportError:
        print("PyQt5 is not installed. Installing now...")

        # 운영 체제에 맞는 명령어로 PyQt5 설치
        if platform.system() == "Windows":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqt5"])
        elif platform.system() == "Linux":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqt5"])
        elif platform.system() == "Darwin":  # macOS
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqt5"])
        else:
            print("Unsupported OS. Please install PyQt5 manually.")
            return

        print("PyQt5 installation completed.")

# 호출하여 PyQt5 설치 여부 확인 및 설치
check_and_install_pyqt()

# 이후 PyQt5 사용 예제 코드 추가 가능
