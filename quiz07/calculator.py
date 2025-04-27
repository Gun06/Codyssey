import sys
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# PyQt5 설치 확인 및 설치 함수
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

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset_all()

    # 계산기 초기화
    def reset_all(self):
        self.current_value = '0'  # 계산기 디스플레이에 0을 초기값으로 설정
        self.operator = None  # 연산자 초기화
        self.last_value = None  # 마지막 계산값 초기화
        self.display.setText('0')  # 디스플레이에 0을 표시

    def initUI(self):
        self.setWindowTitle('Calculator')  # 윈도우 타이틀 설정
        self.btn_font = QFont('Arial', 20)
        
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        center_widget.setStyleSheet("background-color: black;")

        vbox = QVBoxLayout(center_widget)

        # 디스플레이 부분 정의(QLineEdit)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText('0')

        self.display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: none;
                font-size: 36px;
                padding: 10px;
            }
        """)
        
        vbox.addWidget(self.display)

        grid = QGridLayout()
        vbox.addLayout(grid)

        buttons = [
            [('AC', 'function'), ('+/-', 'function'), ('%', 'function'), ('/', 'operator')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('*', 'operator')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('-', 'operator')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operator')],
            [('0', 'number'), ('.', 'number'), ('=', 'operator')]
        ]

        # 버튼 배치
        for row_idx, row_values in enumerate(buttons):
            col_idx = 0
            for val, role in row_values:
                if val is None:
                    col_idx += 1
                    continue
                btn = self.create_button(val, role)
                btn.clicked.connect(self.onButtonClicked)
                if val == '0':
                    grid.addWidget(btn, row_idx, col_idx, 1, 2)
                    col_idx += 2
                else:
                    grid.addWidget(btn, row_idx, col_idx)
                    col_idx += 1
        
        self.resize(300, 600)

    def onButtonClicked(self):
        btn = self.sender()
        key = btn.text()

        # 숫자일 경우
        if key.isdigit():
            if self.current_value == '0':
                self.current_value = key
            else:
                self.current_value += key
            self.display.setText(self.current_value)
        
        # 소수점일 경우
        elif key == '.':
            if '.' not in self.current_value:
                self.current_value += '.'
                self.display.setText(self.current_value)
        
        # 연산자를 눌렀을 경우
        elif key in ['+','-','*','/']:
            self.operator = key
            self.last_value = self.current_value
            self.current_value = '0'
            self.display.setText(self.current_value)
        
        # '=' 버튼을 눌렀을 경우
        elif key == '=':
            self.equal()
        
        # 'AC' 버튼을 눌렀을 경우 == 초기화
        elif key == 'AC':
            self.reset_all()
        
        # '+/-' 버튼을 눌렀을 경우 == 부호 변경
        elif key == '+/-':
            self.negative_positive()
        
        # '%' 버튼을 눌렀을 경우 퍼센트 계산
        elif key == '%':
            self.percent()

    # 계산 로직
    def calculate(self, left, right, op):
        if op == '+':
            return self.add(left, right)
        elif op == '-':
            return self.subtract(left, right)
        elif op == '*':
            return self.multiply(left, right)
        elif op == '/':
            return self.divide(left, right)
        return 0

    # 사칙연산 메소드 추가
    def add(self, left, right):
        return left + right

    def subtract(self, left, right):
        return left - right

    def multiply(self, left, right):
        return left * right

    def divide(self, left, right):
        if right == 0:
            return "Error"  # 나누기 0 오류 처리
        return left / right

    # 결과 출력 메소드 추가
    def equal(self):
        if self.operator and self.last_value is not None:
            result = self.calculate(
                float(self.last_value),
                float(self.current_value),
                self.operator
            )

            # 쉼표 추가한 문자열로 포맷
            if result == int(result):
                formatted = f"{int(result):,}"
            else:
                formatted = f"{result:,.10f}".rstrip('0').rstrip('.')

            self.current_value = str(result)
            self.display.setText(formatted)

            # 연속 계산 편의상 last_value에 결과값 저장
            self.last_value = self.current_value

    # 음수/양수 변환
    def negative_positive(self):
        if self.current_value == '0':
            return  # 0일 때는 부호 변경을 하지 않음
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = '-' + self.current_value
        self.display.setText(self.current_value)

    # 퍼센트 계산
    def percent(self):
        value = float(self.current_value) / 100.0
        self.current_value = str(value)
        self.display.setText(self.current_value)

    # 버튼 스타일 함수 정의
    def create_button(self, label, role='number'):
        btn = QPushButton(label)
        if label == '0' and role == 'number':
            btn.setFixedSize(170, 80)  # 가로 2칸 정도로
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border: none;
                    border-radius: 40px;
                    font-size: 24px;
                    padding-left: 30px;
                    text-align: left;
                }
                QPushButton:pressed {
                    background-color: #444444;
                }
            """)
        else:
            btn.setFixedSize(80, 80)
            if role == 'number':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #333333;
                        color: white;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                    }
                    QPushButton:pressed {
                        background-color: #444444;
                    }
                """)
            elif role == 'operator':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9500;
                        color: white;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                    }
                    QPushButton:pressed {
                        background-color: #e07e00;
                    }
                """)
            elif role == 'function':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #A5A5A5;
                        color: black;
                        border: none;
                        border-radius: 40px;
                        font-size: 24px;
                    }
                    QPushButton:pressed {
                        background-color: #BBBBBB;
                    }
                """)
        return btn


if __name__ == '__main__':
    app = QApplication([])
    window = Calculator()
    window.show()
    app.exec_()
