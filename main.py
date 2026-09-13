from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class VoiceControlApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=50,
            spacing=20
        )

        self.label = Label(
            text="التحكم الصوتي بالإعدادات\nاضغط للتحدث",
            font_size=20
        )

        layout.add_widget(self.label)

        btn = Button(
            text="بدء الاستماع",
            font_size=22
        )

        layout.add_widget(btn)

        return layout


if __name__ == "__main__":
    VoiceControlApp().run()
