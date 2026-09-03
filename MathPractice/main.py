from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import random


# ============================================================
# LOAD FILE KV
# ============================================================

Builder.load_file("mathpractice.kv")


# ============================================================
# SCREEN
# ============================================================

class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class OperationScreen(Screen):
    pass


class LevelScreen(Screen):
    pass


class QuizScreen(Screen):

    question = StringProperty("")
    question_number = NumericProperty(1)
    score = NumericProperty(0)
    correct_answer = NumericProperty(0)

    # Pesan benar / salah
    feedback = StringProperty("")
    feedback_color = StringProperty("")

    # ========================================================
    # FOCUS INPUT
    # ========================================================

    def focus_input(self, *args):
        if "answer_input" in self.ids:
            self.ids.answer_input.focus = True

    # ========================================================
    # MULAI QUIZ
    # ========================================================

    def start_quiz(self):

        self.question_number = 1
        self.score = 0

        self.feedback = ""
        self.feedback_color = ""

        self.new_question()

        if "answer_input" in self.ids:
            self.ids.answer_input.text = ""

        # Fokus otomatis ke input
        Clock.schedule_once(self.focus_input, 0.3)

    # ========================================================
    # MEMBUAT SOAL
    # ========================================================

    def new_question(self):

        app = App.get_running_app()

        operation = app.selected_operation
        level = app.selected_level

        # Reset feedback setiap ganti soal
        self.feedback = ""
        self.feedback_color = ""

        # ====================================================
        # PERKALIAN
        # ====================================================

        if operation == "Perkalian":

            if level == "A":
                a = random.randint(1, 9)
                b = random.randint(1, 9)

            elif level == "B":
                a = random.randint(10, 50)
                b = random.randint(10, 50)

            else:
                a = random.randint(60, 100)
                b = random.randint(60, 100)

            self.question = f"{a} × {b} = ?"
            self.correct_answer = a * b

        # ====================================================
        # PEMBAGIAN
        # ====================================================

        elif operation == "Pembagian":

            if level == "A":
                divisor = random.randint(1, 9)
                quotient = random.randint(1, 9)

            elif level == "B":
                divisor = random.randint(10, 50)
                quotient = random.randint(1, 10)

            else:
                divisor = random.randint(60, 100)
                quotient = random.randint(1, 10)

            dividend = divisor * quotient

            self.question = f"{dividend} ÷ {divisor} = ?"
            self.correct_answer = quotient

        # ====================================================
        # PERTAMBAHAN
        # ====================================================

        elif operation == "Pertambahan":

            if level == "A":
                a = random.randint(1, 9)
                b = random.randint(1, 9)

            elif level == "B":
                a = random.randint(10, 50)
                b = random.randint(10, 50)

            else:
                a = random.randint(60, 100)
                b = random.randint(60, 100)

            self.question = f"{a} + {b} = ?"
            self.correct_answer = a + b

        # ====================================================
        # PENGURANGAN
        # ====================================================

        elif operation == "Pengurangan":

            if level == "A":
                a = random.randint(1, 9)
                b = random.randint(1, 9)

            elif level == "B":
                a = random.randint(10, 50)
                b = random.randint(10, 50)

            else:
                a = random.randint(60, 100)
                b = random.randint(60, 100)

            # Supaya tidak negatif
            if b > a:
                a, b = b, a

            self.question = f"{a} - {b} = ?"
            self.correct_answer = a - b

        # ====================================================
        # PERPANGKATAN
        # ====================================================

        elif operation == "Perpangkatan":

            power = int(level)

            if power == 2:
                base = random.randint(1, 10)

            else:
                base = random.randint(1, 7)

            self.question = f"{base}^{power} = ?"
            self.correct_answer = base ** power

        # ====================================================
        # AKAR
        # ====================================================

        elif operation == "Akar":

            root_type = int(level)

            if root_type == 2:

                base = random.randint(1, 12)
                number = base ** 2

                self.question = f"√{number} = ?"
                self.correct_answer = base

            else:

                base = random.randint(1, 7)
                number = base ** 3

                self.question = f"∛{number} = ?"
                self.correct_answer = base

    # ========================================================
    # CEK JAWABAN
    # ========================================================

    def submit_answer(self):

        answer_box = self.ids.answer_input
        answer_text = answer_box.text.strip()

        # Kalau kosong
        if not answer_text:

            self.feedback = "Masukkan jawaban terlebih dahulu!"
            self.feedback_color = "warning"

            answer_box.focus = True
            return

        try:
            answer = int(answer_text)

        except ValueError:

            self.feedback = "Masukkan angka yang valid!"
            self.feedback_color = "wrong"

            answer_box.text = ""
            answer_box.focus = True
            return

        # ====================================================
        # JAWABAN BENAR
        # ====================================================

        if answer == self.correct_answer:

            self.score += 10

            self.feedback = "✓ Jawaban benar!"
            self.feedback_color = "correct"

        # ====================================================
        # JAWABAN SALAH
        # ====================================================

        else:

            self.feedback = "✕ Jawaban salah!"
            self.feedback_color = "wrong"

        # Bersihkan input
        answer_box.text = ""

        # ====================================================
        # SELESAI 10 SOAL
        # ====================================================

        if self.question_number >= 10:

            app = App.get_running_app()

            app.final_score = self.score

            # Beri waktu feedback terlihat
            Clock.schedule_once(
                lambda dt: app.show_result(),
                0.5
            )

        # ====================================================
        # LANJUT SOAL
        # ====================================================

        else:

            self.question_number += 1

            # Tunggu sebentar agar feedback sempat terlihat
            Clock.schedule_once(
                self.next_question,
                0.5
            )

    # ========================================================
    # SOAL BERIKUTNYA
    # ========================================================

    def next_question(self, *args):

        self.new_question()

        self.ids.answer_input.text = ""

        # Langsung aktifkan keyboard/input
        Clock.schedule_once(
            self.focus_input,
            0.1
        )


