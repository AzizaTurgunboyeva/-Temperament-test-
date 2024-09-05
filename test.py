from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QRadioButton, QVBoxLayout
from PyQt5.QtGui import QIcon
#27.08.2024

class Variant:
    def __init__(self, text, ballar) -> None:
        self.text = text
        self.ballar = ballar

class Question:
    def __init__(self, text, variant) -> None:
        self.text = text
        self.variant = variant

class Matn(QLabel):
    def __init__(self, text: str, window) -> None:
        super().__init__(text, window)
        self.setStyleSheet("font-size:22px; color:black; font-weight:bold")
        self.adjustSize()

class User_button(QPushButton):
    def __init__(self, text: str, window) -> None:
        super().__init__(text, window)
        self.setStyleSheet("""QPushButton {
            font-size: 20px;
            color: green;
            border: 1px solid black;
            border-radius: 25px;
        }
        QPushButton::pressed {
            font-size: 25px;
            background-color: red;
            border: 1px solid grey;
            border-radius: 25px;
        }
        """)

class USer_radio_b(QRadioButton):
    def __init__(self, text: str, window) -> None:
        super().__init__(text, window)
        self.setStyleSheet("font-size:20px;")
        self.adjustSize()

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Temperament Testi")
        self.setWindowIcon(QIcon("temperament.png"))
        self.resize(400, 560)  # O'lchamni o'zgartirish

        self.label = Matn("Temperamentingizni aniqlang", self)
        self.label.move(50, 50)

        self.start_button = User_button("Boshlash", self)
        self.start_button.move(150, 500)  # Tugma holatini o'zgartirish
        self.start_button.clicked.connect(self.boshlanish)

    def boshlanish(self):
        self.questions_window = QuestionsWindow()
        self.questions_window.show()
        self.close()

class QuestionsWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Savollar")
        self.setWindowIcon(QIcon("temperament.png"))
        self.resize(400, 560)  # O'lchamni o'zgartirish

        layout = QVBoxLayout(self)

        self.questions = [
            Question("Qaysi vaziyatda o'zingizni eng qulay his qilasiz?", [
                Variant("Do'stlar davrasida", 1),
                Variant("Raqobat sharoitida", 2),
                Variant("Yolg'izlikda", 3),
                Variant("Tinch, osuda joyda", 4),
            ]),
            Question("Biror yangi ishni boshlashdan oldin", [
                Variant("Rejalashtirmay ishga kirishasiz", 1),
                Variant("Hamma narsani nazorat qilasiz", 2),
                Variant("Avval barcha mumkin bo'lgan qiyinchiliklarni ko'rib chiqasiz", 3),
                Variant("Qulay va oson yo'lni izlaysiz", 4),
            ]),
            Question("Sizni nimadan qo'rqitish mumkin?", [
                Variant("Yolg'izlikdan", 1),
                Variant("Nazoratni yo'qotishdan", 2),
                Variant("Noma'lum va kutilmagan holatlardan", 3),
                Variant("Tashvish va asabiylikdan", 4),
            ]),
            Question("Sizning ish uslubingiz qanday?", [
                Variant("Jamoaviy va do'stona", 1),
                Variant("Qat'iy va faol", 2),
                Variant("O'ylangan va mulohazali", 3),
                Variant("Bosiq va xotirjam", 4),
            ]),
            Question("Siz qanday odamlar bilan ko'proq muloqot qilasiz?", [
                Variant("Keng doira bilan", 1),
                Variant("Yetakchilar va faol odamlar bilan", 2),
                Variant("Bir nechta yaqin do'stlar bilan", 3),
                Variant("Xotirjam va ishonchli odamlar bilan", 4),
            ]),
        ]

            
        

        self.savol_indexi = 0
        self.scores = []

        self.question_label = Matn("", self)
        layout.addWidget(self.question_label)

        self.radio_buttons = []
        for _ in range(4):
            rb = USer_radio_b("", self)
            layout.addWidget(rb)
            self.radio_buttons.append(rb)

        self.next_button = User_button("Keyingi", self)
        self.next_button.move(150, 520)  # Tugma holatini o'zgartirish
        layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.keyingi_button)

        self.birinchi_savol()

    def birinchi_savol(self):
        question = self.questions[self.savol_indexi]
        self.question_label.setText(question.text)
        self.question_label.adjustSize()

        for rb, option in zip(self.radio_buttons, question.variant):
            rb.setText(option.text)
            rb.setChecked(False)
            rb.adjustSize()

    def keyingi_button(self):
        self.save_score()
        if self.savol_indexi < len(self.questions) - 1:
            self.savol_indexi += 1
            self.birinchi_savol()
        else:
            self.finish_test()

    def save_score(self):
        for rb in self.radio_buttons:
            if rb.isChecked():
                option_text = rb.text()
                for variant in self.questions[self.savol_indexi].variant:
                    if variant.text == option_text:
                        self.scores.append(variant.ballar)
                        break

    def finish_test(self):
        total_score = sum(self.scores)
        self.result_window = ResultWindow(total_score)
        self.result_window.show()
        self.close()

class ResultWindow(QWidget):
    def __init__(self, score) -> None:
        super().__init__()
        self.setWindowTitle("Natija")
        self.setWindowIcon(QIcon("temperament.png"))
        self.resize(400, 560)  # O'lchamni o'zgartirish

        self.result_label = QLabel(self)
        self.result_label.setStyleSheet("font-size:22px; color:black; font-weight:bold")
        self.result_label.setWordWrap(True)

        result_text = self.get_result_text(score)
        self.result_label.setText(result_text)

        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def get_result_text(self, score):
        if 1 <= score <= 5:
            return ("Melanxolik - Siz mulohazali va sezgir odamsiz. Odatda, chuqur o'ylaysiz va "
                    "o'z his-tuyg'ularingizni ichingizda saqlaysiz.")
        elif 6 <= score <= 9:
            return ("Sangvinik - Siz ijtimoiy va energiyaga to'la odamsiz. Sizni doimo faoliyat va "
                    "muloqot ilhomlantiradi.")
        elif 10 <= score <= 13:
            return ("Xolerik - Siz yetakchi va maqsadga yo'naltirilgan odamsiz. Sizda kuchli iroda va "
                    "raqobatga bo'lgan ehtiros mavjud.")
        elif 14 <= score <= 16:
            return ("Flegmatik - Siz sokin, xotirjam va barqaror odamsiz. Sizga muvozanat va barqarorlik "
                    "yoqadi.")
        else:
            return "Natija topilmadi"

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

