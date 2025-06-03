import tkinter as tk

import utilities
from timer import Timer


class AppInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Speed typing app')
        self.window.config(padx=20, pady=20)

        self.CPM = 0
        self.time_left = '00'
        self.words_list = []
        self.user_text = ''

        self._create_widgets()
        self.timer = Timer(self.window)
        self.keyboard_listener = self.input.bind('<Key>', self.key_handler)
        self.window.mainloop()

    def _create_widgets(self):
        tk.Label(text='Check how fast you are!', font=('Arial', 32)).grid(column=1, row=0, pady=20)

        self.CPM_label = tk.Label(text=f'Score: {self.CPM} CPM', font=('Arial', 26))
        self.CPM_label.grid(column=0, row=1, pady=20)

        self.time_label = tk.Label(text=f'Time left: {self.time_left}', font=('Arial', 26))
        self.time_label.grid(column=2, row=1, pady=20)

        tk.Button(text='Start', font=('Arial', 26), command=self.start_game).grid(column=1, row=2, pady=20)

        self.pattern = tk.Text(wrap='word', bg='grey', fg='white', padx=20, pady=20, height=4)
        self.pattern.grid(column=0, row=3, columnspan=3, rowspan=3, sticky="ew")
        self.pattern.tag_config('correct_letter', foreground='green')
        self.pattern.tag_config('wrong_letter', foreground='red')
        self.pattern.tag_config('raw', foreground='white')
        self.pattern.tag_config('correct_word', background='blue')
        self.pattern.tag_config('wrong_word', background='yellow')

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
        # get previous character from input
        previous_char = self.input.get("end-2c", "end-1c")

        # check if new character is a letter, space or backspace
        if not (event.char.isalpha() or event.char == " " or event.keysym == 'BackSpace'):
            return 'break'

        # avoid double-spacing
        if event.char == " " and previous_char == " ":
            return 'break'

        #fires _process_text after character is entered in input
        self.input.after_idle(self._process_text, event.keysym, previous_char)

    def _process_text(self, key, previous_char):
        self.user_text = self.input.get("1.0", "end-1c")  # without trailing \n

        utilities.compare_input(self.pattern, self.user_text, key, self.words_list, previous_char, self.update_cpm)

    def update_cpm(self, cpm):
        print(cpm, self.CPM)
        self.CPM = self.CPM + cpm
        self.CPM_label.config(text=f'Score: {self.CPM} CPM')


