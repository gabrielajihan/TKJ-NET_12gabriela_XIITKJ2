# ============================================================
# WINDOW MOBILE / PORTRAIT
# ============================================================

from kivy.config import Config

Config.set("graphics", "width", "400")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", "0")


# ============================================================
# IMPORT
# ============================================================

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import random


# ============================================================
# LOAD KV
# ============================================================

Builder.load_file("mathpractice.kv")


# ============================================================
# LOGIN SCREEN
# ============================================================

class LoginScreen(Screen):
    pass


# ============================================================
# HOME SCREEN
# ============================================================

class HomeScreen(Screen):
    pass


# ============================================================
# OPERATION SCREEN
# ============================================================

class OperationScreen(Screen):
    pass


# ============================================================
# LEVEL SCREEN
# ============================================================

class LevelScreen(Screen):
    pass


# ============================================================
# QUIZ SCREEN
# ============================================================

class QuizScreen(Screen):

    question = StringProperty("")
    question_number = NumericProperty(1)
    score = NumericProperty(0)
    correct_answer = NumericProperty(0)

    feedback = StringProperty("")
    feedback_color = StringProperty("")

    # ========================================================
    # MENYIMPAN KUMPULAN SOAL
    # ========================================================

    question_pool = []


    # --------------------------------------------------------
    # FOCUS INPUT
    # --------------------------------------------------------

    def focus_input(self, *args):
        self.ids.answer_input.focus = True


    # --------------------------------------------------------
    # START QUIZ
    # --------------------------------------------------------

    def start_quiz(self):

        self.question_number = 1
        self.score = 0
        self.feedback = ""
        self.feedback_color = ""

        # Buat kumpulan soal baru setiap latihan
        self.create_question_pool()

        self.new_question()

        self.ids.answer_input.text = ""

        Clock.schedule_once(
            lambda dt: self.focus_input(),
            0.2
        )


    # ========================================================
    # MEMBUAT KUMPULAN SOAL UNIK
    # ========================================================

    def create_question_pool(self):

        app = App.get_running_app()

        operation = app.selected_operation
        level = app.selected_level

        pool = []


        # ====================================================
        # PERKALIAN
        # ====================================================

        if operation == "Perkalian":

            if level == "A":

                for a in range(1, 10):
                    for b in range(1, 10):
                        pool.append(
                            (f"{a} × {b} = ?", a * b)
                        )

            elif level == "B":

                for a in range(10, 51):
                    for b in range(10, 51):
                        pool.append(
                            (f"{a} × {b} = ?", a * b)
                        )

            else:

                for a in range(60, 101):
                    for b in range(60, 101):
                        pool.append(
                            (f"{a} × {b} = ?", a * b)
                        )


        # ====================================================
        # PEMBAGIAN
        # ====================================================

        elif operation == "Pembagian":

            if level == "A":

                for divisor in range(1, 10):
                    for quotient in range(1, 10):

                        dividend = divisor * quotient

                        pool.append(
                            (
                                f"{dividend} ÷ {divisor} = ?",
                                quotient
                            )
                        )

            elif level == "B":

                for divisor in range(10, 51):
                    for quotient in range(1, 11):

                        dividend = divisor * quotient

                        pool.append(
                            (
                                f"{dividend} ÷ {divisor} = ?",
                                quotient
                            )
                        )

            else:

                for divisor in range(60, 101):
                    for quotient in range(1, 11):

                        dividend = divisor * quotient

                        pool.append(
                            (
                                f"{dividend} ÷ {divisor} = ?",
                                quotient
                            )
                        )


        # ====================================================
        # PERTAMBAHAN
        # ====================================================

        elif operation == "Pertambahan":

            if level == "A":

                for a in range(1, 10):
                    for b in range(1, 10):
                        pool.append(
                            (f"{a} + {b} = ?", a + b)
                        )

            elif level == "B":

                for a in range(10, 51):
                    for b in range(10, 51):
                        pool.append(
                            (f"{a} + {b} = ?", a + b)
                        )

            else:

                for a in range(60, 101):
                    for b in range(60, 101):
                        pool.append(
                            (f"{a} + {b} = ?", a + b)
                        )


        # ====================================================
        # PENGURANGAN
        # ====================================================

        elif operation == "Pengurangan":

            if level == "A":

                for a in range(1, 10):
                    for b in range(1, 10):

                        if b > a:
                            continue

                        pool.append(
                            (f"{a} − {b} = ?", a - b)
                        )

            elif level == "B":

                for a in range(10, 51):
                    for b in range(10, 51):

                        if b > a:
                            continue

                        pool.append(
                            (f"{a} − {b} = ?", a - b)
                        )

            else:

                for a in range(60, 101):
                    for b in range(60, 101):

                        if b > a:
                            continue

                        pool.append(
                            (f"{a} − {b} = ?", a - b)
                        )


        # ====================================================
        # PERPANGKATAN
        # ====================================================

        elif operation == "Perpangkatan":

            if level == "2":

                for base in range(1, 11):

                    pool.append(
                        (
                            f"{base}² = ?",
                            base ** 2
                        )
                    )

            elif level == "3":

                # 1 sampai 10 supaya tersedia 10 soal unik
                for base in range(1, 11):

                    pool.append(
                        (
                            f"{base}³ = ?",
                            base ** 3
                        )
                    )


        # ====================================================
        # AKAR
        # ====================================================

        elif operation == "Akar":

            if level == "2":

                for base in range(1, 13):

                    number = base ** 2

                    pool.append(
                        (
                            f"√{number} = ?",
                            base
                        )
                    )

            elif level == "3":

                # 1 sampai 10 supaya tersedia 10 soal unik
                for base in range(1, 11):

                    number = base ** 3

                    pool.append(
                        (
                            f"∛{number} = ?",
                            base
                        )
                    )


        # ====================================================
        # ACAK KUMPULAN SOAL
        # ====================================================

        random.shuffle(pool)

        # Ambil minimal 10 soal
        self.question_pool = pool[:10]


    # --------------------------------------------------------
    # NEW QUESTION
    # --------------------------------------------------------

    def new_question(self):

        # Kalau masih ada soal di dalam kumpulan
        if self.question_pool:

            question_data = self.question_pool.pop(0)

            self.question = question_data[0]
            self.correct_answer = question_data[1]

        else:

            # Pengaman jika pool kosong
            self.create_question_pool()

            question_data = self.question_pool.pop(0)

            self.question = question_data[0]
            self.correct_answer = question_data[1]


    # --------------------------------------------------------
    # SUBMIT ANSWER
    # --------------------------------------------------------

    def submit_answer(self):

        answer_text = self.ids.answer_input.text.strip()


        # Jika kosong
        if not answer_text:

            self.feedback = "Isi jawaban terlebih dahulu!"
            self.feedback_color = "wrong"

            return


        try:

            user_answer = int(answer_text)

        except ValueError:

            self.feedback = "Masukkan angka!"
            self.feedback_color = "wrong"

            return


        # ====================================================
        # CEK JAWABAN
        # ====================================================

        if user_answer == self.correct_answer:

            self.feedback = "✓ Jawaban benar!"
            self.feedback_color = "correct"

            self.score += 10

        else:

            self.feedback = (
                f"✗ Salah. Jawaban yang benar: "
                f"{self.correct_answer}"
            )

            self.feedback_color = "wrong"


        # Bersihkan input
        self.ids.answer_input.text = ""


        # ====================================================
        # SELESAI 10 SOAL
        # ====================================================

        if self.question_number >= 10:

            app = App.get_running_app()

            app.final_score = self.score

            Clock.schedule_once(
                lambda dt: app.show_result(),
                0.8
            )

        else:

            self.question_number += 1

            Clock.schedule_once(
                lambda dt: self.next_question(),
                0.8
            )


    # --------------------------------------------------------
    # NEXT QUESTION
    # --------------------------------------------------------

    def next_question(self):

        self.new_question()

        self.ids.answer_input.text = ""

        Clock.schedule_once(
            lambda dt: self.focus_input(),
            0.2
        )


