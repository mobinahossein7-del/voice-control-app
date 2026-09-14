# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# Android permissions
try:
    from android.permissions import (
        Permission,
        check_permission,
        request_permissions,
    )
    ANDROID_AVAILABLE = True
except Exception:
    ANDROID_AVAILABLE = False

# PyJNIus
try:
    from jnius import autoclass, PythonJavaClass, java_method
    PYJNIUS_AVAILABLE = True
except Exception:
    PYJNIUS_AVAILABLE = False


class VoiceRecognitionListener(
    PythonJavaClass if PYJNIUS_AVAILABLE else object
):

    if PYJNIUS_AVAILABLE:

        __javainterfaces__ = [
            "android/speech/RecognitionListener"
        ]

        __javacontext__ = "app"

        @java_method("(Landroid/os/Bundle;)V")
        def onReadyForSpeech(self, params):
            if self.app:
                self.app.set_status("🎙️ استمع الآن...")

        @java_method("()V")
        def onBeginningOfSpeech(self):
            if self.app:
                self.app.set_status("🎙️ جارٍ الاستماع...")

        @java_method("([B)V")
        def onBufferReceived(self, buffer):
            pass

        @java_method("(F)V")
        def onRmsChanged(self, rmsdB):
            pass

        @java_method("(Landroid/os/Bundle;)V")
        def onEndOfSpeech(self):
            if self.app:
                self.app.set_status("⏳ جارٍ تحليل الكلام...")

        @java_method("(I)V")
        def onError(self, error):
            if self.app:
                self.app.on_speech_error(error)

        @java_method("(Landroid/os/Bundle;)V")
        def onResults(self, results):
            if self.app:
                self.app.on_speech_results(results)

        @java_method("(Landroid/os/Bundle;)V")
        def onPartialResults(self, results):
            if self.app:
                self.app.on_partial_results(results)

        @java_method("(I[Ljava/lang/String;)V")
        def onEvent(self, eventType, params):
            pass

    def __init__(self, app):
        if PYJNIUS_AVAILABLE:
            super().__init__()

        self.app = app


