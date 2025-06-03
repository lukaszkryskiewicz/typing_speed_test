class Timer:
    def __init__(self, window):
        self.window = window
        self.time_left = 0
        self.timer = None



    def run_timer(self, time, time_label, end_game):
        self.time_left = time
        time_label.config(text=f'Time left: {self.time_left if self.time_left >= 10 else f'0{self.time_left}'}')

        if time > 0:
            self.timer = self.window.after(1000, self.run_timer, time - 1, time_label, end_game)
        else:
            self.window.after_cancel(self.timer)
            self.timer = None
            end_game()
