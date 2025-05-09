import sys
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
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

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        # UI 초기화
        self.initUI()

    def initUI(self):
        # 출력 디스플레이
        self.display = QLineEdit(self)
        self.display.setAlignment(Qt.AlignRight)
        
        # 명시적으로 QFont 객체를 생성하여 폰트를 설정
        font = QFont("Arial", 24)
        self.display.setFont(font)
        
        self.display.setReadOnly(True)
        self.display.setText("0")

        # 레이아웃 설정
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.display)

        gridLayout = QGridLayout()
        buttons = [
            ('AC', self.clear), ('+/-', self.toggle_sign), ('%', self.percent), ('÷', self.set_operator),
            ('7', self.append_digit), ('8', self.append_digit), ('9', self.append_digit), ('×', self.set_operator),
            ('4', self.append_digit), ('5', self.append_digit), ('6', self.append_digit), ('-', self.set_operator),
            ('1', self.append_digit), ('2', self.append_digit), ('3', self.append_digit), ('+', self.set_operator),
            ('0', self.append_digit), ('.', self.append_digit), ('=', self.calculate)
        ]

        # 버튼 생성
        row, col = 1, 0
        for button_text, handler in buttons:
            button = QPushButton(button_text, self)
            button.clicked.connect(lambda _, text=button_text, handler=handler: handler(text))
            gridLayout.addWidget(button, row, col, 1, 1)
            col += 1
            if col > 3:
                col = 0
                row += 1

        mainLayout.addLayout(gridLayout)
        self.setLayout(mainLayout)

        # 윈도우 설정
        self.setWindowTitle('Calculator')
        self.setGeometry(300, 300, 350, 400)

        self.operator = None
        self.first_operand = None

    # 숫자 버튼 클릭 시 처리
    def append_digit(self, digit):
        current_text = self.display.text()
        if current_text == "0":
            self.display.setText(digit)
        else:
            self.display.setText(current_text + digit)

    # 연산자 버튼 클릭 시 처리
    def set_operator(self, operator):
        if self.operator is None:
            self.first_operand = float(self.display.text())
            self.operator = operator
            self.display.setText("0")
        else:
            self.calculate()
            self.operator = operator
            self.first_operand = float(self.display.text())
            self.display.setText("0")

    # 계산 버튼 처리
    def calculate(self, _=None):
        second_operand = float(self.display.text())
        
        if self.operator == "+":
            result = self.first_operand + second_operand
        elif self.operator == "-":
            result = self.first_operand - second_operand
        elif self.operator == "×":
            result = self.first_operand * second_operand
        elif self.operator == "÷":
            if second_operand == 0:
                result = "Error"
            else:
                result = self.first_operand / second_operand

        self.display.setText(str(result))
        self.operator = None
        self.first_operand = None

    # AC 버튼 클릭 시 처리
    def clear(self, _=None):
        self.display.setText("0")
        self.operator = None
        self.first_operand = None

    # +/- 버튼 클릭 시 처리
    def toggle_sign(self, _=None):
        current_text = self.display.text()
        if current_text.startswith('-'):
            self.display.setText(current_text[1:])
        else:
            self.display.setText('-' + current_text)

    # % 버튼 클릭 시 처리
    def percent(self, _=None):
        current_text = self.display.text()
        self.display.setText(str(float(current_text) / 100))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())