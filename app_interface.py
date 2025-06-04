import tkinter as tk
from tkinter import messagebox

import utilities
from timer import Timer


class AppInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Speed typing app')
        self.window.config(padx=20, pady=20)

        self.CPM = 000
        self.time_left = '00'
        self.words_list = []
        self.user_text = ''
        self.current_highscore = utilities.get_highscore()

        self._create_widgets()
        self.timer = Timer(self.window)
        self.keyboard_listener = self.input.bind('<Key>', self.key_handler)
        self.window.mainloop()

    def _create_widgets(self):
        tk.Label(text='Check how fast you are!', font=('Arial', 32)).grid(column=1, row=0, pady=20)

        self.CPM_label = tk.Label(text=f'Score: 00{self.CPM} CPM', font=('Arial', 26))
        self.CPM_label.grid(column=0, row=1, pady=20)

        self.time_label = tk.Label(text=f'Time left: {self.time_left}', font=('Arial', 26))
        self.time_label.grid(column=2, row=1, pady=20)

        self.highscore_label = tk.Label(text=f'Highscore: {self.current_highscore} CPM', font=('Arial', 26))
        self.highscore_label.grid(column=1, row=1)

        self.start_stop_button = tk.Button(text='Start', font=('Arial', 26), command=self.start_stop_game)
        self.start_stop_button.status = 'start'
        self.start_stop_button.grid(column=1, row=2, pady=20)

        self.pattern = tk.Text(wrap='word', bg='grey', fg='white', padx=20, pady=20, height=4)
        self.pattern.grid(column=0, row=3, columnspan=3, rowspan=3, sticky="ew")
        self.pattern.tag_config('correct_letter', foreground='green')
        self.pattern.tag_config('wrong_letter', foreground='red')
        self.pattern.tag_config('raw', foreground='white')
        self.pattern.tag_config('correct_word', background='blue')
        self.pattern.tag_config('wrong_word', background='yellow')

        self.input = tk.Text(height=4, padx=20, pady=20, spacing1=1, state='disabled')
        self.input.grid(column=0, row=6, columnspan=3, sticky="ew")


    def start_stop_game(self):
        if not self.timer.timer and self.start_stop_button.status == 'start':
            self._reset_widgets()
            self._create_words_list()
            self.start_timer()
            self.input.focus()
            self.start_stop_button.config(text='Stop')
            self.start_stop_button.status = 'stop'

        elif self.start_stop_button.status == 'stop':
            self.timer.stop_timer(self.end_game)


    def end_game(self):
        message = f'Final score: {self.CPM} CPM, {self.CPM // 5} WPM'
        messagebox.showinfo(title='Game finished!', message=message)
        self.input.config(state='disabled')
        self.start_stop_button.config(text='Start')
        self.start_stop_button.status = 'start'

        if self.CPM > self.current_highscore:
            self.current_highscore = self.CPM
            self.highscore_label.config(text=f'Highscore: {self.current_highscore} CPM')
            utilities.update_highscore(self.current_highscore)

    def _reset_widgets(self):
        self.CPM = 0
        self.CPM_label.config(text=f'Score: 00{self.CPM} CPM')

        self._remove_patterns()
        self.pattern.config(state='normal')
        self.pattern.delete('1.0', 'end')

        self.input.config(state='normal')
        self.input.delete('1.0', 'end')


    def _remove_patterns(self):
        patterns = ['raw', 'correct_letter', 'wrong_letter', 'correct_word', 'wrong_word']
        for pattern in patterns:
            self.pattern.tag_remove(pattern, '1.0', 'end')

    def _create_words_list(self):
        self.words_list = utilities.generate_words()
        self.pattern.insert(1.0, self.words_list)
        self.pattern.config(state='disabled')

    def start_timer(self):
        self.timer.run_timer(10, self.time_label, self.end_game)
        self.time_left = self.timer.time_left

    def key_handler(self, event):
        if self.input['state'] == 'disabled':
            return 'break'

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
        self.CPM = self.CPM + cpm
        if self.CPM < 10:
            result = f'00{self.CPM}'
        elif self.CPM < 100:
            result = f'0{self.CPM}'
        else:
            result = f'{self.CPM}'
        self.CPM_label.config(text=f'Score: {result} CPM')

