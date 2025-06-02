import tkinter as tk

import utilities


class AppInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Speed typing app')
        self.window.config(padx=20, pady=20)

        self.score = 0
        self.time_left = '00:00'
        self.words_list = []
        self.user_text = tk.StringVar()

        self._create_widgets()
        self.window.mainloop()

    def _create_widgets(self):
        tk.Label(text='Check how fast you are!', font=('Arial', 32)).grid(column=1, row=0, pady=20)

        tk.Label(text=f'Score: {self.score}', font=('Arial', 26)).grid(column=0, row=1, pady=20)

        tk.Label(text=f'Time left: {self.time_left}', font=('Arial', 26)).grid(column=2, row=1, pady=20)

        tk.Button(text='Start', font=('Arial', 26), command=self.start_game).grid(column=1, row=2, pady=20)

        self.pattern = tk.Message(text='', bg='grey', fg='white', aspect=500, justify='center', padx=20, pady=20)
        self.pattern.grid(column=0, row=3, columnspan=3, rowspan=3, sticky="ew")

        self.input = tk.Text(height=4, padx=20, pady=20, spacing1=1)
        self.input.grid(column=0, row=6, columnspan=3, sticky="ew")

    def start_game(self):
        pass

