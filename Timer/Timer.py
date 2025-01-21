import winsound as ws
from tkinter import messagebox
import ttkbootstrap as ttk
import time

# Make the timer screen adjusts to it
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.configure(background="#000000")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.normal_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.normal_tab, text="Base Timer")
        self.setup_tab(self.normal_tab)

        self.pomodoro_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pomodoro_tab, text="Pomodoro Timer")
        self.setup_tab_pomodoro(self.pomodoro_tab)

        style = ttk.Style()

        style.configure('TButton', font=('Arial', 14), padding=(10, 10), relief="flat", background="#4169e1", foreground="white", width=7, highlightthickness=0, focuscolor="#27408b")
        style.map('TButton', background=[('active', '#27408b')])
        style.configure('TNotebook', background="#2c2c2c")
        style.configure('TFrame', background="#2c2c2c", weight= 1)
        style.configure('TLabel', background="#2c2c2c", font=('Arial', 55))
        style.configure('TEntry', font=('Arial', 18), padding=13, relief="flat", borderwidth=0, highlightthickness=0)


    def setup_tab(self, tab):
        # Normal setup
        tab.grid_rowconfigure((0, 1, 2, 3, 4), weight=1, minsize=65)
        tab.grid_columnconfigure((0, 1, 2), weight=1, minsize=65)
        self.time_seconds = None
        self.running = False
        self.conversion = 1
        self.beeped = False

        self.start_time = None
        self.elapsed_time = 0

        # Timer display
        self.label = ttk.Label(tab, text="00:00:00")
        self.label.grid(row=0, column=1, sticky="nsew")
            
        # Buttons inputs
        start_button = ttk.Button(tab, text="Start", command=lambda: self.start_timer())
        start_button.grid(row=1, column=1, sticky="nsew", padx=15, pady=5)

        pause_button = ttk.Button(tab, text="Pause", command=lambda: self.pause_timer())
        pause_button.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        restart_button = ttk.Button(tab, text="Restart", command=lambda: self.restart_timer())
        restart_button.grid(row=1, column=2, sticky="nsew", padx=15, pady=5)

        # Entry of the user input number
        timer_entry = ttk.Entry(tab)
        timer_entry.grid(row=2, column=1, sticky="nsew", pady=30)

        timer_button = ttk.Button(tab, text="Insert", command=lambda: self.define_timer(timer_entry))
        timer_button.grid(row=2, column=2, sticky="nsew", padx=(0, 15), pady=30)

        # Buttons for time preference
        sec_button = ttk.Button(tab, text="Second", command=lambda: self.set_conversion('sec'))
        sec_button.grid(row=2, column=0, sticky="nsew", padx=15, pady=(30, 0))
    
        min_button = ttk.Button(tab, text="Minutes", command=lambda: self.set_conversion('min'))
        min_button.grid(row=3, column=0, sticky="nsew", padx=15)

        hour_button = ttk.Button(tab, text="Hours", command=lambda: self.set_conversion('hour'))
        hour_button.grid(row=4, column=0, sticky="nsew", padx=15, pady=(0, 15))

    def set_conversion(self, conversion_type):
        # Converts the keywords to its time definition
        conversions = {"sec": 1, "min": 60, "hour": 3600}
        self.conversion = conversions.get(conversion_type, 1)

    def start_timer(self):
        # Start the time
        if not self.running:
            self.running = True
            if self.start_time is None:
                self.start_time = time.time()
            else:
                self.start_time = time.time() - self.elapsed_time
            self.update_timer()

    def update_label(self, total_seconds):
        # Update the timer countdown
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def update_timer(self):
        # Update the timer countdown per second
        if self.running and self.time_seconds != None:
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
        # Pause the timer
        if self.running:
            self.running = False

    def restart_timer(self):
        # Restart the timer to its defined time
        self.running = False
        self.elapsed_time = 0
        self.start_time = None
        if self.time_seconds is None:
            self.update_label(0)
        else:
            self.update_label(self.time_seconds)

    def beep_sound(self):
        # Beep sound when timer is out
        if not self.beeped:
            ws.Beep(448, 1000)
            self.beeped = True

    def define_timer(self, entry):
        # Set the timer time
        try:
            self.time_seconds = int(entry.get()) * self.conversion
            if self.time_seconds <= 0:
                raise ValueError
            elif self.time_seconds > 359999:
                self.time_seconds = 359999
            self.update_label(self.time_seconds)
            self.beeped = False

        except ValueError:
            messagebox.showerror("Invalid Timer", "Please enter a number higher than 0")

    def setup_tab_pomodoro(self, tab_pomodoro):
        # Pomodoro timer
        tab_pomodoro.grid_rowconfigure((0, 1, 2), weight=1, minsize=65)
        tab_pomodoro.grid_columnconfigure((0, 1, 2), weight=1, minsize=65)
        self.work_pomodoro = 0
        self.rest_pomodoro = 0
        self.running_pomodoro = False
        self.beeped_pomodoro = False
        self.work = True
        self.counter = 0
        self.session = f"Work\n  {self.counter}/{self.counter}"

        self.timer_value_pomodoro = None
        self.work_time = 0
        self.rest_time = 0

        # Timer display
        self.label_pomodoro = ttk.Label(tab_pomodoro, text="00:00:00")
        self.label_pomodoro.grid(row=0, column=1, sticky="nsew")

        # Button inputs
        start_button_pomodoro = ttk.Button(tab_pomodoro, text="Start", command=lambda: self.start_timer_pomodoro())
        start_button_pomodoro.grid(row=1, column=1, sticky="nsew", padx=15, pady=5)

        pause_button_pomodoro = ttk.Button(tab_pomodoro, text="Pause", command=lambda: self.pause_timer_pomodoro())
        pause_button_pomodoro.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        restart_button_pomodoro = ttk.Button(tab_pomodoro, text="Restart", command=lambda: self.restart_timer_pomodoro())
        restart_button_pomodoro.grid(row=1, column=2, sticky="nsew", padx=15, pady=5)

        # Entry of the user input
        timer_entry_pomodoro = ttk.Entry(tab_pomodoro)
        timer_entry_pomodoro.grid(row=2, column=1, sticky="nsew", pady=30)

        timer_button_pomodoro = ttk.Button(tab_pomodoro, text="Insert", command=lambda: self.define_timer_pomodoro(timer_entry_pomodoro))
        timer_button_pomodoro.grid(row=2, column=2, sticky="nsew", padx=(0, 15), pady=30)  

        self.progress_label_pomodoro = ttk.Label(tab_pomodoro, text=f"{self.session}", font=('Arial', 30))
        self.progress_label_pomodoro.grid(row=2, column=0, sticky="nsew", padx=15)

        tab_pomodoro.grid_rowconfigure(3, minsize=65)

        tab_pomodoro.grid_rowconfigure(4, minsize=65)

    def update_session_pomodoro(self):

        if self.work:
            self.session = f"Work\n  {self.counter_hud}/{self.counter_max}"
        else:
            self.session = f"Rest\n  {self.counter_hud-1}/{self.counter_max-1}"
        self.progress_label_pomodoro.config(text=self.session)

    def update_label_pomodoro(self, time):
        # Update the timer time
        hours, remainder = divmod(time, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.label_pomodoro.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def start_timer_pomodoro(self):
        # Start the timer
        if not self.running_pomodoro:
            self.running_pomodoro = True

        if self.timer_value_pomodoro != None and self.running_pomodoro:
            if self.work:
                self.run_work_pomodoro()
            else:
                self.run_rest_pomodoro()
        
    def run_work_pomodoro(self):
        # Starts the work timer
        if self.running_pomodoro:
            if self.work_pomodoro > 0:
                        self.work_pomodoro -= 1
                        self.update_label_pomodoro(self.work_pomodoro)
                        self.root.after(1000, self.run_work_pomodoro)
            # Alternates to rest
            else:
                self.counter -= 1
                # Resets the timer if all the cycles were finished
                if self.counter == 0:
                    self.beep_sound_pomodoro()
                    self.restart_timer_pomodoro()
                    self.update_session_pomodoro()

                    return
                self.alternate_pomodoro_session()

    def run_rest_pomodoro(self):
        # Starts the rest timer
        if self.running_pomodoro:
            if self.rest_pomodoro > 0:
                        self.rest_pomodoro -= 1
                        self.update_label_pomodoro(self.rest_pomodoro)
                        self.root.after(1000,  self.run_rest_pomodoro)

            # Alternate to work
            else:
                self.alternate_pomodoro_session()


    def pause_timer_pomodoro(self):
        # Pause the timer
        self.running_pomodoro = False

    def alternate_pomodoro_session(self):
        # Alternates between work time and rest
        # Alternates to rest
        if self.work_pomodoro <= 0:
            self.beep_sound_pomodoro()
            self.beeped_pomodoro = False
            self.work = False
            self.work_pomodoro = self.work_time
            self.rest_pomodoro = self.rest_time
            self.counter_hud += 1
            self.update_session_pomodoro()
            self.update_label_pomodoro(self.rest_pomodoro)
            self.root.after(1000,  self.run_rest_pomodoro) 


        # Alternates to work
        elif self.rest_pomodoro <= 0:
            self.beep_sound_pomodoro()
            self.beeped_pomodoro = False
            self.work = True
            self.rest_pomodoro = self.rest_time
            self.work_pomodoro = self.work_time
            self.update_label_pomodoro(self.work_pomodoro)
            self.update_session_pomodoro()
            self.root.after(1000,  self.run_work_pomodoro) 

    def restart_timer_pomodoro(self):
        # Restart the timer to its defined time
        self.running_pomodoro = False
        self.work = True
        self.work_pomodoro = self.work_time
        self.counter = self.counter_max
        self.counter_hud = 0
        self.update_label_pomodoro(self.work_pomodoro)

    def define_timer_pomodoro(self, entry):
        # Set the timer time in minutes
        try:
            self.timer_value_pomodoro = int(entry.get()) * 60
            if self.timer_value_pomodoro < 600:
                raise ValueError    
            # Define the work and its rests based on the defined time
            if self.timer_value_pomodoro <= 3600:
                self.counter = 2
                self.rest_time = 300
                work_time_per_cycle = (self.timer_value_pomodoro - self.rest_time) / self.counter
                
            elif self.timer_value_pomodoro <= 14400:
                self.counter = 3
                self.rest_time = 600
                work_time_per_cycle = (self.timer_value_pomodoro - self.rest_time * 2) / self.counter
            else:
                self.timer_value_pomodoro = 14400
                self.counter = 3
                self.rest_time = 600
                work_time_per_cycle = (self.timer_value_pomodoro - self.rest_time * 2) / self.counter
                
            self.work_pomodoro = int(work_time_per_cycle)
            self.work_time = self.work_pomodoro
            self.update_label_pomodoro(self.work_pomodoro)
            self.counter_max = self.counter
            self.counter_hud = 0
            self.update_session_pomodoro()
            self.beeped_pomodoro = False

        except ValueError:
            messagebox.showerror("Invalid Timer", "The minimum time must be 10 minutes for adequate cycles")

    def beep_sound_pomodoro(self):
        # Beep when the timer is out
        if not self.beeped_pomodoro:
            ws.Beep(438, 1000)
            self.beeped_pomodoro = True

def main():
    # Iniciate the app
    
    root = ttk.Window(themename='darkly')
    app = TimerApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
