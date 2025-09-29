import tkinter as tk
from tkinter import messagebox, font

class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Most Dangerous Writing App")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        self.primary_font = font.Font(family="Courier New", size=14)
        self.secondary_font = font.Font(family="Helvetica", size=12)
        self.timer_font = font.Font(family="Impact", size=24)
        self.text_color = "#f0f0f0"
        self.background_color = "#1e1e1e"
        self.text_area_bg = "#2b2b2b"
        self.accent_color = "#e63946"

        self.inactivity_limit = 5  # seconds
        self.time_left = self.inactivity_limit
        self.timer_running = False
        self.word_count = 0
        self.timer_id = None

        main_frame = tk.Frame(root, bg=self.background_color)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(main_frame, bg=self.background_color)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text="Dangerous Writing App", font=("Impact", 28), fg=self.text_color, bg=self.background_color)
        title_label.pack()

        subtitle_label = tk.Label(header_frame, text="Don't stop writing, or all your progress will be lost.", font=self.secondary_font, fg=self.text_color, bg=self.background_color)
        subtitle_label.pack(pady=(0, 10))

        stats_frame = tk.Frame(main_frame, bg=self.background_color)
        stats_frame.pack(fill=tk.X, pady=10)

        self.word_count_label = tk.Label(stats_frame, text="Words: 0", font=self.secondary_font, fg=self.text_color, bg=self.background_color)
        self.word_count_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(stats_frame, text=f"Time Left: {self.time_left}", font=self.timer_font, fg=self.accent_color, bg=self.background_color)
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        # Text Area
        self.text_area = tk.Text(main_frame, wrap=tk.WORD, font=self.primary_font, bg=self.text_area_bg, fg=self.text_color, insertbackground=self.text_color, undo=True, borderwidth=2, relief="solid")
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.focus_set()

        self.text_area.bind("<Key>", self.start_session)
        self.text_area.bind("<KeyRelease>", self.update_stats)

    def start_session(self, event=None):
        if not self.timer_running:
            self.timer_running = True
            self.countdown()
        self.reset_timer()

    def update_stats(self, event=None):
        text_content = self.text_area.get("1.0", tk.END).strip()
        words = text_content.split()
        self.word_count = len(words)
        self.word_count_label.config(text=f"Words: {self.word_count}")

    def reset_timer(self):
        self.time_left = self.inactivity_limit
        self.timer_label.config(text=f"Time Left: {self.time_left}", fg=self.accent_color)
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.countdown()

    def countdown(self):
        if self.timer_running:
            self.timer_label.config(text=f"Time Left: {self.time_left}")

            if self.time_left > 0:
                self.time_left -= 1
                self.timer_id = self.root.after(1000, self.countdown)
            else:
                self.clear_text()

    def clear_text(self):
        self.timer_running = False
        text_content = self.text_area.get("1.0", tk.END).strip()
        if not text_content:
            return

        self.text_area.config(bg="#8b0000")
        self.root.update()
        messagebox.showwarning("Time's up!", f"You stopped writing for {self.inactivity_limit} seconds and lost {self.word_count} words!")
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(bg=self.text_area_bg)
        self.update_stats()
        self.time_left = self.inactivity_limit
        self.timer_label.config(text=f"Time Left: {self.time_left}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()