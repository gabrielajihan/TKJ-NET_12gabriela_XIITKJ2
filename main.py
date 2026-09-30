# ============================================================
# WINDOW CONFIGURATION
# ============================================================

from kivy.config import Config

Config.set("graphics", "width", "420")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", "1")


# ============================================================
# IMPORT
# ============================================================

import math
import os
import random
import sqlite3
import struct
import wave
from datetime import datetime
from io import BytesIO

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


# ============================================================
# DATABASE UTILITIES
# ============================================================

def init_db():
    """Inisialisasi tabel SQLite untuk menyimpan riwayat latihan."""
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            operation TEXT NOT NULL,
            level TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def save_score(username, score, operation, level):
    """Menyimpan hasil kuis ke database."""
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO quiz_history (username, score, operation, level, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            username,
            score,
            operation,
            level,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    conn.close()


def get_history():
    """Mengambil riwayat latihan dari database."""
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, score, operation, level "
        "FROM quiz_history ORDER BY id DESC LIMIT 50"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_score(history_id):
    """Menghapus satu hasil latihan berdasarkan id database."""
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quiz_history WHERE id = ?", (history_id,))
    conn.commit()
    conn.close()


# ============================================================
# SOUND & PARTICLE UTILITIES
# ============================================================


def play_victory_sound():
    """Menghasilkan audio ceria (arpeggio C-major) menggunakan sintesis gelombang WAV."""
    try:
        sample_rate = 22050
        duration_per_note = 0.12
        notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6

        raw_bytes = bytearray()
        for freq in notes:
            num_samples = int(sample_rate * duration_per_note)
            for i in range(num_samples):
                t = float(i) / sample_rate
                envelope = max(0.0, 1.0 - (i / num_samples))
                val = int(16000 * envelope * math.sin(2 * math.pi * freq * t))
                raw_bytes.extend(struct.pack("<h", val))

        buf = BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(raw_bytes)

        sound = SoundLoader.load_mem("victory.wav", buf.getvalue())
        if sound:
            sound.volume = 0.8
            sound.play()
    except Exception as e:
        print(f"Sintesis suara dilewati: {e}")


class CelebrationParticles(Widget):
    """Widget animasi partikel ceria/confetti yang menyebar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        colors = [
            (1, 0.3, 0.4, 1),  # Merah Muda
            (0.3, 0.8, 0.4, 1),  # Hijau
            (0.3, 0.6, 1, 1),  # Biru
            (1, 0.8, 0.2, 1),  # Kuning
            (0.8, 0.4, 0.9, 1),  # Ungu
        ]

        center_x = self.center_x if self.center_x != 0 else 210
        center_y = self.center_y if self.center_y != 0 else 400

        with self.canvas:
            for _ in range(40):
                color = random.choice(colors)
                Color(*color)
                size = random.randint(8, 16)
                p = Ellipse(pos=(center_x, center_y), size=(size, size))
                vx = random.uniform(-6, 6)
                vy = random.uniform(4, 14)
                self.particles.append(
                    {
                        "graphic": p,
                        "x": center_x,
                        "y": center_y,
                        "vx": vx,
                        "vy": vy,
                    }
                )

        Clock.schedule_interval(self.update_particles, 1 / 60.0)

    def update_particles(self, dt):
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] -= 0.25  # Gravitasi
            p["graphic"].pos = (p["x"], p["y"])


# ============================================================
# LOAD KV
# ============================================================

Builder.load_file("mathpractice.kv")


# ============================================================
# SCREENS
# ============================================================


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class OperationScreen(Screen):
    pass


class LevelScreen(Screen):
    pass


class HistoryRow(GridLayout):
    def __init__(self, history_id, on_long_press, **kwargs):
        super().__init__(**kwargs)
        self.history_id = history_id
        self.on_long_press_callback = on_long_press
        self._long_press_event = None
        self._long_press_triggered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._long_press_triggered = False
            self._long_press_event = Clock.schedule_once(
                self._handle_long_press, 0.7
            )
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._long_press_event is not None:
            self._long_press_event.cancel()
            self._long_press_event = None
        return super().on_touch_up(touch)

    def _handle_long_press(self, _dt):
        self._long_press_event = None
        self._long_press_triggered = True
        self.on_long_press_callback(self.history_id)


class HistoryScreen(Screen):

    def populate_history(self):
        container = self.ids.history_container
        container.clear_widgets()
        records = get_history()

        if not records:
            lbl = Label(
                text="Belum ada riwayat latihan.",
                font_size="14sp",
                color=(0.5, 0.5, 0.6, 1),
                size_hint_y=None,
                height=40,
            )
            container.add_widget(lbl)
            return

        for history_id, name, score, op, lvl in records:
            row = HistoryRow(
                history_id=history_id,
                on_long_press=self.show_delete_popup,
                cols=3,
                spacing=8,
                size_hint_y=None,
                height=30,
            )
            for value, alignment in (
                (name, "left"),
                (str(score), "center"),
                (op.lower(), "right"),
            ):
                lbl = Label(
                    text=value,
                    font_size="14sp",
                    bold=True,
                    color=(0.2, 0.2, 0.3, 1),
                    halign=alignment,
                    valign="middle",
                )
                lbl.bind(size=lbl.setter("text_size"))
                row.add_widget(lbl)
            container.add_widget(row)

    def show_delete_popup(self, history_id):
        content = BoxLayout(orientation="vertical", spacing=10, padding=12)
        content.add_widget(Label(text="Hapus riwayat latihan ini?"))

        actions = BoxLayout(spacing=10, size_hint_y=None, height=44)
        popup = Popup(
            title="Hapus Riwayat",
            content=content,
            size_hint=(None, None),
            size=(320, 180),
            auto_dismiss=False,
        )

        cancel_button = Button(text="Batal")
        cancel_button.bind(on_release=popup.dismiss)
        delete_button = Button(text="Hapus", background_color=(0.85, 0.25, 0.25, 1))
        delete_button.bind(
            on_release=lambda *_: self.delete_history_record(history_id, popup)
        )
        actions.add_widget(cancel_button)
        actions.add_widget(delete_button)
        content.add_widget(actions)
        popup.open()

    def delete_history_record(self, history_id, popup):
        delete_score(history_id)
        popup.dismiss()
        self.populate_history()


# ============================================================
# QUIZ SCREEN
# ============================================================


class QuizScreen(Screen):

    question = StringProperty("")
    question_number = NumericProperty(1)
    score = NumericProperty(0)
    correct_answer = NumericProperty(0)

    feedback = StringProperty("")
    feedback_color = StringProperty("neutral")

    question_pool = []

    def focus_input(self, *args):
        if "answer_input" in self.ids:
            self.ids.answer_input.focus = True

    def start_quiz(self):
        self.question_number = 1
        self.score = 0
        self.feedback = ""
        self.feedback_color = "neutral"

        self.create_question_pool()
        self.new_question()

        if "answer_input" in self.ids:
            self.ids.answer_input.text = ""

        Clock.schedule_once(lambda dt: self.focus_input(), 0.2)

    def create_question_pool(self):
        app = App.get_running_app()
        operation = app.selected_operation
        level = app.selected_level
        pool = []

        if operation == "Perkalian":
            if level == "A":
                for a in range(1, 10):
                    for b in range(1, 10):
                        pool.append((f"{a} × {b} = ?", a * b))
            elif level == "B":
                for a in range(10, 51):
                    for b in range(10, 51):
                        pool.append((f"{a} × {b} = ?", a * b))
            else:
                for a in range(60, 101):
                    for b in range(60, 101):
                        pool.append((f"{a} × {b} = ?", a * b))

        elif operation == "Pembagian":
            if level == "A":
                for divisor in range(1, 10):
                    for quotient in range(1, 10):
                        dividend = divisor * quotient
                        pool.append((f"{dividend} ÷ {divisor} = ?", quotient))
            elif level == "B":
                for divisor in range(10, 51):
                    for quotient in range(1, 11):
                        dividend = divisor * quotient
                        pool.append((f"{dividend} ÷ {divisor} = ?", quotient))
            else:
                for divisor in range(60, 101):
                    for quotient in range(1, 11):
                        dividend = divisor * quotient
                        pool.append((f"{dividend} ÷ {divisor} = ?", quotient))

        elif operation == "Pertambahan":
            if level == "A":
                for a in range(1, 10):
                    for b in range(1, 10):
                        pool.append((f"{a} + {b} = ?", a + b))
            elif level == "B":
                for a in range(10, 51):
                    for b in range(10, 51):
                        pool.append((f"{a} + {b} = ?", a + b))
            else:
                for a in range(60, 101):
                    for b in range(60, 101):
                        pool.append((f"{a} + {b} = ?", a + b))

        elif operation == "Pengurangan":
            if level == "A":
                for a in range(1, 10):
                    for b in range(1, 10):
                        if b <= a:
                            pool.append((f"{a} − {b} = ?", a - b))
            elif level == "B":
                for a in range(10, 51):
                    for b in range(10, 51):
                        if b <= a:
                            pool.append((f"{a} − {b} = ?", a - b))
            else:
                for a in range(60, 101):
                    for b in range(60, 101):
                        if b <= a:
                            pool.append((f"{a} − {b} = ?", a - b))

        elif operation == "Perpangkatan":
            if level == "2":
                for base in range(1, 11):
                    pool.append((f"{base}² = ?", base**2))
            elif level == "3":
                for base in range(1, 11):
                    pool.append((f"{base}³ = ?", base**3))

        elif operation == "Akar":
            if level == "2":
                for base in range(1, 13):
                    pool.append((f"√{base ** 2} = ?", base))
            elif level == "3":
                # Karakter unicode \u221b dijamin mendukung simbol ∛
                cube_root_sym = "\u221b"
                for base in range(1, 11):
                    pool.append((f"{cube_root_sym}{base ** 3} = ?", base))

        random.shuffle(pool)
        self.question_pool = pool[:10]

    def new_question(self):
        if not self.question_pool:
            self.create_question_pool()

        question_data = self.question_pool.pop(0)
        self.question = question_data[0]
        self.correct_answer = question_data[1]

    def submit_answer(self):
        answer_text = self.ids.answer_input.text.strip()

        if not answer_text:
            self.feedback = "Isi jawaban dulu ya!"
            self.feedback_color = "wrong"
            return

        try:
            user_answer = int(answer_text)
        except ValueError:
            self.feedback = "Masukkan angka saja!"
            self.feedback_color = "wrong"
            return

        if user_answer == self.correct_answer:
            self.feedback = "Wah, Jawabanmu Benar!"
            self.feedback_color = "correct"
            self.score += 10
        else:
            self.feedback = f"Kurang tepat. Harusnya: {self.correct_answer}"
            self.feedback_color = "wrong"

        self.ids.answer_input.text = ""

        if self.question_number >= 10:
            app = App.get_running_app()
            app.final_score = self.score
            # Simpan hasil kuis ke database SQLite
            save_score(
                app.username, self.score, app.selected_operation, app.selected_level
            )
            Clock.schedule_once(lambda dt: app.show_result(), 0.8)
        else:
            self.question_number += 1
            Clock.schedule_once(lambda dt: self.next_question(), 0.8)

    def next_question(self):
        self.feedback = ""
        self.feedback_color = "neutral"
        self.new_question()
        self.ids.answer_input.text = ""
        Clock.schedule_once(lambda dt: self.focus_input(), 0.2)


# ============================================================
# RESULT SCREEN
# ============================================================


class ResultScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles_widget = None

    def update_result(self):
        app = App.get_running_app()
        score = app.final_score

        if self.particles_widget and self.particles_widget in self.children:
            self.remove_widget(self.particles_widget)
            self.particles_widget = None

        self.ids.score_label.text = f"{score}"

        if score == 100:
            self.ids.message_label.text = "SEMPURNA! Kamu Genius Matematika!"
        elif score >= 80:
            self.ids.message_label.text = (
                "HEBAT! Sedikit lagi dapat nilai sempurna!"
            )
        elif score >= 60:
            self.ids.message_label.text = "KERJA BAGUS! Terus berlatih ya!"
        else:
            self.ids.message_label.text = "JANGAN MENYERAH! Coba lagi yuk!"

        if score >= 80:
            play_victory_sound()
            self.particles_widget = CelebrationParticles()
            self.add_widget(self.particles_widget)


# ============================================================
# MAIN APP
# ============================================================


class MathPracticeApp(App):

    username = StringProperty("")
    selected_operation = StringProperty("")
    selected_level = StringProperty("")
    final_score = NumericProperty(0)
    symbol_font = StringProperty("Roboto")

    def select_symbol_font(self):
        """Pilih font Windows yang memiliki glyph simbol matematika."""
        windows_symbol_font = os.path.join(
            os.environ.get("WINDIR", r"C:\\Windows"),
            "Fonts",
            "seguisym.ttf",
        )
        if os.path.exists(windows_symbol_font):
            self.symbol_font = windows_symbol_font

    def build(self):
        self.select_symbol_font()
        init_db()  # Inisialisasi Database SQLite
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(OperationScreen(name="operation"))
        sm.add_widget(LevelScreen(name="level"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(ResultScreen(name="result"))
        sm.add_widget(HistoryScreen(name="history"))
        return sm

    def login(self, username):
        username = username.strip()
        if not username:
            return
        self.username = username
        self.root.current = "home"

    def select_operation(self, operation):
        self.selected_operation = operation
        self.root.current = "level"

    def select_level(self, level):
        self.selected_level = level
        quiz_screen = self.root.get_screen("quiz")
        quiz_screen.start_quiz()
        self.root.current = "quiz"

    def show_result(self):
        result_screen = self.root.get_screen("result")
        result_screen.update_result()
        self.root.current = "result"

    def show_history(self):
        history_screen = self.root.get_screen("history")
        history_screen.populate_history()
        self.root.current = "history"

    def retry_quiz(self):
        quiz_screen = self.root.get_screen("quiz")
        quiz_screen.start_quiz()
        self.root.current = "quiz"

    def back_home(self):
        # Langsung kembali ke menu pilihan operasi
        self.root.current = "operation"

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

    def logout(self):
        self.username = ""
        self.selected_operation = ""
        self.selected_level = ""
        self.final_score = 0
        self.root.current = "login"


if __name__ == "__main__":
    MathPracticeApp().run()