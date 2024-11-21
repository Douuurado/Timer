import tkinter as tk
import winsound as ws
from tkinter import messagebox
from tkinter import ttk
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
            
        for _ in range(5):
            self.root.grid_columnconfigure(_, weight=1)
            self.root.grid_rowconfigure(_, weight=1)

        self.normal_tab = tk.Frame(self.notebook)
        self.notebook.add(self.normal_tab, text="Base Timer")
        self.setup_tab(self.normal_tab)

        self.pomodoro_tab = tk.Frame(self.notebook)
        self.notebook.add(self.pomodoro_tab, text="Pomodoro Timer")
        self.setup_tab_pomodoro(self.pomodoro_tab)

    def setup_tab(self, tab):
        self.time_seconds = 0
        self.running = False
        self.conversion = 1
        self.beeped = False

        self.start_time = None
        self.elapsed_time = 0

        self.label = tk.Label(tab, text="00:00:00", font=('Arial', 48))
        self.label.grid(row=0, column=0)
            
        frame = tk.Frame(tab)
        frame.grid(row=1, column=0, sticky="nsew")

        start_button = tk.Button(frame, text="Start", font=('Arial', 14), width=7, command=lambda: self.start_timer())
        start_button.grid(row=1, column=0, padx=10, pady=5)

        pause_button = tk.Button(frame, text="Pause", font=('Arial', 14), width=7, command=lambda: self.pause_timer())
        pause_button.grid(row=1, column=1, padx=10, pady=5)

        restart_button = tk.Button(frame, text="Restart", font=('Arial', 14), width=7, command=lambda: self.restart_timer())
        restart_button.grid(row=1, column=2, padx=10, pady=5)

        timer_entry = tk.Entry(frame, width=14)
        timer_entry.grid(row=3, column=1, sticky="e", ipady=5, ipadx=7)

        timer_button = tk.Button(frame, text="Insert", font=('Arial', 10), width=5, command=lambda: self.define_timer(timer_entry))
        timer_button.grid(row=3, column=2, sticky="w", ipadx=7)

        sec_button = tk.Button(frame, text="Seconds", font=('Arial', 7), width=7, command=lambda: self.set_conversion('sec'))
        sec_button.grid(row=2, column=0, sticky="se")
    
        min_button = tk.Button(frame, text="Minutes", font=('Arial', 7), width=7, command=lambda: self.set_conversion('min'))
        min_button.grid(row=3, column=0, sticky="nse")

        hour_button = tk.Button(frame, text="Hours", font=('Arial', 7), width=7, command=lambda: self.set_conversion('hour'))
        hour_button.grid(row=4, column=0, sticky="ne")

    def set_conversion(self, conversion_type):
        conversions = {"sec": 1, "min": 60, "hour": 3600}
        self.conversion = conversions.get(conversion_type, 1)

    def start_timer(self):
        if not self.running:
            self.running = True
            if self.start_time is None:
                self.start_time = time.time()
            else:
                self.start_time = time.time() - self.elapsed_time
            self.update_timer()

    def update_label(self, total_seconds):
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def update_timer(self):
        if self.running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            remaining_time = max(0, self.time_seconds - int(self.elapsed_time))
            self.update_label(int(remaining_time))

            if remaining_time <= 0:
                self.update_label(0)
                self.beep_sound()
                self.running = False
            else:
                self.root.after(100, self.update_timer)

    def pause_timer(self):
        if self.running:
            self.running = False

    def restart_timer(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = None
        self.update_label(self.time_seconds)

    def beep_sound(self):
        if not self.beeped:
            ws.Beep(448, 1000)
            self.beeped = True

    def define_timer(self, entry):
        try:
            self.time_seconds = int(entry.get()) * self.conversion
            if self.time_seconds < 0:
                raise ValueError
            elif self.time_seconds > 359999:
                self.time_seconds = 359999
            self.update_label(self.time_seconds)
            self.beeped = False

        except ValueError:
            messagebox.showerror("Invalid Timer", "Please enter a valid time (above 1 second)")

    def setup_tab_pomodoro(self, tab_pomodoro):
        self.time_work_pomodoro = 0
        self.time_rest_pomodoro = 0
        self.running_pomodoro = False
        self.beeped_pomodoro = False
        self.work = True
        self.counter = 0

        self.timer_value_pomodoro = None
        self.work_time = 0
        self.rest_time = 0

        self.label_pomodoro = tk.Label(tab_pomodoro, text="00:00:00", font=('Arial', 48))
        self.label_pomodoro.grid(row=0, column=0)

        frame_pomodoro = tk.Frame(tab_pomodoro)
        frame_pomodoro.grid(row=1, column=0, sticky="nsew")

        start_button_pomodoro = tk.Button(frame_pomodoro, text="Start", font=('Arial', 14), width=7, command=lambda: self.start_timer_pomodoro())
        start_button_pomodoro.grid(row=1, column=0, padx=10, pady=5)

        pause_button_pomodoro = tk.Button(frame_pomodoro, text="Pause", font=('Arial', 14), width=7, command=lambda: self.pause_timer_pomodoro())
        pause_button_pomodoro.grid(row=1, column=1, padx=10, pady=5)

        restart_button_pomodoro = tk.Button(frame_pomodoro, text="Restart", font=('Arial', 14), width=7, command=lambda: self.restart_timer_pomodoro())
        restart_button_pomodoro.grid(row=1, column=2, padx=10, pady=5)

        timer_entry_pomodoro = tk.Entry(frame_pomodoro, width=14)
        timer_entry_pomodoro.grid(row=3, column=1, sticky="e", ipady=5, ipadx=7)

        timer_button_pomodoro = tk.Button(frame_pomodoro, text="Insert", font=('Arial', 10), width=5, command=lambda: self.define_timer_pomodoro(timer_entry_pomodoro))
        timer_button_pomodoro.grid(row=3, column=2, sticky="w", ipadx=7)

    def update_label_pomodoro(self, time):

        hours, remainder = divmod(time, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.label_pomodoro.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def start_timer_pomodoro(self):
        if not self.running_pomodoro:
            self.running_pomodoro = True
            self.run_timer_pomodoro()

    def run_timer_pomodoro(self):
        if self.timer_value_pomodoro != None and self.running_pomodoro:
            if self.work:
                self.run_work_pomodoro()
            else:
                self.run_rest_pomodoro()

    def run_work_pomodoro(self):
        if self.time_work_pomodoro > 0:
                    self.time_work_pomodoro -= 1
                    self.update_label_pomodoro(self.time_work_pomodoro)
                    self.root.after(1000, self.run_timer_pomodoro)

        elif self.time_work_pomodoro <= 0:
            self.counter -= 1
            if self.counter == 0:
                self.beep_sound_pomodoro()
                self.restart_timer_pomodoro()
                return

            self.beep_sound_pomodoro()
            self.restart_work_rest_pomodoro()
            self.root.after(1000,  self.run_timer_pomodoro) 

    def run_rest_pomodoro(self):
        if self.time_rest_pomodoro > 0:
                    self.time_rest_pomodoro -= 1
                    self.update_label_pomodoro(self.time_rest_pomodoro)
                    self.root.after(1000,  self.run_timer_pomodoro)
                        
        elif self.time_rest_pomodoro <= 0:
            self.beep_sound_pomodoro()
            self.restart_work_rest_pomodoro()
            self.root.after(1000,  self.run_timer_pomodoro)

    def pause_timer_pomodoro(self):
        self.running_pomodoro = False

    def restart_work_rest_pomodoro(self):
        if self.time_work_pomodoro <= 0:
            self.beeped_pomodoro = False
            self.work = False
            self.time_work_pomodoro = self.work_time
            self.time_rest_pomodoro = self.rest_time
            self.update_label_pomodoro(self.time_rest_pomodoro)

        elif self.time_rest_pomodoro <= 0:
            self.beeped_pomodoro = False
            self.work = True
            self.time_rest_pomodoro = self.rest_time
            self.time_work_pomodoro = self.work_time
            self.update_label_pomodoro(self.time_work_pomodoro)

    def restart_timer_pomodoro(self):
        self.running_pomodoro = False
        self.work = True
        self.time_work_pomodoro = self.work_time
        self.update_label_pomodoro(self.time_work_pomodoro)

    def define_timer_pomodoro(self, entry):
        try:
            self.timer_value_pomodoro = int(entry.get()) * 60
            if self.timer_value_pomodoro < 600:
                raise ValueError    

            if self.timer_value_pomodoro <= 3600:
                self.counter = 2
                self.rest_time = 300
                time_work_holder = (self.timer_value_pomodoro - self.rest_time) / self.counter
                
            else:
                self.counter = 3
                self.rest_time = 600
                time_work_holder = (self.timer_value_pomodoro - self.rest_time * 2) / self.counter
                
            self.time_work_pomodoro = int(time_work_holder)
            self.work_time = self.time_work_pomodoro
            self.update_label_pomodoro(self.time_work_pomodoro)
            self.beeped_pomodoro = False

        except ValueError:
            messagebox.showerror("Invalid Timer", "Please enter a valid time (Above 10 minutes)")

    def beep_sound_pomodoro(self):
        if not self.beeped_pomodoro:
            ws.Beep(438, 1000)
            self.beeped_pomodoro = True

def main():
    if __name__ == "__main__":
        root = tk.Tk()
        app = TimerApp(root)    
        root.mainloop()
main()
