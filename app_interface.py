import tkinter as tk

import utilities
from timer import Timer


class AppInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Speed typing app')
        self.window.config(padx=20, pady=20)

        self.score = 0
        self.time_left = '00'
        self.words_list = []
        self.user_text = ''

        self._create_widgets()
        self.timer = Timer(self.window)
        self.keyboard_listener = self.input.bind('<Key>', self.key_handler)
        self.window.mainloop()

    def _create_widgets(self):
        tk.Label(text='Check how fast you are!', font=('Arial', 32)).grid(column=1, row=0, pady=20)

        tk.Label(text=f'Score: {self.score}', font=('Arial', 26)).grid(column=0, row=1, pady=20)

        self.time_label = tk.Label(text=f'Time left: {self.time_left}', font=('Arial', 26))
        self.time_label.grid(column=2, row=1, pady=20)

        tk.Button(text='Start', font=('Arial', 26), command=self.start_game).grid(column=1, row=2, pady=20)

        self.pattern = tk.Text(wrap='word', bg='grey', fg='white', padx=20, pady=20, height=4)
        self.pattern.grid(column=0, row=3, columnspan=3, rowspan=3, sticky="ew")
        self.pattern.tag_config('correct', foreground='green')
        self.pattern.tag_config('wrong', foreground='red')
        self.pattern.tag_config('raw', foreground='white')

        self.input = tk.Text(height=4, padx=20, pady=20, spacing1=1)
        self.input.grid(column=0, row=6, columnspan=3, sticky="ew")



    def start_game(self):
        if not self.timer.timer:
            self._create_words_list()
            self.start_timer()

    def _create_words_list(self):
        self.words_list = utilities.generate_words()
        self.pattern.insert(1.0, self.words_list)
        self.pattern.config(state='disabled')

    def start_timer(self):
        self.timer.run_timer(10, self.time_label)
        self.time_left = self.timer.time_left

    def key_handler(self, event):
        if not event.char.isalpha() and event.char == " " and event.keysym == 'BackSpace':
            return 'break'
        #fires _process_text after character is entered in input
        self.input.after_idle(self._process_text, event.keysym)

    def _process_text(self, key):
        self.user_text = self.input.get("1.0", "end-1c")  # bez końcowego \n
        utilities.compare_input(self.pattern, self.user_text, key, self.words_list)