class VoiceControlApp(App):

    title = "التحكم الصوتي"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.recognizer = None
        self.intent = None
        self.listener = None
        self.listening = False
        self.last_text = ""

    def build(self):

        Window.clearcolor = (
            0.96,
            0.97,
            0.98,
            1
        )

        root = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12)
        )

        # Header
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(92),
            spacing=dp(4)
        )

        title = Label(
            text="التحكم الصوتي",
            font_size=dp(28),
            bold=True,
            color=(0.08, 0.09, 0.12, 1),
            halign="right",
            valign="middle"
        )

        title.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        subtitle = Label(
            text="تحدث بالعربية وسأعرض ما تم التعرف عليه",
            font_size=dp(15),
            color=(0.30, 0.32, 0.36, 1),
            halign="right",
            valign="middle"
        )

        subtitle.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        root.add_widget(header)

        # Status
        self.status = Label(
            text="جاهز للاستماع",
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(48),
            color=(0.10, 0.35, 0.65, 1),
            halign="center",
            valign="middle"
        )

        self.status.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        root.add_widget(self.status)

        # Recognition result
        self.result_label = Label(
            text="لم يتم التعرف على أي كلام بعد.",
            font_size=dp(20),
            color=(0.10, 0.10, 0.12, 1),
            halign="right",
            valign="top"
        )

        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )

        scroll.add_widget(self.result_label)

        root.add_widget(scroll)

        # Microphone button
        self.listen_button = Button(
            text="🎙️  بدء الاستماع",
            font_size=dp(21),
            bold=True,
            size_hint_y=None,
            height=dp(64)
        )

        self.listen_button.bind(
            on_release=self.toggle_listening
        )

        root.add_widget(self.listen_button)

        # Bottom buttons
        buttons = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(52),
            spacing=dp(10)
        )

        clear_button = Button(
            text="مسح",
            font_size=dp(16)
        )

        clear_button.bind(
            on_release=self.clear_result
        )

        help_button = Button(
            text="المساعدة",
            font_size=dp(16)
        )

        help_button.bind(
            on_release=self.show_help
        )

        buttons.add_widget(clear_button)
        buttons.add_widget(help_button)

        root.add_widget(buttons)

        # Information
        self.info = Label(
            text="الميكروفون يحتاج إلى إذن من Android عند أول استخدام.",
            font_size=dp(13),
            color=(0.35, 0.36, 0.40, 1),
            size_hint_y=None,
            height=dp(38),
            halign="center",
            valign="middle"
        )

        self.info.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        root.add_widget(self.info)

        Clock.schedule_once(
            self.initialize_android,
            0.5
        )

        return root

    def set_status(self, text):

        self.status.text = text

    def initialize_android(self, *_args):

        if not ANDROID_AVAILABLE:

            self.info.text = (
                "وضع الاختبار: ميزات Android "
                "الصوتية تعمل داخل APK."
            )

            return

        self.request_microphone_permission()

        if not PYJNIUS_AVAILABLE:

            self.set_status(
                "مكوّن Android الصوتي غير متاح"
            )

            self.info.text = (
                "تحقق من تضمين pyjnius في APK."
            )

            return

        try:

            SpeechRecognizer = autoclass(
                "android.speech.SpeechRecognizer"
            )

            self.recognizer = SpeechRecognizer(
                self._get_activity()
            )

            self.listener = VoiceRecognitionListener(
                self
            )

            self.recognizer.setRecognitionListener(
                self.listener
            )

            self.set_status(
                "جاهز للاستماع"
            )

        except Exception as exc:

            self.recognizer = None

            self.set_status(
                "تعذر تهيئة التعرف الصوتي"
            )

            self.info.text = (
                "تأكد من وجود خدمة التعرف على الكلام "
                "في الجهاز."
            )

            print(
                "SpeechRecognizer initialization error:",
                exc
            )

    def _get_activity(self):

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        return PythonActivity.mActivity

    def request_microphone_permission(self):

        if not ANDROID_AVAILABLE:
            return

        try:

            if not check_permission(
                Permission.RECORD_AUDIO
            ):

                request_permissions(
                    [Permission.RECORD_AUDIO],
                    self.permission_callback
                )

        except Exception as exc:

            print(
                "Permission error:",
                exc
            )

    def permission_callback(
        self,
        permissions,
        grant_results
    ):

        Clock.schedule_once(
            lambda *_:
            self.set_status("جاهز للاستماع"),
            0.2
        )

    def create_intent(self):

        Intent = autoclass(
            "android.content.Intent"
        )

        RecognizerIntent = autoclass(
            "android.speech.RecognizerIntent"
        )

        intent = Intent(
            RecognizerIntent.ACTION_RECOGNIZE_SPEECH
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE,
            "ar"
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE,
            "ar"
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_PARTIAL_RESULTS,
            True
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_MAX_RESULTS,
            5
        )

        return intent

    def toggle_listening(self, *_args):

        if self.listening:

            self.stop_listening()

        else:

            self.start_listening()

    def start_listening(self):

        if (
            not ANDROID_AVAILABLE
            or not PYJNIUS_AVAILABLE
        ):

            self.set_status(
                "هذه الميزة تحتاج إلى APK على Android"
            )

            return

        if self.recognizer is None:

            self.initialize_android()

            if self.recognizer is None:
                return

        try:

            if not check_permission(
                Permission.RECORD_AUDIO
            ):

                self.request_microphone_permission()

                self.set_status(
                    "اسمح بالميكروفون ثم اضغط مرة أخرى"
                )

                return

        except Exception:
            pass

        try:

            self.intent = self.create_intent()

            self.recognizer.startListening(
                self.intent
            )

            self.listening = True

            self.listen_button.text = (
                "⏹️  إيقاف الاستماع"
            )

            self.set_status(
                "🎙️ استمع الآن..."
            )

        except Exception as exc:

            self.listening = False

            self.listen_button.text = (
                "🎙️  بدء الاستماع"
            )

            self.set_status(
                "تعذر بدء الاستماع"
            )

            self.info.text = (
                "تأكد من وجود خدمة التعرف على الكلام "
                "على الهاتف."
            )

            print(
                "startListening error:",
                exc
            )

    def stop_listening(self):

        try:

            if self.recognizer is not None:

                self.recognizer.stopListening()

        except Exception as exc:

            print(
                "stopListening error:",
                exc
            )

        self.listening = False

        self.listen_button.text = (
            "🎙️  بدء الاستماع"
        )

        self.set_status(
            "تم إيقاف الاستماع"
        )

    def extract_text(self, bundle):

        if (
            not PYJNIUS_AVAILABLE
            or bundle is None
        ):

            return ""

        try:

            SpeechRecognizer = autoclass(
                "android.speech.SpeechRecognizer"
            )

            key = (
                SpeechRecognizer.RESULTS_RECOGNITION
            )

            results = bundle.getStringArrayList(
                key
            )

            if (
                results is None
                or results.size() == 0
            ):

                return ""

            return str(
                results.get(0)
            )

        except Exception as exc:

            print(
                "Result extraction error:",
                exc
            )

            return ""

    def on_speech_results(self, bundle):

        text = self.extract_text(
            bundle
        )

        self.listening = False

        self.listen_button.text = (
            "🎙️  بدء الاستماع"
        )

        if text:

            self.last_text = text

            self.result_label.text = text

            self.set_status(
                "✅ تم التعرف على الكلام"
            )

            self.handle_command(text)

        else:

            self.set_status(
                "لم يتم التعرف على الكلام"
            )

    def on_partial_results(self, bundle):

        text = self.extract_text(
            bundle
        )

        if text:

            self.result_label.text = text

            self.set_status(
                "🎙️ جارٍ الاستماع..."
            )

    def on_speech_error(self, error):

        self.listening = False

        self.listen_button.text = (
            "🎙️  بدء الاستماع"
        )

        messages = {

            1: "حدث خطأ في الشبكة",

            2: "لا توجد استجابة من الشبكة",

            3: "تعذر تشغيل الصوت",

            4: "الخدمة غير متاحة",

            5: "حدث خطأ في التطبيق",

            6: "انتهت مهلة الاستماع",

            7: "لم أفهم الكلام",

            8: "خدمة التعرف مشغولة",

            9: "لا تملك صلاحية التعرف الصوتي",

            10: "حدث خطأ في الأذونات"
        }

        self.set_status(
            messages.get(
                int(error),
                "حدث خطأ في التعرف الصوتي"
            )
        )

    def handle_command(self, text):

        normalized = text.strip().lower()

        if (
            "مساعدة" in normalized
            or "الأوامر" in normalized
        ):

            self.show_help()

        elif (
            "مسح" in normalized
            or "امسح" in normalized
        ):

            self.clear_result()

        elif (
            "توقف" in normalized
            or "أوقف الاستماع" in normalized
        ):

            self.stop_listening()

        elif (
            "ابدأ" in normalized
            and "استماع" in normalized
        ):

            Clock.schedule_once(
                lambda *_:
                self.start_listening(),
                0.2
            )

    def clear_result(self, *_args):

        self.last_text = ""

        self.result_label.text = (
            "لم يتم التعرف على أي كلام بعد."
        )

        self.set_status(
            "جاهز للاستماع"
        )

    def show_help(self, *_args):

        self.result_label.text = (
            "الأوامر المتاحة داخل التطبيق:\n\n"
            "• «ابدأ الاستماع»\n"
            "• «أوقف الاستماع»\n"
            "• «امسح»\n"
            "• «مساعدة»\n\n"
            "يمكنك أيضاً التحدث بشكل طبيعي، "
            "وسيظهر النص الذي يتعرف عليه Android هنا."
        )

        self.set_status(
            "المساعدة"
        )

    def on_stop(self):

        try:

            if self.recognizer is not None:

                self.recognizer.destroy()

        except Exception:
            pass

        self.recognizer = None


if __name__ == "__main__":

    VoiceControlApp().run()