# ============================================================
# RESULT
# ============================================================

class ResultScreen(Screen):

    def update_result(self):

        app = App.get_running_app()

        score = app.final_score

        self.ids.score_label.text = f"{score} / 100"

        if score == 100:

            self.ids.message_label.text = "Sempurna!"

        elif score >= 80:

            self.ids.message_label.text = (
                "Hebat! Tinggal sedikit lagi menuju sempurna."
            )

        elif score >= 60:

            self.ids.message_label.text = (
                "Bagus! Terus latihan."
            )

        else:

            self.ids.message_label.text = (
                "Tidak apa-apa. Coba lagi dan tingkatkan skornya."
            )


# ============================================================
# APP
# ============================================================

class MathPracticeApp(App):

    username = StringProperty("")

    selected_operation = StringProperty("")

    selected_level = StringProperty("")

    final_score = NumericProperty(0)

    # ========================================================
    # BUILD
    # ========================================================

    def build(self):

        sm = ScreenManager()

        sm.add_widget(
            LoginScreen(name="login")
        )

        sm.add_widget(
            HomeScreen(name="home")
        )

        sm.add_widget(
            OperationScreen(name="operation")
        )

        sm.add_widget(
            LevelScreen(name="level")
        )

        sm.add_widget(
            QuizScreen(name="quiz")
        )

        sm.add_widget(
            ResultScreen(name="result")
        )

        return sm

    # ========================================================
    # LOGIN
    # ========================================================

    def login(self, username):

        username = username.strip()

        if not username:
            return

        self.username = username

        self.root.current = "home"

    # ========================================================
    # PILIH OPERASI
    # ========================================================

    def select_operation(self, operation):

        self.selected_operation = operation

        self.root.current = "level"

    # ========================================================
    # PILIH LEVEL
    # ========================================================

    def select_level(self, level):

        self.selected_level = level

        quiz = self.root.get_screen("quiz")

        quiz.start_quiz()

        self.root.current = "quiz"

    # ========================================================
    # HASIL
    # ========================================================

    def show_result(self):

        result = self.root.get_screen("result")

        result.update_result()

        self.root.current = "result"

    # ========================================================
    # COBA LAGI
    # ========================================================

    def retry_quiz(self):

        quiz = self.root.get_screen("quiz")

        quiz.start_quiz()

        self.root.current = "quiz"

    # ========================================================
    # KEMBALI KE HOME
    # ========================================================

    def back_home(self):

        self.root.current = "home"

    # ========================================================
    # GANTI LATIHAN
    # ========================================================

    def leave_quiz(self):

        quiz = self.root.get_screen("quiz")

        # Bersihkan soal yang sedang dikerjakan
        quiz.question = ""
        quiz.question_number = 1
        quiz.score = 0
        quiz.feedback = ""
        quiz.feedback_color = ""

        if "answer_input" in quiz.ids:
            quiz.ids.answer_input.text = ""
            quiz.ids.answer_input.focus = False

        self.root.current = "operation"

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        self.username = ""
        self.selected_operation = ""
        self.selected_level = ""
        self.final_score = 0

        self.root.current = "login"


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    MathPracticeApp().run()