import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Script Launcher")
        self.geometry("600x400")
        
        self.label = tk.Label(self, text="Launch Scripts")
        self.label.pack(pady=10)

        self.launch_button = tk.Button(self, text="Launch Scripts", command=self.launch_scripts)
        self.launch_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_app)
        self.quit_button.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=15)
        self.log_text.pack(pady=10)

    def launch_scripts(self):
        try:
            # Launch RaspQuickLaunch.py
            self.log_message("Launching RaspQuickLaunch.py...")
            result = subprocess.run(["python", "RaspQuickLaunch.py"], capture_output=True, text=True, check=True)
            self.log_message(result.stdout)
            self.log_message("RaspQuickLaunch.py finished.")

            # Launch WatchDogeSupercharged.py
            self.log_message("Launching WatchDogeSupercharged.py...")
            result = subprocess.run(["python", "WatchDogeSupercharged.py"], capture_output=True, text=True, check=True)
            self.log_message(result.stdout)
            self.log_message("WatchDogeSupercharged.py finished.")

            messagebox.showinfo("Success", "Both scripts have been successfully launched.")
        except subprocess.CalledProcessError as e:
            self.log_message(f"Error: {e.stderr}")
            messagebox.showerror("Error", f"An error occurred while launching the scripts: {e.stderr}")
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def quit_app(self):
        self.quit()

if __name__ == "__main__":
    app = AppLauncher()
    app.mainloop()
