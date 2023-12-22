import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_operation = QLabel()
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("Calculator: ")
        self.equation = QLineEdit("")
        
        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(label_equation, self.equation)

        ### 계산결과를 나타내기 위해 QLineEdit를 추가, 입출력은 한곳에서만 해야하므로 hide()함수를 통해 숨김 
        self.result = QLineEdit("")
        self.result.setReadOnly(True) 
        self.result.hide()
        layout_equation_solution.addRow(self.result)

         # QGridLayout으로 변경
        layout_operation = QGridLayout()
        layout_number = QGridLayout()

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("÷")
        button_remain = QPushButton("%")
        button_reciprocal = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_root = QPushButton("√x")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))        
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_remain.clicked.connect(lambda state, operation="%": self.button_operation_clicked(operation))
        button_reciprocal.clicked.connect(self.button_reciprocal_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_root.clicked.connect(self.button_root_clicked)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear1 = QPushButton("C")
        button_clear2 = QPushButton("CE")
        button_backspace = QPushButton("Backspace")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear1.clicked.connect(self.button_clear_clicked)
        button_clear2.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        # layout_operation.addWidget(button_plus)
        # layout_operation.addWidget(button_minus)
        # layout_operation.addWidget(button_product)
        layout_operation.addWidget(button_reciprocal, 1, 0)
        layout_operation.addWidget(button_square, 1, 1)
        layout_operation.addWidget(button_root, 1, 2)
        layout_operation.addWidget(button_division, 1, 3)
        layout_operation.addWidget(button_remain, 0, 0)
        layout_operation.addWidget(button_clear2, 0, 1)
        layout_operation.addWidget(button_clear1, 0, 2)
        layout_operation.addWidget(button_backspace, 0, 3)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if 3 >= number >= 1:
                x,y = divmod(number + 5, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif 6 >= number >= 4:
                x,y = divmod(number - 1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number >= 7:
                x,y = divmod(number - 7, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_PlusMinus = QPushButton("+/-")
        layout_number.addWidget(button_PlusMinus, 3, 0)
        # button_double_zero = QPushButton("00")
        # button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        # layout_number.addWidget(button_double_zero, 3, 0)

        # 연산 기호를 숫자 옆에 배치
        layout_number.addWidget(button_product, 0, 3)
        layout_number.addWidget(button_minus, 1, 3)
        layout_number.addWidget(button_plus, 2, 3)
        layout_number.addWidget(button_equal, 3, 3)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_operation)
        main_layout.addLayout(layout_number)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    # 윈도우 계산기와 같이 입력창 초기화
    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText("") 
        self.result.setText(equation)

    def button_reciprocal_clicked(self):
        operand = float(self.equation.text())
        result = 1 / operand
        self.result.setText(str(result))
        self.equation.setText(str(result))

    def button_square_clicked(self):
        operand = float(self.equation.text())
        result = operand ** 2
        self.result.setText(str(result))
        self.equation.setText(str(result))

    def button_root_clicked(self):
        operand = float(self.equation.text())
        result = operand ** 0.5
        self.result.setText(str(result))
        self.equation.setText(str(result))

    # 숨긴 result창을 통해 결과를 구하고 출력하기
    def button_equal_clicked(self):
        equation = self.equation.text()
        result = self.result.text()
        result += equation
        result = eval(result)
        self.result.setText(str(result))
        self.equation.setText(str(result))

    def button_clear_clicked(self):
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())