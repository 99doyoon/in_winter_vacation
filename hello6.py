import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import threading

class SpeechTranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("음성 인식 및 번역기")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_ui()
        self.running = False
        # `auto_listen` 호출 부분은 삭제합니다.

    def setup_ui(self):
        # 언어 선택 드롭다운 메뉴
        ttk.Label(self.root, text="입력 언어:").grid(column=0, row=0, sticky=tk.W)
        self.input_language = tk.StringVar()
        self.input_language_menu = ttk.Combobox(self.root, textvariable=self.input_language, values=list(LANGUAGES.values()))
        self.input_language_menu.grid(column=1, row=0)
        self.input_language_menu.current(94)  # 기본값으로 한국어 설정

        ttk.Label(self.root, text="번역 언어:").grid(column=0, row=1, sticky=tk.W)
        self.translation_language = tk.StringVar()
        self.translation_language_menu = ttk.Combobox(self.root, textvariable=self.translation_language, values=list(LANGUAGES.values()))
        self.translation_language_menu.grid(column=1, row=1)
        self.translation_language_menu.current(21)  # 기본값으로 영어 설정

        ttk.Label(self.root, text="음성 출력 언어:").grid(column=0, row=2, sticky=tk.W)
        self.speech_language = tk.StringVar()
        self.speech_language_menu = ttk.Combobox(self.root, textvariable=self.speech_language, values=list(LANGUAGES.values()))
        self.speech_language_menu.grid(column=1, row=2)
        self.speech_language_menu.current(21)  # 기본값으로 영어 설정

        # 결과 출력 창
        self.result_frame = ttk.LabelFrame(self.root, text="결과")
        self.result_frame.grid(column=0, row=4, columnspan=2, sticky=tk.W+tk.E)
        self.result_text = tk.Text(self.result_frame, height=10, width=50)
        self.result_text.pack()

        # 시작/중지 버튼 추가
        self.start_stop_button = ttk.Button(self.root, text="시작", command=self.toggle_listen)
        self.start_stop_button.grid(column=0, row=3, sticky=tk.W+tk.E, columnspan=2)

        # 결과 출력 창 설정 코드 유지

    def toggle_listen(self):
        """음성 인식 시작과 중지를 토글합니다."""
        if self.running:
            self.running = False
            self.start_stop_button["text"] = "시작"
            self.update_ui("음성 인식 중지...")
        else:
            self.running = True
            self.start_stop_button["text"] = "중지"
            self.update_ui("음성 인식 시작...")
            threading.Thread(target=self.monitor_microphone).start()

    # 기존의 monitor_microphone, recognize_speech, update_ui 메서드 유지
    def monitor_microphone(self):
        """마이크 상태를 모니터링하고 음성 인식을 제어합니다."""
        while self.running:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.update_ui("듣고 있습니다...")
                audio = self.recognizer.listen(source)
                self.recognize_speech(audio)

    def recognize_speech(self, audio):
        # 언어 코드 찾기
        input_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.input_language.get())]
        translation_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.translation_language.get())]
    def recognize_speech(self, audio):
        try:
            # 음성 인식
            input_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.input_language.get())]
            translation_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.translation_language.get())]
            recognized_text = self.recognizer.recognize_google(audio, language=input_lang_code)
            self.update_ui(f"인식된 문장: {recognized_text}")
            # 번역
            translator = Translator()
            translated = translator.translate(recognized_text, src=input_lang_code, dest=translation_lang_code)
            self.update_ui(f"번역된 문장: {translated.text}")
            # 음성 변환
            speech_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.speech_language.get())]
            tts = gTTS(translated.text, lang=speech_lang_code)
            temp_file = "temp_audio.mp3"
            tts.save(temp_file)
            os.system(f"start {temp_file}")  # Windows에서 mp3 파일 실행
        except Exception as e:
            self.update_ui(f"오류 발생: {e}")

    def update_ui(self, message):
        """UI의 결과 텍스트 박스를 업데이트합니다."""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTranslatorApp(root)
    root.mainloop()
