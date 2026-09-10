from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class ProfilScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="[b]TENTANG TKJ-NET[/b]",
            markup=True,
            font_size=28,
            size_hint_y=None,
            height=60
        )

        info = Label(
            text="[b]TKJ-Net[/b]\n\n"
                 "Layanan internet cepat dan stabil\n"
                 "untuk kebutuhan rumah dan bisnis.\n\n"
                 "Dibuat oleh:\n"
                 "Gabriela Jihan Gracia\n"
                 "XI TKJ 2 | Absen 12\n"
                 "SMKN 1 Kediri",
            markup=True,
            font_size=17,
            halign="center"
        )

        kembali = Button(
            text="← Kembali",
            size_hint_y=None,
            height=50
        )

        kembali.bind(
            on_press=self.kembali_home
        )

        layout.add_widget(title)
        layout.add_widget(info)
        layout.add_widget(kembali)

        self.add_widget(layout)

    def kembali_home(self, instance):
        self.manager.current = "home"