# ============================================================
# RESULT SCREEN
# ============================================================

class ResultScreen(Screen):

    def update_result(self):

        app = App.get_running_app()

        score = app.final_score

        # Tampilkan skor lengkap
        self.ids.score_label.text = str(score)


        if score == 100:

            self.ids.message_label.text = "Sempurna!"

        elif score >= 80:

            self.ids.message_label.text = (
                "Hebat! Tinggal sedikit lagi "
                "menuju sempurna."
            )

        elif score >= 60:

            self.ids.message_label.text = (
                "Kerja bagus! Terus latihan."
            )

        else:

            self.ids.message_label.text = (
                "Tidak apa-apa. Coba lagi "
                "dan tingkatkan skornya."
            )


# ============================================================
# MAIN APP
# ============================================================

class MathPracticeApp(App):

    username = StringProperty("")

    selected_operation = StringProperty("")

    selected_level = StringProperty("")

    final_score = NumericProperty(0)


    # --------------------------------------------------------
    # BUILD
    # --------------------------------------------------------

    def build(self):

        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))

        sm.add_widget(HomeScreen(name="home"))

        sm.add_widget(OperationScreen(name="operation"))

        sm.add_widget(LevelScreen(name="level"))

        sm.add_widget(QuizScreen(name="quiz"))

        sm.add_widget(ResultScreen(name="result"))

        return sm


    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    def login(self, username):

        username = username.strip()

        if not username:

            return

        self.username = username

        self.root.current = "home"


    # --------------------------------------------------------
    # SELECT OPERATION
    # --------------------------------------------------------

    def select_operation(self, operation):

        self.selected_operation = operation

        self.root.current = "level"


    # --------------------------------------------------------
    # SELECT LEVEL
    # --------------------------------------------------------

    def select_level(self, level):

        self.selected_level = level

        quiz_screen = self.root.get_screen("quiz")

        quiz_screen.start_quiz()

        self.root.current = "quiz"


    # --------------------------------------------------------
    # SHOW RESULT
    # --------------------------------------------------------

    def show_result(self):

        result_screen = self.root.get_screen("result")

        result_screen.update_result()

        self.root.current = "result"


    # --------------------------------------------------------
    # RETRY QUIZ
    # --------------------------------------------------------

    def retry_quiz(self):

        quiz_screen = self.root.get_screen("quiz")

        quiz_screen.start_quiz()

        self.root.current = "quiz"


    # --------------------------------------------------------
    # BACK HOME
    # --------------------------------------------------------

    def back_home(self):

        self.root.current = "home"


    # --------------------------------------------------------
    # LEAVE QUIZ
    # --------------------------------------------------------

    def leave_quiz(self):

        quiz_screen = self.root.get_screen("quiz")

        quiz_screen.question = ""

        quiz_screen.question_number = 1

        quiz_screen.score = 0

        quiz_screen.feedback = ""

        quiz_screen.question_pool = []

        quiz_screen.ids.answer_input.text = ""

        quiz_screen.ids.answer_input.focus = False

        self.root.current = "operation"


    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

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