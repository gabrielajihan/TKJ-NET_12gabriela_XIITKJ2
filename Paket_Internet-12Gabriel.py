from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# =========================================================
# HALAMAN HOME
# =========================================================

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="TKJ-Net",
            font_size=32
        )

        subtitle = Label(
            text="Internet Cepat & Stabil"
        )

        paket_button = Button(
            text="Paket Internet"
        )
        paket_button.bind(
            on_press=self.buka_paket
        )

        pesan_button = Button(
            text="Pesan WiFi"
        )
        pesan_button.bind(
            on_press=self.buka_pesan
        )

        profil_button = Button(
            text="Profil"
        )
        profil_button.bind(
            on_press=self.buka_profil
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(paket_button)
        layout.add_widget(pesan_button)
        layout.add_widget(profil_button)

        self.add_widget(layout)

    def buka_paket(self, instance):
        self.manager.current = "paket"

    def buka_pesan(self, instance):
        self.manager.current = "pesan"

    def buka_profil(self, instance):
        self.manager.current = "profil"


# =========================================================
# HALAMAN PAKET
# =========================================================

class PaketScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=15
        )

        title = Label(
            text="Paket Internet",
            font_size=28
        )

        bronze = Label(
            text="Bronze\n10 Mbps - Rp200.000 / bulan"
        )

        silver = Label(
            text="Silver\n20 Mbps - Rp350.000 / bulan"
        )

        gold = Label(
            text="Gold\n50 Mbps - Rp500.000 / bulan"
        )

        pesan_button = Button(
            text="Pesan Sekarang"
        )
        pesan_button.bind(
            on_press=self.buka_pesan
        )

        kembali = Button(
            text="Kembali"
        )
        kembali.bind(
            on_press=self.kembali_home
        )

        layout.add_widget(title)
        layout.add_widget(bronze)
        layout.add_widget(silver)
        layout.add_widget(gold)
        layout.add_widget(pesan_button)
        layout.add_widget(kembali)

        self.add_widget(layout)

    def buka_pesan(self, instance):
        self.manager.current = "pesan"

    def kembali_home(self, instance):
        self.manager.current = "home"


# =========================================================
# HALAMAN PESAN WIFI
# =========================================================

class PesanScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=12
        )

        title = Label(
            text="Pesan WiFi",
            font_size=28
        )

        # Input nama
        nama_label = Label(
            text="Nama Pelanggan"
        )

        self.nama_input = TextInput(
            hint_text="Masukkan nama",
            multiline=False
        )

        # Pilihan paket
        paket_label = Label(
            text="Pilih Paket"
        )

        self.paket_spinner = Spinner(
            text="Bronze",
            values=("Bronze", "Silver", "Gold"),
            size_hint_y=None,
            height=50
        )

        # Pilihan durasi
        durasi_label = Label(
            text="Durasi Berlangganan"
        )

        self.durasi_spinner = Spinner(
            text="1 Bulan",
            values=("1 Bulan", "3 Bulan", "6 Bulan", "12 Bulan"),
            size_hint_y=None,
            height=50
        )

        # Tombol hitung
        hitung = Button(
            text="Hitung Total Harga"
        )
        hitung.bind(
            on_press=self.hitung_total
        )

        # Label hasil
        self.hasil = Label(
            text="Total: Rp0"
        )

        # Tombol pesan
        pesan = Button(
            text="Konfirmasi Pesanan"
        )
        pesan.bind(
            on_press=self.konfirmasi_pesanan
        )

        # Tombol kembali
        kembali = Button(
            text="Kembali"
        )
        kembali.bind(
            on_press=self.kembali_home
        )

        # Masukkan semua widget
        layout.add_widget(title)

        layout.add_widget(nama_label)
        layout.add_widget(self.nama_input)

        layout.add_widget(paket_label)
        layout.add_widget(self.paket_spinner)

        layout.add_widget(durasi_label)
        layout.add_widget(self.durasi_spinner)

        layout.add_widget(hitung)
        layout.add_widget(self.hasil)
        layout.add_widget(pesan)
        layout.add_widget(kembali)

        self.add_widget(layout)

    # =====================================================
    # EVENT: HITUNG TOTAL
    # =====================================================

    def hitung_total(self, instance):

        harga_paket = {
            "Bronze": 200000,
            "Silver": 350000,
            "Gold": 500000
        }

        harga = harga_paket[self.paket_spinner.text]

        durasi = {
            "1 Bulan": 1,
            "3 Bulan": 3,
            "6 Bulan": 6,
            "12 Bulan": 12
        }

        jumlah_bulan = durasi[self.durasi_spinner.text]

        total = harga * jumlah_bulan

        self.hasil.text = (
            f"Paket: {self.paket_spinner.text}\n"
            f"Durasi: {jumlah_bulan} bulan\n"
            f"Total: Rp{total:,}".replace(",", ".")
        )

    # =====================================================
    # EVENT: KONFIRMASI PESANAN
    # =====================================================

    def konfirmasi_pesanan(self, instance):

        nama = self.nama_input.text

        if nama == "":
            self.hasil.text = "Silakan masukkan nama pelanggan!"
            return

        harga_paket = {
            "Bronze": 200000,
            "Silver": 350000,
            "Gold": 500000
        }

        durasi = {
            "1 Bulan": 1,
            "3 Bulan": 3,
            "6 Bulan": 6,
            "12 Bulan": 12
        }

        paket = self.paket_spinner.text
        jumlah_bulan = durasi[self.durasi_spinner.text]

        total = harga_paket[paket] * jumlah_bulan

        self.hasil.text = (
            f"Pesanan berhasil!\n"
            f"Nama: {nama}\n"
            f"Paket: {paket}\n"
            f"Durasi: {jumlah_bulan} bulan\n"
            f"Total: Rp{total:,}".replace(",", ".")
        )

    def kembali_home(self, instance):
        self.manager.current = "home"


# =========================================================
# HALAMAN PROFIL
# =========================================================

class ProfilScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=15
        )

        title = Label(
            text="Profil",
            font_size=28
        )

        identitas = Label(
            text="Gabriela Jihan Gracia\n"
                 "XI TKJ 2\n"
                 "No. Absen 12\n"
                 "SMKN 1 Kediri"
        )

        kembali = Button(
            text="Kembali"
        )
        kembali.bind(
            on_press=self.kembali_home
        )

        layout.add_widget(title)
        layout.add_widget(identitas)
        layout.add_widget(kembali)

        self.add_widget(layout)

    def kembali_home(self, instance):
        self.manager.current = "home"


# =========================================================
# SCREEN MANAGER
# =========================================================

class TKJNetApp(App):

    def build(self):

        screen_manager = ScreenManager()

        screen_manager.add_widget(
            HomeScreen(name="home")
        )

        screen_manager.add_widget(
            PaketScreen(name="paket")
        )

        screen_manager.add_widget(
            PesanScreen(name="pesan")
        )

        screen_manager.add_widget(
            ProfilScreen(name="profil")
        )

        return screen_manager


# =========================================================
# MENJALANKAN APLIKASI
# =========================================================

if __name__ == "__main__":
    TKJNetApp().run()